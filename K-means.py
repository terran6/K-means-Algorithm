from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random
import math
import pdb



def k_means(P, k):

    iter_num = 1
    colors = []
    P = np.array(P)
    centroids = []
    new_centroids = []
    assignments = defaultdict(list)
    
    #set boundaries for random centroids
    max_x = np.max(P, axis = 0)[0]
    min_x = np.min(P, axis = 0)[0]
    max_y = np.max(P, axis = 0)[1]
    min_y = np.min(P, axis = 0)[1]

    #create array of distinct colors for k clusters
    rainbow = cm.get_cmap('rainbow')
    colors = rainbow(np.linspace(0, 1, k))
    
    #if k is equal to or larger than the number of points available, make each point it's own cluster
    if len(P) <= k:
        print("Each point is assigned it's own cluster due to k being equal to or greater than the number of points available!")
        
        for x, y in P:
            assignments[(x, y)].append((x, y))

        plot(assignments, len(P), colors, iter_num)
        return assignments, P

    #ensure that the number of clusters is equal to k
    #sometimes, a centroid is not assigned a single point based on other centroids being better suitors
    while len(assignments) != k:
    
        #create original randomized centroids
        for i in range(0,k):
            new_centroid = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
            centroids.append(new_centroid)  
        
        new_centroids = []
        #update centroid location based on points until centroids are unable to move to better coordinates
        while set(centroids) != set(new_centroids):
            if new_centroids:
                centroids = new_centroids

            new_centroids = []
            assignments = defaultdict(list)

            #calculate distances between each point and each centroid to assign points to their closes centroid
            for x, y in P:
                distances = {}
                for p, q in centroids:
                    euclidean_distance = math.sqrt((x - p)**2 + (y - q)**2)
                    distances[(p,q)] = euclidean_distance
                #assign each point to its closest centroid
                assignments[min(distances, key = distances.get)].append((x,y))  

            #plot update if k value is satisfied, otherwise, reassign original centroids to ensure k value is met
            if len(assignments) == k:
                plot(assignments, k, colors, iter_num)
                iter_num += 1
            
            else:
                break

            #update centroid values based on the mean coordinates of their assigned points
            for val in assignments.values():
                val = np.array(val)
                new_cent = (np.mean(val, axis = 0)[0], np.mean(val, axis = 0)[1])
                new_centroids.append(new_cent)           
                
    return assignments, centroids

 

def plot(assignments, k, colors, iter_num):

    color_num = 0
    for key, val in assignments.items():
        val = np.array(val)
        key = np.array(key)

        x = val[:, 0]
        y = val[:, 1]

        p = key[0]
        q = key[1]

        plt.scatter(x, y, c = [colors[color_num]], edgecolors = 'k')
        plt.scatter(p,q, c = 'k', marker = 'x')
        plt.title('K-means : Iteration {}'.format(iter_num))

        color_num += 1

    plt.show(block = True)

       

def print_info(assignments, k):
    print("\n\033[93mThe initialized points were assigned to the {} clusters as follows:\033[00m\n".format(k))
    print("\t\033[90mcluster_id\tpoints\033[00m\n")
    for i, val in enumerate(list(assignments.values())):
        print("\t{}\t\t{}\n".format(i, str(val).strip('[]')))
    print("\n\033[93mThe coordinates for the {} centroids were as follows:\033[00m\n".format(k))
    print("\t\033[90mcluster_id\tcentroid_coordinates\033[00m\n")
    for i, centroid in enumerate(list(assignments.keys())):
        print("\t{}\t\t{}\n".format(i, centroid))



if __name__ == '__main__':
    
    #Initialize the integer number of clusters desired, k
    k = 4
    
    #Initialize coordinates of all points to take part in K-means clustering
    P = [(1,2), (2,3), (94, 10), (500, 6), (4, -1), (80, 4), (81,4), (-100, 1), (-99,1)]

    assignments, centroids = k_means(P, k)

    print_info(assignments, k)