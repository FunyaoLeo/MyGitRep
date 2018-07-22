import csv

actor_name = [["Name", "ID"]]

merges = []
with open('merge.txt', 'r') as merge_file:
    id = 0
    for line in merge_file:
        line = line[:-1]
        dict = {}
        line_break = line.split("\t\t")
        name_vector = [line_break[0], str(id)]
        actor_name.append(name_vector)
        for i in range(1, len(line_break)):
            dict[line_break[i]] = id
        merges.append(dict)
        id = id + 1
merge_file.close()

myFile = open('name_id_list.csv', 'w')
with myFile:
    writer = csv.writer(myFile, lineterminator='\n')
    writer.writerows(actor_name)
myFile.close()
print ("name-id finished")

merges1 = merges
merges2 = merges

myFile = open('actor_actress_weighted.csv', 'w')
with myFile:
    writer = csv.writer(myFile, lineterminator='\n')
    writer.writerows([["V1", "V2", "weight"]])
    total_actor_num = len(merges)

    for actor_index1 in range(total_actor_num):
        actor_1 = merges1[actor_index1]
        movie_num1 = len(actor_1.keys())
        for actor_index2 in range(total_actor_num):
            if actor_index1 == actor_index2:
                continue
            common = 0
            actor_2 = merges2[actor_index2]
            for movies1 in actor_1.keys():
                if actor_2.has_key(movies1):
                    common = common+1
            if common != 0:
                writer.writerows([[str(actor_index1), str(actor_index2), str(common*1.0 / movie_num1)]])
        if (actor_index1 % 2000 == 0):
            print ("have finished " + str(actor_index1))
myFile.close()


id_movie_num = {}
with open('merge.txt', 'r') as merge_file:
    id = 0
    for line in merge_file:
        line = line[:-1]
        line_break = line.split("\t\t")
        id_movie_num[str(id)] = len(line_break)-1
        id = id + 1
merge_file.close()

with open('actor_actress_weighted.csv', 'r') as original_file:
    myFile = open('actor_actress_weighted_double.csv', 'w')
    with myFile:
        writer = csv.writer(myFile, lineterminator='\n')
        line_num = 0
        for line in original_file:
            line = line[:-1]
            line_break = line.split(",")
            writer.writerows([[line_break[0], line_break[1], line_break[2]]])
            if line_num != 0:
                id1 = line_break[1]
                id2 = line_break[0]
                weight = float(line_break[2])*id_movie_num[id2]/id_movie_num[id1]
                writer.writerows([[id1, id2, str(weight)]])
            line_num = line_num+1
    myFile.close()
original_file.close()


