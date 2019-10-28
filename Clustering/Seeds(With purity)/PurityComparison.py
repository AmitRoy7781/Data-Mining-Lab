from matplotlib import pyplot as plt
import numpy as np


###tobechanged
x = [3,4,5,6,7]
KMeans = [0.6285714286,
0.8952380952,
0.6333333333,
0.8761904762,
0.9047619048]
KMediods = [0.8857142857,
0.9,
0.8904761905,
0.8857142857,
0.8904761905
]
plt_title = "Dataset Name: Seeds"

n_groups = len(x)
fig,ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.2
opacity = 0.8

X = KMeans
Y = KMediods
measure_name = 'Purity'
file_name = 'purity_comparison.png'

rects1 = plt.bar(index, X,bar_width,
alpha=opacity,
color='b',
label='K-Means')

rects2 = plt.bar(index+bar_width, Y,bar_width,
alpha=opacity,
color='r',
label='K-Medoids')

plt.xlabel('k')
plt.ylabel(measure_name)
plt.suptitle('Comparison between K-Means and K-Medoids Algorithm\n')
plt.title(plt_title)

plt.xticks(index+bar_width,tuple(x))
# plt.yticks(index+bar_width,tuple(x))
plt.legend(loc='upper left')

# plt.yscale('log',basey=2)

# plt.tight_layout()
plt.savefig(file_name,dpi=600)


plt.show()
