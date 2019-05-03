from kmean import init_centers_random, init_centers_first_k, train_kmean, sum_of_within_group_ss
from data import load_data
import numpy as np
import matplotlib.pyplot as plt

def main():
    val_names, data_set = load_data()
    iter_limit = 20

    # find the values of sum of within group sum of squares for k = 5, k = 10 and k = 20.
    print "sum of within group sum of suares for k=5,10,20"
    for k in [5, 10, 20]:
        init_centers = init_centers_first_k(data_set, k)
        centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
        print "k =", str(k) + ": " + str(sum_of_within_group_ss(clusters, centers))
    print

    # The number of iterations that k-means ran for a given k.
    print "number of iterations that kmeans ran for given k"
    k = 10
    init_centers = init_centers_first_k(data_set, k)
    centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
    print "k =", str(k) + ", num_iter: " + str(num_iterations)
    print
    country_groups = []
    for cluster in clusters:
        countries = []
        for point in cluster:
            countries.append(point['country'])
        country_groups.append(countries)
    for i in country_groups:
        print(i)
        print

    # A plot of the sum of within group sum of squares versus k for k = 1 - 50.
    # centers are started randomly (choose k points from the dataset at random).
    print "A plot of the sum of within group sum of squares vs k for k in range 1-50"
    kvals = np.arange(1,51,1)
    sssvals = []
    for k in range(1, 51):
        init_centers = init_centers_random(data_set, k)
        centers, clusters, num_iterations = train_kmean(data_set, init_centers, iter_limit)
        print str(k) + ", " + str(sum_of_within_group_ss(clusters, centers))
        sssvals.append(sum_of_within_group_ss(clusters,centers))
    sssvals = np.asarray(sssvals)
    f,ax = plt.subplots()
    plt.plot(kvals,sssvals)
    plt.title("Plot of sss values as a function of k")
    plt.xlabel('k')
    plt.ylabel('sss')
    f.show()
    input('<enter> to exit')

if __name__ == "__main__":
    main()
