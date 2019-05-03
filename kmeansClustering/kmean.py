import random

# Selectis the first k points from the data set as starting centers.
def init_centers_first_k(data_set, k):
    centers = []
    for i in range(k):
        centers.append(data_set[i]['vals'])
    return centers


# Selects k points randomly from the data set as starting centers.
def init_centers_random(data_set, k):
    
    centers = random.sample(data_set,k)
    for i in range(len(centers)):
        centers[i] = centers[i]['vals']
    return centers


# computes the euclidean distance from a data point to the center of a cluster
def dist(vals, center):
    d = 0.0
    for  i in range(len(vals)):
        d += (vals[i]-center[i])**2
    d = d**.5
    return d


# returns the index of the nearest cluster
def get_nearest_center(vals, centers):
    c_idx = 0
    min_dist = 9999999 # ridiculously large number so the next is guaranteed to be lower
    for j in range(len(centers)):
        current_dist = dist(vals,centers[j])
        if current_dist < min_dist:
            min_dist = current_dist
            c_idx = j
    return c_idx


# computes element-wise addition of two vectors.
def vect_add(x, y):
    s = [0]*len(x)
    for i in range(len(x)):
        s[i] = x[i] + y[i]
    return s


# averaging n vectors.
def vect_avg(s, n):
    avg = []
    for i in range(len(s)):
        avg.append(float(s[i])/n)
    return avg


# returns the updated centers.
def recalculate_centers(clusters):
    centers = []
    for cluster in clusters:
        vect_sum = [0]*len(cluster[0]['vals'])
        for data_point in cluster:
            vect_sum = vect_add(data_point['vals'],vect_sum)
        center = vect_avg(vect_sum,len(cluster))
        centers.append(center)
    return centers


# run kmean algorithm on data set until convergence or iteration limit.
def train_kmean(data_set, centers, iter_limit):
    clusters = [[] for x in range(len(centers))]
    newcenters = []
    num_iterations = 0
    while (num_iterations <= iter_limit):
        for i in range(len(data_set)):
            index = get_nearest_center(data_set[i]['vals'],centers)
            clusters[index].append(data_set[i])
        num_iterations += 1
        recalculated_centers = recalculate_centers(clusters)
        if newcenters.sort() == recalculated_centers.sort():
            break
        else:
            centers = recalculated_centers
    return centers, clusters, num_iterations


# helper function: compute within group sum of squares
def within_group_ss(cluster, center):
    ss = 0.0
    for i in range(len(cluster)):
        #ss = (dist(cluster[i]['vals'],center))**2
        for j in range(len(center)):
            ss += (cluster[i]['vals'][j]-center[j])**2
    return ss


# compute sum of within group sum of squares
def sum_of_within_group_ss(clusters, centers):
    sss = 0.0
    for i in range(len(clusters)):
        sss += within_group_ss(clusters[i],centers[i])
    return sss
