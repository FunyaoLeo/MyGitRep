
library('igraph')
library('Matrix')
memory.limit()

path <- "C:/Users/Scott/GOOGLE/EE232/P4/actor_actress_weighted_double.csv"
el <- read.csv(path)
num_el <- as.matrix(el)




el[,1] <- as.character(el[,1])

el[,2] <- as.character(el[,2])

el <- as.matrix(el)

g <- graph.edgelist(el[,1:2])
E(g)$weight <- as.numeric(el[,3])

plot(degree.distribution(g, v = V(g),mode = "in"))

name_id <- read.csv("C:/Users/Scott/GOOGLE/EE232/P4/name_id_list.csv")

getID <- function(name_id,name){
    actorNode <- which(name_id == name)-1
    return(actorNode)
}

getName <- function(name_id,ID){
    actorName <- name_id[ID+1,1]
    return(actorName)
}




getPairing <- function(inputName){
    actorInput <- getID(name_id,inputName)
    Prob <- numeric()
    line <- which(num_el[,1] == actorInput)
    for(i in 1:length(line)){
        Prob[i] <- num_el[line[i],][3]
    }
    index <- which(Prob == max(Prob))
    actorOutput <- num_el[line[index[1]],][2]
    print(num_el[line[index[1]],][3])
    return(getName(name_id,actorOutput))
}
    


getPairing("Pitt, Brad")

rank_score <- page.rank (g,algo = "prpack",vids = V(g),directed = TRUE, damping = 0.85,weights = NULL)

rank_vector <- rank_score$vector
top10 <- sort(rank_vector,decreasing = TRUE)[1:10]
print(top10)

print(names(top10))
num_V = as.matrix(V(g))
x = which(names(V(g)) == names(top10[10]))
degree(g,v = x ,mode = "in")




