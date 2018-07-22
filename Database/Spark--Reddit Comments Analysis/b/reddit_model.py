from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext


# IMPORT OTHER MODULES HERE
import re
import string
import argparse
import sys
import json
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidator, CrossValidatorModel, ParamGridBuilder
from pyspark.ml.evaluation import BinaryClassificationEvaluator

def sanitize(text):
    """Do parse the text in variable "text" according to the spec, and return
    a LIST containing FOUR strings
    1. The parsed text.
    2. The unigrams
    3. The bigrams
    4. The trigrams
    """

    # YOUR CODE GOES BELOW:
    # 1. Replace new lines and tab characters with a single space.
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    # 2. Remove URLs
    text = re.sub('(http|https)?:\/(\/\S*)?', '', text)

    # 3. Split text on a single space. If there are multiple contiguous spaces,
    # you will need to remove empty tokens after doing the split.
    text = re.sub(' +', ' ', text)

    # 4. Separate all external punctuation such as periods, commas, etc.
    text=" "+text+" "
    text=list(text)
    for index in range(len(text)):
        if text[index] in string.punctuation:
            if(text[index+1] not in string.ascii_letters or text[index-1] not in string.ascii_letters) and (text[index+1] not in string.digits or text[index-1] not in string.digits):
                if not (text[index]=="$" and text[index+1] in string.digits ):
                    text[index]=" "+text[index]+" "
    del text[0]
    del text[-1]
    text = "".join(text)

    # 5. Remove all punctuations
    text = text.split(" ")
    while "" in text:
        text.remove("")
    remain_pun=[".", "!", "?", ":", ",", ";"]
    for index in range(len(text)):
        if text[index] in string.punctuation and text[index] not in remain_pun:
            text[index] = ""
    while "" in text:
        text.remove("")
    text = " ".join(text)

    # 6. Convert all text to lower cases
    text = text.lower()

    parsed_text = text

    # 8. unigram
    punc = string.punctuation
    original_split_text = text.split(' ')
    unigram_text = ""
    flag = 0
    for i in range(len(original_split_text)):
        if(original_split_text[i] in punc):
            continue
        if(flag==1):
            unigram_text += ' '
        flag=1
        unigram_text += original_split_text[i]

    # 8. bigram
    bigram_text = ""
    flag = 0
    for i in range(len(original_split_text)-1):
        if(original_split_text[i] in punc or original_split_text[i+1] in punc):
            continue
        if(flag==1):
            bigram_text += ' '
        flag=1
        bigram_text += original_split_text[i]
        bigram_text += '_'
        bigram_text += original_split_text[i+1]
        #bigram_text += ' '

    # 8. trigram
    trigram_text = ""
    flag = 0
    for i in range(len(original_split_text)-2):
        if(original_split_text[i] in punc or original_split_text[i+1] in punc or original_split_text[i+2] in punc):
            continue
        if(flag==1):
            trigram_text += ' '
        flag=1
        trigram_text += original_split_text[i]
        trigram_text += '_'
        trigram_text += original_split_text[i+1]
        trigram_text += '_'
        trigram_text += original_split_text[i+2]
        #trigram_text += ' '

    return [unigram_text, bigram_text, trigram_text]

def remove_t3(link_id):
    return re.sub("^t3_", "", link_id)

def replace_gt(body):
    return re.sub("^&gt", "/s", body)

def get_pos_probability(probability):
    if float(probability[1]) >= 0.2:
        return 1
    else:
        return 0

def get_neg_probability(probability):
    if float(probability[1]) >= 0.25:
        return 1
    else:
        return 0

def concat_string_arrays(ngram):
    string_arrays = []
    for gram in ngram:
        string_arrays = string_arrays + gram.split(" ")
    return string_arrays

def main(context):
    """Main function takes a Spark SQL context."""
    # YOUR CODE HERE
    # YOU MAY ADD OTHER FUNCTIONS AS NEEDED

    sqlContext = SQLContext(sc)
    sc.addPyFile("cleantext.py")
    
    # Task 1
    # Code for task 1
    comments = sqlContext.read.json("comments-minimal.json.bz2")
    comments.write.parquet("comments.parquet")
    submissions = sqlContext.read.json("submissions.json.bz2")
    submissions.write.parquet("submissions.parquet")
    labels = sqlContext.read.load("labeled_data.csv", format="csv", sep=",", inferSchema="true", header="true")
    labels.write.save("labels.parquet", format="parquet")
    """"
    comments = sqlContext.read.parquet("comments.parquet")
    submissions = sqlContext.read.parquet("submissions.parquet")
    labels = sqlContext.read.parquet("labels.parquet")
    """
    
    # Task 2
    # Code for task 2
    comments.createOrReplaceTempView("comments")
    submissions.createOrReplaceTempView("submissions")
    labels.createOrReplaceTempView("labels")
    filtered_data = sqlContext.sql("select Input_id, body, labeldem, labelgop, labeldjt from comments, labels where comments.id=labels.Input_id")
    # filtered_data.write.parquet("filtered_data.parquet")
    
    # Task 4
    # Code for task 4
    # Cited from https://docs.databricks.com/spark/latest/spark-sql/udf-in-python.html
    # filtered_data = sqlContext.read.parquet("filtered_data.parquet")
    filtered_data.createOrReplaceTempView("filtered_data")
    sqlContext.udf.register("sanitize", sanitize, ArrayType(StringType()))
    ngram_table = sqlContext.sql("select *, sanitize(body) as ngram from filtered_data")
    ngram_table.createOrReplaceTempView("ngram_table")

    # Task 5
    # Code for task 5
    sqlContext.udf.register("concat_string_arrays", concat_string_arrays, ArrayType(StringType()))
    ngram_table = sqlContext.sql("select Input_id, body, labeldem, labelgop, labeldjt, concat_string_arrays(ngram) as ngram from ngram_table")
    ngram_table.createOrReplaceTempView("ngram_table")
    
    # Task 6A, 6B
    # Code for task 6A, 6B
    cv = CountVectorizer(inputCol="ngram", outputCol="features", minDF=5.0, binary=True)
    model = cv.fit(ngram_table)
    result = model.transform(ngram_table)
    result.createOrReplaceTempView("result")
    
    ngram_table_finished = sqlContext.sql("select *, if (labeldjt=1, 1, 0) as positive, if(labeldjt = -1, 1, 0) as negative from result")
    ngram_table_finished.createOrReplaceTempView("ngram_table_finished")
    
    # Task 7
    # Code for task 7
    pos = sqlContext.sql("select positive as label, features from ngram_table_finished")
    neg = sqlContext.sql("select negative as label, features from ngram_table_finished")

    # Initialize two logistic regression models.
    # Replace labelCol with the column containing the label, and featuresCol with the column containing the features.
    poslr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
    neglr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
    # This is a binary classifier so we need an evaluator that knows how to deal with binary classifiers.
    posEvaluator = BinaryClassificationEvaluator()
    negEvaluator = BinaryClassificationEvaluator()
    # There are a few parameters associated with logistic regression. We do not know what they are a priori.
    # We do a grid search to find the best parameters. We can replace [1.0] with a list of values to try.
    # We will assume the parameter is 1.0. Grid search takes forever.
    posParamGrid = ParamGridBuilder().addGrid(poslr.regParam, [1.0]).build()
    negParamGrid = ParamGridBuilder().addGrid(neglr.regParam, [1.0]).build()
    # We initialize a 5 fold cross-validation pipeline.
    posCrossval = CrossValidator(
        estimator=poslr,
        evaluator=posEvaluator,
        estimatorParamMaps=posParamGrid,
        numFolds=5)
    negCrossval = CrossValidator(
        estimator=neglr,
        evaluator=negEvaluator,
        estimatorParamMaps=negParamGrid,
        numFolds=5)
    # Although crossvalidation creates its own train/test sets for
    # tuning, we still need a labeled test set, because it is not
    # accessible from the crossvalidator (argh!)
    # Split the data 50/50
    posTrain, posTest = pos.randomSplit([0.5, 0.5])
    negTrain, negTest = neg.randomSplit([0.5, 0.5])
    # Train the models
    print("Training positive classifier...")
    posModel = posCrossval.fit(posTrain)
    print("Training negative classifier...")
    negModel = negCrossval.fit(negTrain)

    # Once we train the models, we don't want to do it again. We can save the models and load them again later.
    posModel.save("pos.model")
    negModel.save("neg.model")
    
    """
    # Load Model
    posModel=CrossValidatorModel.load("pos.model")
    negModel=CrossValidatorModel.load("neg.model")
    """

    # Task 8
    # Code for task 8
    sqlContext.udf.register("remove_t3", remove_t3)
    comments = sqlContext.sql("select body, id, remove_t3(link_id) as link_id, score as comment_score, created_utc, author_flair_text from comments order by link_id")
    submissions = sqlContext.sql("select title, id , score as story_score from submissions order by id")
    comments.createOrReplaceTempView("comments")
    submissions.createOrReplaceTempView("submissions")

    comments.write.parquet("comments_new.parquet")
    submissions.write.parquet("submissions_new.parquet")

    comments_new = sqlContext.read.parquet("comments_new.parquet")
    submissions_new = sqlContext.read.parquet("submissions_new.parquet")
    comments_new.createOrReplaceTempView("comments_new")
    submissions_new.createOrReplaceTempView("submissions_new")

    data_set = sqlContext.sql("select comments_new.id as id, body,  comment_score,  story_score, link_id, created_utc, author_flair_text, title from comments_new, submissions_new where comments_new.link_id=submissions_new.id")
    data_set = data_set.sample(False, 0.2, None)
    data_set.createOrReplaceTempView("data_set")

    data_set.write.parquet("data_set.parquet")
    data_set = sqlContext.read.parquet("data_set.parquet")

    # Task 9
    # Code for task 9
    sqlContext.udf.register("replace_gt", replace_gt)
    data_set1 = sqlContext.sql("select id, replace_gt(body) as body, comment_score,  story_score, link_id, created_utc, author_flair_text, title from data_set")
    data_set1.createOrReplaceTempView("data_set1")
    data_set1.write.parquet("data_set1.parquet")
    data_set1 = sqlContext.read.parquet("data_set1.parquet")
    data_set1.createOrReplaceTempView("data_set1")

    data_set2 = sqlContext.sql("select * from data_set1 where body not like \"%/s%\"")
    data_set2.createOrReplaceTempView("data_set2")
    data_set2.write.parquet("data_set2.parquet")
    data_set2 = sqlContext.read.parquet("data_set2.parquet")
    data_set2.createOrReplaceTempView("data_set2")

    data_set3 = sqlContext.sql("select *, sanitize(body) as ngram from data_set2")
    data_set3.createOrReplaceTempView("data_set3")
    data_set3.write.parquet("data_set3.parquet")
    data_set3 = sqlContext.read.parquet("data_set3.parquet")
    data_set3.createOrReplaceTempView("data_set3")

    data_set4 = sqlContext.sql("select id, link_id, comment_score,  story_score, created_utc, author_flair_text, title, concat_string_arrays(ngram) as ngram from data_set3")
    data_set4.createOrReplaceTempView("data_set4")
    data_set4.write.parquet("data_set4.parquet")
    data_set5 = sqlContext.read.parquet("data_set4.parquet")
    data_set5.createOrReplaceTempView("data_set4")

    temp_result = model.transform(data_set5)
    temp_result.createOrReplaceTempView("temp_result")
    temp_result.write.parquet("temp_result1.parquet")
    temp_result = sqlContext.read.parquet("temp_result1.parquet")
    temp_result.createOrReplaceTempView("temp_result1")

    sqlContext.udf.register("get_pos_probability", get_pos_probability)
    temp_result = posModel.transform(temp_result)
    temp_result.createOrReplaceTempView("temp_result")
    temp_result = sqlContext.sql("select id,  link_id, created_utc, author_flair_text, comment_score,  story_score, features, get_pos_probability(probability) as pos from temp_result")
    temp_result.createOrReplaceTempView("temp_result")
    temp_result.write.parquet("temp_result2.parquet")
    temp_result=sqlContext.read.parquet("temp_result2.parquet")
    temp_result.createOrReplaceTempView("temp_result2")

    sqlContext.udf.register("get_neg_probability", get_neg_probability)
    temp_result = negModel.transform(temp_result)
    temp_result.createOrReplaceTempView("temp_result")
    result = sqlContext.sql("select id,  link_id, created_utc, author_flair_text,  comment_score,  story_score, pos, get_neg_probability(probability) as neg from temp_result")
    result.createOrReplaceTempView("result")
    result.write.parquet("task9_final_result.parquet")
    result = sqlContext.read.parquet("task9_final_result.parquet")
    result.createOrReplaceTempView("result")

    # Task 10
    # Code for task 10

    # task 10 pos
    result_simple = sqlContext.sql("select link_id, pos , neg from result")
    result_simple.createOrReplaceTempView("result_simple")
    posnum = sqlContext.sql(
        "select link_id,  count(1) as positive_number from result_simple where pos=1 group by link_id ")
    posnum.createOrReplaceTempView("posnum")
    posnumdiv = sqlContext.sql("select link_id,  count(1) as div from result_simple group by link_id ")
    posnumdiv.createOrReplaceTempView("posnumdiv")

    task10_1_pos = sqlContext.sql(
        "select posnum.link_id ,positive_number ,(positive_number)/(div) as percentage from posnum , posnumdiv where posnum.link_id=posnumdiv.link_id")
    task10_1_pos.createOrReplaceTempView("task10_1_pos")
    task10_1_pos.show()
    task10_1_pos.toPandas().to_csv("task10_1_pos.csv", header=True)

    result_day = sqlContext.sql("select  Date(from_unixtime(created_utc)) as day, pos, neg from result")
    result_day.createOrReplaceTempView("result_day")
    dayposnum = sqlContext.sql("select day, count(1) as count_day , day from result_day where pos=1 group by day")
    dayposnum.createOrReplaceTempView("dayposnum")
    dayposnumdiv = sqlContext.sql("select day, count(1) as div , day from result_day  group by day")
    dayposnumdiv.createOrReplaceTempView("dayposnumdiv")
    task10_2_pos = sqlContext.sql(
        "select dayposnum.day, count_day,(count_day)/(div) as percentage from dayposnum, dayposnumdiv where dayposnum.day=dayposnumdiv.day  ")
    task10_2_pos.createOrReplaceTempView("task10_2_pos")
    task10_2_pos.show()
    task10_2_pos.toPandas().to_csv("task10_2_pos.csv", header=True)

    result_state = sqlContext.sql(
        "select author_flair_text as state, pos, neg from result where author_flair_text is not null")
    result_state.createOrReplaceTempView("result_state")
    stateposnum = sqlContext.sql(
        "select state, count(1) as count_state , state from result_state where pos=1 group by state")
    stateposnum.createOrReplaceTempView("stateposnum")
    stateposnumdiv = sqlContext.sql("select state, count(1) as div , state from result_state group by state")
    stateposnumdiv.createOrReplaceTempView("stateposnumdiv")
    task10_3_pos = sqlContext.sql(
        "select stateposnum.state, count_state,(count_state)/(div) as percentage from stateposnum, stateposnumdiv where stateposnum.state=stateposnumdiv.state")
    task10_3_pos.createOrReplaceTempView("task10_3_pos")
    task10_3_pos.show()
    task10_3_pos.toPandas().to_csv("task10_3_pos.csv", header=True)

    result_commentscore = sqlContext.sql("select comment_score, pos, neg from result")
    result_commentscore.createOrReplaceTempView("result_commentscore")
    comnum = sqlContext.sql(
        "select  comment_score , count(1) as count_comscore from result_commentscore where pos=1 group by comment_score")
    comnum.createOrReplaceTempView("comnum")
    comnumdiv = sqlContext.sql(
        "select  comment_score , count(1) as div from result_commentscore group by comment_score")
    comnumdiv.createOrReplaceTempView("comnumdiv")
    task10_41_pos = sqlContext.sql(
        "select comnum.comment_score,(count_comscore)/(div) as percentage from comnum, comnumdiv where comnum.comment_score=comnumdiv.comment_score")
    task10_41_pos.createOrReplaceTempView("task10_41_pos")
    task10_41_pos.show()
    task10_41_pos.toPandas().to_csv("task10_41_pos.csv", header=True)

    result_storyscore = sqlContext.sql("select story_score, pos, neg from result")
    result_storyscore.createOrReplaceTempView("result_storyscore")
    storynum = sqlContext.sql(
        "select count(1) as count_storyscore , story_score from result_storyscore where pos=1 group by story_score")
    storynum.createOrReplaceTempView("storynum")
    storynumdiv = sqlContext.sql("select count(1) div , story_score from result_storyscore group by story_score")
    storynumdiv.createOrReplaceTempView("storynumdiv")
    task10_42_pos = sqlContext.sql(
        "select storynum.story_score,(count_storyscore)/(div) as percentage from storynum ,storynumdiv where storynum.story_score=storynumdiv.story_score")
    task10_42_pos.createOrReplaceTempView("task10_42_story")
    task10_42_pos.show()
    task10_42_pos.toPandas().to_csv("task10_42pos.csv", header=True)

    # task 10 neg
    result_simple = sqlContext.sql("select link_id, pos , neg from result")
    result_simple.createOrReplaceTempView("result_simple")
    negnum = sqlContext.sql(
        "select link_id,  count(1) as negitive_number from result_simple where neg=1 group by link_id ")
    negnum.createOrReplaceTempView("negnum")
    negnumdiv = sqlContext.sql("select link_id,  count(1) as div from result_simple group by link_id ")
    negnumdiv.createOrReplaceTempView("negnumdiv")

    task10_1_neg = sqlContext.sql(
        "select negnum.link_id ,negitive_number ,(negitive_number)/(div) as percentage from negnum , negnumdiv where negnum.link_id=negnumdiv.link_id")
    task10_1_neg.createOrReplaceTempView("task10_1_neg")
    task10_1_neg.show()
    task10_1_neg.toPandas().to_csv("task10_1_neg.csv", header=True)

    result_day = sqlContext.sql("select  Date(from_unixtime(created_utc)) as day, pos, neg from result")
    result_day.createOrReplaceTempView("result_day")
    daynegnum = sqlContext.sql("select day, count(1) as count_day , day from result_day where neg=1 group by day")
    daynegnum.createOrReplaceTempView("daynegnum")
    daynegnumdiv = sqlContext.sql("select day, count(1) as div , day from result_day  group by day")
    daynegnumdiv.createOrReplaceTempView("daynegnumdiv")
    task10_2_neg = sqlContext.sql(
        "select daynegnum.day, count_day,(count_day)/(div) as percentage from daynegnum, daynegnumdiv where daynegnum.day=daynegnumdiv.day  ")
    task10_2_neg.createOrReplaceTempView("task10_2_neg")
    task10_2_neg.show()
    task10_2_neg.toPandas().to_csv("task10_2_neg.csv", header=True)

    result_state = sqlContext.sql(
        "select author_flair_text as state, pos, neg from result where author_flair_text is not null")
    result_state.createOrReplaceTempView("result_state")
    statenegnum = sqlContext.sql(
        "select state, count(1) as count_state , state from result_state where neg=1 group by state")
    statenegnum.createOrReplaceTempView("statenegnum")
    statenegnumdiv = sqlContext.sql("select state, count(1) as div , state from result_state group by state")
    statenegnumdiv.createOrReplaceTempView("statenegnumdiv")
    task10_3_neg = sqlContext.sql(
        "select statenegnum.state, count_state,(count_state)/(div) as percentage from statenegnum, statenegnumdiv where statenegnum.state=statenegnumdiv.state")
    task10_3_neg.createOrReplaceTempView("task10_3_neg")
    task10_3_neg.show()
    task10_3_neg.toPandas().to_csv("task10_3_neg.csv", header=True)

    result_commentscore = sqlContext.sql("select comment_score, pos, neg from result")
    result_commentscore.createOrReplaceTempView("result_commentscore")
    comnum = sqlContext.sql(
        "select  comment_score , count(1) as count_comscore from result_commentscore where neg=1 group by comment_score")
    comnum.createOrReplaceTempView("comnum");
    comnumdiv = sqlContext.sql(
        "select  comment_score , count(1) as div from result_commentscore group by comment_score")
    comnumdiv.createOrReplaceTempView("comnumdiv");
    task10_41_neg = sqlContext.sql(
        "select comnum.comment_score,(count_comscore)/(div) as percentage from comnum, comnumdiv where comnum.comment_score=comnumdiv.comment_score")
    task10_41_neg.createOrReplaceTempView("task10_41_neg")
    task10_41_neg.show()
    task10_41_neg.toPandas().to_csv("task10_41_neg.csv", header=True)

    result_storyscore = sqlContext.sql("select story_score, pos, neg from result")
    result_storyscore.createOrReplaceTempView("result_storyscore")
    storynum = sqlContext.sql(
        "select count(1) as count_storyscore , story_score from result_storyscore where neg=1 group by story_score")
    storynum.createOrReplaceTempView("storynum");
    storynumdiv = sqlContext.sql("select count(1) div , story_score from result_storyscore group by story_score")
    storynumdiv.createOrReplaceTempView("storynumdiv");
    task10_42_neg = sqlContext.sql(
        "select storynum.story_score,(count_storyscore)/(div) as percentage from storynum ,storynumdiv where storynum.story_score=storynumdiv.story_score")
    task10_42_neg.createOrReplaceTempView("task10_42_story")
    task10_42_neg.show()
    task10_42_neg.toPandas().to_csv("task10_42_neg.csv", header=True)
    
    
    
    #task 10 question5
    
    result_day=sqlContext.sql("select  Date(from_unixtime(created_utc)) as day, pos, neg from result")
    result_day.createOrReplaceTempView("result_day")
    dayposnum=sqlContext.sql("select day, count(1) as count_day , day from result_day where pos=0 and neg =0 group by day")
    dayposnum.createOrReplaceTempView("dayposnum")
    dayposnumdiv=sqlContext.sql("select day, count(1) as div , day from result_day  group by day")
    dayposnumdiv.createOrReplaceTempView("dayposnumdiv")
    day00=sqlContext.sql("select dayposnum.day, count_day,(count_day)/(div) as percentage from dayposnum, dayposnumdiv where dayposnum.day=dayposnumdiv.day  ")
    day00.createOrReplaceTempView("day00")
    day00.show()
    day00.toPandas().to_csv("day00.csv", header=True)

    result_day=sqlContext.sql("select  Date(from_unixtime(created_utc)) as day, pos, neg from result")
    result_day.createOrReplaceTempView("result_day")
    dayposnum=sqlContext.sql("select day, count(1) as count_day , day from result_day where pos=1 and neg =0 group by day")
    dayposnum.createOrReplaceTempView("dayposnum")
    dayposnumdiv=sqlContext.sql("select day, count(1) as div , day from result_day  group by day")
    dayposnumdiv.createOrReplaceTempView("dayposnumdiv")
    day10=sqlContext.sql("select dayposnum.day, count_day,(count_day)/(div) as percentage from dayposnum, dayposnumdiv where dayposnum.day=dayposnumdiv.day  ")
    day10.createOrReplaceTempView("day10")
    day10.show()
    day10.toPandas().to_csv("day10.csv", header=True)

    result_day=sqlContext.sql("select  Date(from_unixtime(created_utc)) as day, pos, neg from result")
    result_day.createOrReplaceTempView("result_day")
    dayposnum=sqlContext.sql("select day, count(1) as count_day , day from result_day where pos=0 and neg =1 group by day")
    dayposnum.createOrReplaceTempView("dayposnum")
    dayposnumdiv=sqlContext.sql("select day, count(1) as div , day from result_day  group by day")
    dayposnumdiv.createOrReplaceTempView("dayposnumdiv")
    day01=sqlContext.sql("select dayposnum.day, count_day,(count_day)/(div) as percentage from dayposnum, dayposnumdiv where dayposnum.day=dayposnumdiv.day  ")
    day01.createOrReplaceTempView("day01")
    day01.show()
    day01.toPandas().to_csv("day01.csv", header=True)

    result_day=sqlContext.sql("select  Date(from_unixtime(created_utc)) as day, pos, neg from result")
    result_day.createOrReplaceTempView("result_day")
    dayposnum=sqlContext.sql("select day, count(1) as count_day , day from result_day where pos=1 and neg =1 group by day")
    dayposnum.createOrReplaceTempView("dayposnum")
    dayposnumdiv=sqlContext.sql("select day, count(1) as div , day from result_day  group by day")
    dayposnumdiv.createOrReplaceTempView("dayposnumdiv")
    day11=sqlContext.sql("select dayposnum.day, count_day,(count_day)/(div) as percentage from dayposnum, dayposnumdiv where dayposnum.day=dayposnumdiv.day  ")
    day11.createOrReplaceTempView("day11")
    day11.show()
    day11.toPandas().to_csv("day11.csv", header=True)

if __name__ == "__main__":
    conf = SparkConf().setAppName("CS143 Project 2B")
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    sc.addPyFile("cleantext.py")
    main(sqlContext)

