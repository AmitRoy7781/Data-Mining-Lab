from MixedDistance import *
import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import statistics
import time


PLOT_FLAG = 0

K_VECTOR = []
COST_VECTOR = []
RUNTIME_VECTOR = []
PURITY_VECTOR = []
SILHOUTTE_VECTOR = []




def getCenter(data,type,order):

    if type=="Numeric": #mean for numeric
        if(len(data)>0):
            return statistics.mean(data)
        return 0

    elif type=="Nominal": #mode for nominal
        return max(data,key=data.count)

    elif type=="Binary": #mode for binary
        return max(data, key=data.count)

    elif type=="Ordinal": #median for ordinal
        encoded_data = []
        for x in data:
            for o in range(len(order)):
                if x==order[o]:
                    encoded_data.append(o)
                    break
        return order[int(statistics.median(encoded_data))]




print("\n\n\t\t K-Means Clustering Algorithm\n\n")

data, types, info, order_info,has_class,class_map,d,dataset = readFile()
n = len(data)
if d<3:
    PLOT_FLAG = 1
else:
    PLOT_FLAG = 0
data = copy.deepcopy(data)

print("Enter l: ",end="")
l = int(input())
print("Enter r: ",end="")
r = int(input())
for k in range(l,r+1):
    K_VECTOR.append(k)

    clusters = random.sample([data[i] for i in range(len(data))], k=k)
    # clusters = [data[0], data[133], data[112], data[94]]
    cluster_id = [None for i in range(len(data))]

    st = time.time()

    while True:
        clusters_p = copy.deepcopy(clusters)
        for i in range(len(data)):
            for c in range(len(clusters)):
                distance = dis(data[i],clusters[c],types,info,order_info)
                if cluster_id[i] is None:
                    cluster_id[i] = (c, distance)
                elif distance < cluster_id[i][1]:
                    cluster_id[i] = (c, distance)

        # temp = [[0.0 for j in range(len(data[0]))] for i in range(k)]
        # count = [0 for i in range(k)]


        # for i in range(len(data)):
        #     count[cluster_id[i][0]] += 1
        #     for j in range(len(data[i])):
        #         temp[cluster_id[i][0]][j] += data[i][j]

        # for i in range(k):
        #     for j in range(len(temp[i])):
        #         temp[i][j] /= count[i]
        #     clusters[i] = np.array(temp[i])


        #temp[i][j] contains all types of value present
        # in the jth attribute of the objects of ith cluster

        temp = {}
        for i in range(k):
            temp[i] = {}
            for j in range(len(data[0])):
                temp[i][j] = []

        for i in range(len(data)):
            for j in range(len(data[i])):
                temp[cluster_id[i][0]][j].append(data[i][j])

        for i in range(k):
            center_list = []
            for j in temp[i]:
                center = getCenter(temp[i][j],types[j],order_info[j])
                center_list.append(center)
            clusters[i] = np.array(center_list)


        cost = 0.0
        for i in range(len(data)):
            distance = dis(data[i],clusters[cluster_id[i][0]],types,info,order_info)
            cost += distance


        # print("Within Cluster Variation:",cost)

        eq = True
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                if clusters_p[i][j] != clusters[i][j]:
                    eq = False
        if eq:

            COST_VECTOR.append(cost)
            print("Within Cluster Variation:", cost)

            break


    en = time.time()

    print("Runtime: ", en-st)
    RUNTIME_VECTOR.append(en-st)

    final_clusters = {}
    for x in cluster_id:
        final_clusters[x[0]] = []

    for obj in range(0,len(data)):
        leader = cluster_id[obj][0]
        final_clusters[leader].append(obj)

    if has_class:
        purity = calculate_purity(final_clusters,n,class_map)
        print("Purity:",purity)
        PURITY_VECTOR.append(purity)

    silhouette_coeff = 0
    for obj in range(n):
        silhouette_coeff += calculate_silhouette_coefficient(data,final_clusters, obj, types, info, order_info)
    silhouette_coeff /= n

    SILHOUTTE_VECTOR.append(silhouette_coeff)

    for leader in final_clusters.keys():
        # print("Cluster: ", leader+1)
        members = final_clusters[leader]
        #
        # for member in members:
        #     # print(data[member],end=" ")
        #     print(member, end=" ")
        # print("")

        if PLOT_FLAG == 1:

            cluster_member = []

            for member in members:
                cluster_member.append(data[member])


            cluster_member = np.array(cluster_member)
            x,y = cluster_member.T
            plt.scatter(x,y)

    if PLOT_FLAG == 1:
        plt.suptitle("K-means algorithm Visualization")
        plt.title("Dataset Name: " + dataset)
        plt.show()
        print("Converged")

print("K: ")
for k in K_VECTOR:
    print(k)

print("Runtime: ")
for runtime in RUNTIME_VECTOR:
    print(runtime)

print("Purity: ")
for purity in PURITY_VECTOR:
    print(purity)

print("Silhouette Coefficient: ")
for coeff in SILHOUTTE_VECTOR:
    print(coeff)

print("COST:(WCV)")
for wcv in COST_VECTOR:
    print(wcv)