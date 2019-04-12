import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

data = pd.read_excel("distances.xlsx")
D = data.values #df转化成matrix
N = D.shape[0]
T = np.zeros((N,N))
dis_line = np.zeros((N,1))
dis_line = np.sum(np.multiply(D,D),axis = 0)
dis_sum = np.sum(dis_line)

for i in range(N):
    for j in range(N):
        T[i][j] = -0.5*(D[i][j]**2 - 1/N*dis_line[i] + 1/(N*N)*dis_sum)
eigVal,eigVec = np.linalg.eig(T)
#取最大的两个特征值
eigValSorted_indices = np.argsort(eigVal)
#提取d个最大特征向量
topd_eigVec = eigVec[:,eigValSorted_indices[:-2-1:-1]] #-d-1前加:才能向左切
X = np.dot(topd_eigVec, np.diag(eigVal[eigValSorted_indices[:-2-1:-1]]))
for i in range(10):
    X[i,1] = -X[i,1]

plt.figure()
plt.scatter(X[:,0],X[:,1])
#name = ['BJ','SH','WH','YZ','NJ',"CD","XA",'SZ',"DL","GZ"]
name = ['北京','上海','武汉','扬州','南京',"成都","西安",'深圳',"大连","广州"]
for i in range(10):
    plt.annotate(s = name[i],xy = (X[:,0][i], X[:,1][i]+1000))
plt.xticks([])
plt.yticks([])
plt.savefig('城市分布图.jpg')
plt.show()

#显示对比图

img = plt.imread("城市对比图.png")
plt.imshow(img)