Instruction:
1 Please place "comments-minimal.json.bz2", "submissions.json.bz2" and "labeled_data.csv" 
under the same directory of reddit_model.py and cleantext.py. 
2 Please make sure the disk have more than 8 GB free space. 
3 Open virtual box, change directory to the project directory
4 Run command "spark-submit ./reddit_model.py"
5 This will take several hours to run because it involves a lot of read and write. Without
these reading and writing, the program will take forever.(Here are only use 20% of the
data)

Extra credit task :
Task 10 problem5: In this task, we try to find whether people change their attitude towards 
president Trump with the change of time. Also we combine the result of negative and postive 
to show real evaluation of Trump in people'mind.