"""
Author      : Yi-Chieh Wu, Sriram Sankararaman
Description : Famous Faces
"""

# python libraries
import collections

# numpy libraries
import numpy as np

# matplotlib libraries
import matplotlib.pyplot as plt

# libraries specific to project
import util
from util import *
from cluster import *

######################################################################
# helper functions
######################################################################

def build_face_image_points(X, y) :
    """
    Translate images to (labeled) points.
    
    Parameters
    --------------------
        X     -- numpy array of shape (n,d), features (each row is one image)
        y     -- numpy array of shape (n,), targets
    
    Returns
    --------------------
        point -- list of Points, dataset (one point for each image)
    """
    
    n,d = X.shape
    
    images = collections.defaultdict(list) # key = class, val = list of images with this class
    for i in xrange(n) :
        images[y[i]].append(X[i,:])
    
    points = []
    for face in images :
        count = 0
        for im in images[face] :
            points.append(Point(str(face) + '_' + str(count), face, im))
            count += 1

    return points


def plot_clusters(clusters, title, average) :
    """
    Plot clusters along with average points of each cluster.

    Parameters
    --------------------
        clusters -- ClusterSet, clusters to plot
        title    -- string, plot title
        average  -- method of ClusterSet
                    determines how to calculate average of points in cluster
                    allowable: ClusterSet.centroids, ClusterSet.medoids
    """
    
    plt.figure()
    np.random.seed(20)
    label = 0
    colors = {}
    centroids = average(clusters)
    for c in centroids :
        coord = c.attrs
        plt.plot(coord[0],coord[1], 'ok', markersize=12)
    for cluster in clusters.members :
        label += 1
        colors[label] = np.random.rand(3,)
        for point in cluster.points :
            coord = point.attrs
            plt.plot(coord[0], coord[1], 'o', color=colors[label])
    plt.title(title)
    plt.show()


def generate_points_2d(N, seed=1234) :
    """
    Generate toy dataset of 3 clusters each with N points.
    
    Parameters
    --------------------
        N      -- int, number of points to generate per cluster
        seed   -- random seed
    
    Returns
    --------------------
        points -- list of Points, dataset
    """
    np.random.seed(seed)
    
    mu = [[0,0.5], [1,1], [2,0.5]]
    sigma = [[0.1,0.1], [0.25,0.25], [0.15,0.15]]
    
    label = 0
    points = []
    for m,s in zip(mu, sigma) :
        label += 1
        for i in xrange(N) :
            x = util.random_sample_2d(m, s)
            points.append(Point(str(label)+'_'+str(i), label, x))
    
    return points


######################################################################
# k-means and k-medoids
######################################################################

def random_init(points, k) :
    """
    Randomly select k unique elements from points to be initial cluster centers.
    
    Parameters
    --------------------
        points         -- list of Points, dataset
        k              -- int, number of clusters
    
    Returns
    --------------------
        initial_points -- list of k Points, initial cluster centers
    """
    ### ========== TODO : START ========== ###
    # part 2c: implement (hint: use np.random.choice)
    index = np.random.choice(len(points),k,replace=False)
    initial_points = []
    for i in index:
        initial_points.append(points[i])
    return initial_points
    ### ========== TODO : END ========== ###


def cheat_init(points) :
    """
    Initialize clusters by cheating!
    
    Details
    - Let k be number of unique labels in dataset.
    - Group points into k clusters based on label (i.e. class) information.
    - Return medoid of each cluster as initial centers.
    
    Parameters
    --------------------
        points         -- list of Points, dataset
    
    Returns
    --------------------
        initial_points -- list of k Points, initial cluster centers
    """
    ### ========== TODO : START ========== ###
    # part 2f: implement
    k_list = []
    for point in points:
        if point.label not in k_list:
            k_list.append(point.label)
    k = len(k_list)
    cluster_points = []
    for k_loop in range(k):
        cluster_points.append([])
    for point in points:
        cluster_points[point.label].append(point)
    k_cluster = ClusterSet()
    for k_loop in range(k):
        k_cluster.add(Cluster(cluster_points[k_loop]))
    return k_cluster.medoids()
    ### ========== TODO : END ========== ###


def kMeans(points, k, init='random', plot=False) :
    """
    Cluster points into k clusters using variations of k-means algorithm.
    
    Parameters
    --------------------
        points  -- list of Points, dataset
        k       -- int, number of clusters
        average -- method of ClusterSet
                   determines how to calculate average of points in cluster
                   allowable: ClusterSet.centroids, ClusterSet.medoids
        init    -- string, method of initialization
                   allowable: 
                       'cheat'  -- use cheat_init to initialize clusters
                       'random' -- use random_init to initialize clusters
        plot    -- bool, True to plot clusters with corresponding averages
                         for each iteration of algorithm
    
    Returns
    --------------------
        k_clusters -- ClusterSet, k clusters
    """
    
    ### ========== TODO : START ========== ###
    # part 2c: implement
    # Hints:
    #   (1) On each iteration, keep track of the new cluster assignments
    #       in a separate data structure. Then use these assignments to create
    #       a new ClusterSet object and update the centroids.
    #   (2) Repeat until the clustering no longer changes.
    #   (3) To plot, use plot_clusters(...).

    #select the way to initialize
    if init == 'random':
        initial_points = random_init(points,k=k)

    elif init == 'cheat':
        initial_points = cheat_init(points)
    k_clusters = ClusterSet()
    for loop in range(100):
        k_clusters_original = k_clusters
        #create K initial clusters
        points_set=[]
        for k_loop in range(k):
            points_set.append([])

        #classify each point into the corresponding cluster
        for point in points:
            k_point = 0
            min_distance = point.distance(initial_points[0])
            for k_loop in range(1,k):
                distance = point.distance(initial_points[k_loop])

                if distance<min_distance:
                    k_point = k_loop
                    min_distance = distance
            points_set[k_point].append(point)
        k_clusters = ClusterSet()

        for k_loop in range(k):
            k_clusters.add(Cluster(points_set[k_loop]))
        if plot :
            plot_clusters(k_clusters,'N=3, points=20, KCentroid', ClusterSet.centroids)

        initial_points = k_clusters.centroids()
        if k_clusters.equivalent(k_clusters_original):
            break
    return k_clusters.score()
    ### ========== TODO : END ========== ###


def kMedoids(points, k, init='random', plot=False) :
    """
    Cluster points in k clusters using k-medoids clustering.
    See kMeans(...).
    """
    ### ========== TODO : START ========== ###
    # part 2e: implement
    if init == 'random':
        initial_points = random_init(points,k)
    elif init == 'cheat':
        initial_points = cheat_init(points)
    k_clusters = ClusterSet()
    for loop in range(100):
        k_clusters_original = k_clusters
        #create K initial clusters
        points_set=[]
        for k_loop in range(k):
            points_set.append([])

        #classify each point into the corresponding cluster
        for point in points:
            k_point = 0
            min_distance = point.distance(initial_points[0])
            for k_loop in range(1,k):
                distance = point.distance(initial_points[k_loop])
                if distance<min_distance:
                    k_point = k_loop
                    min_distance = distance
            points_set[k_point].append(point)
        k_clusters = ClusterSet()
        for k_loop in range(k):
            k_clusters.add(Cluster(points_set[k_loop]))
        if plot :
            plot_clusters(k_clusters,'N=3, points=20, KMedoid', ClusterSet.medoids)
        initial_points = k_clusters.medoids()


        if k_clusters.equivalent(k_clusters_original):
            break
    return k_clusters.score()
    ### ========== TODO : END ========== ###


######################################################################
# main
######################################################################

def main() :
    ### ========== TODO : START ========== ###
    # part 1: explore LFW data set
    # part 1a:

    X,y = get_lfw_data()
    size = (50,37)
    y_range=[]
    for y_ in y:
        if y_ not in y_range:
            y_range.append(y_)
    print y_range
    """
    show_image(X[0],size)
    print y[0]
    show_image(X[1], size)
    print y[1]
    show_image(X[2], size)
    print y[2]
    show_image(X[4], size)
    print y[4]
"""
    average = 0
    for i in range(0,1508):
        average += X[i]
    average = average/1508.0
    show_image(average,size)
    # part 1b:
    U, mu = PCA(X)
    plot_gallery([vec_to_image(U[:, i]) for i in xrange(12)])
    # part 1c:
    l_range=[1,10,50,100,500,1288]
    for l in l_range:
        Z, Ul = apply_PCA_from_Eig(X,U,l,mu)
        X_rec = reconstruct_from_PCA(Z,Ul,mu)
        #plot_gallery([X_rec[i] for i in xrange(12)])
    ### ========== TODO : END ========== ###

    
    
    ### ========== TODO : START ========== ###
    # part 2d-2f: cluster toy dataset
    np.random.seed(1234)
    points = generate_points_2d(20)
    #kMeans(points,3,plot = True)
    #kMedoids(points,3, plot = True)
    #kMeans(points,3,init='cheat', plot = True)
    #kMedoids(points,3, init='cheat', plot = True)

    ### ========== TODO : END ========== ###
    
    
    """
    ### ========== TODO : START ========== ###    
    # part 3a: cluster faces
    np.random.seed(1234)
    X1, y1 = util.limit_pics(X, y, [2,3,6,8], 40)
    points = build_face_image_points(X1, y1)

    plot = {}
    for pt in points:
        if pt.label not in plot:
            plot[pt.label] = []
        plot[pt.label].append(pt)
    clusters = ClusterSet()
    for l in plot:
        clusters.add(Cluster(plot[l]))
    plot_clusters(clusters, 'orig', ClusterSet.centroids)
    print "start"
    # faces kMeans cluster
    score = kMeans(points,k=4)
    max = score
    min = score
    average = score
    for i in range(9):
        score = kMeans(points, k=4)
        average = average + score
        if score>max:
            max = score
        if score<min:
            min = score
    print "KMeans:"
    print "average:"
    print average/10.0
    print "max"
    print max
    print "min"
    print min
    print "start"
    score = kMedoids(points, k=4)
    max = score
    min = score
    average = score
    for i in range(9):
        score = kMedoids(points, k=4)
        average = average + score
        if score > max:
            max = score
        if score < min:
            min = score
    print "KMedoids"
    print "average:"
    print average / 10.0
    print "max"
    print max
    print "min"
    print min


    # part 3b: explore effect of lower-dimensional representations on clustering performance
    np.random.seed(1234)
    X1, y1 = util.limit_pics(X, y, [2, 8], 40)
    U, mu = PCA(X)
    l = 1
    l_range = []
    kMeans_score = []
    kMedoids_score = []
    while l <= 41:
        l_range.append(l)
        Z, Ul = apply_PCA_from_Eig(X1, U, l, mu)
        points = build_face_image_points(Z, y1)
        kMeans_score.append(kMeans(points, 2, init='cheat'))
        kMedoids_score.append(kMedoids(points, 2, init='cheat'))
        l = l + 2
    mean_scatter = plt.scatter(l_range, kMeans_score,c='b', s=20)
    medoid_scatter = plt.scatter(l_range,kMedoids_score,c='r',s=20)
    plt.legend((mean_scatter,medoid_scatter),('kMeans', 'kMedoids'))
    plt.show()
    #X_rec = reconstruct_from_PCA(Z, Ul, mu)
"""
    # part 3c: determine ``most discriminative'' and ``least discriminative'' pairs of images
    np.random.seed(1234)
    best_pair = []
    poorest_pair = []
    best_score = 0
    poorest_score = 100
    l=30
    for person1 in range(12):
        for person2 in range(person1+1,12):
            X1, y1 = util.limit_pics(X, y, [person1, person2], 40)
            U, mu = PCA(X)
            Z, Ul = apply_PCA_from_Eig(X1, U, l, mu)
            points = build_face_image_points(Z, y1)
            score = kMedoids(points, 2)
            if score>best_score:
                best_score=score
                best_pair = [person1, person2]
            if score<poorest_score:
                poorest_score = score
                poorest_pair = [person1, person2]
    print best_pair
    print best_score
    plot_representative_images(X,y,best_pair,title='The most distinguished two persons')
    print poorest_pair
    print poorest_score
    plot_representative_images(X, y, poorest_pair, title='The most undistinguished two persons')

    
    ### ========== TODO : END ========== ###


if __name__ == "__main__" :
    main()
