import tensorflow as tf
from sklearn.model_selection import KFold
import pandas as pd
import matplotlib.pyplot as plt

def softmax_function(x_train,y_train,x_test,y_test):
    loss_list = []
    x = tf.placeholder(tf.float32,shape = (None,4))
    y = tf.placeholder(tf.float32,shape = (None,3)) #predict
    #用softmax 构建模型
    w = tf.Variable(tf.zeros([4,3]))
    b = tf.Variable(tf.zeros([3]))
    pred = tf.nn.softmax(tf.matmul(x,w)+b)
    #损失函数（交叉熵）
    with tf.name_scope('loss'):
        loss = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred),1))
        tf.summary.scalar('loss',loss)
    #梯度下降
    optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)
    #准确率
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1)), tf.float32))

    #加载session 图
    with tf.Session() as sess:
        #初始化所有变量
        init = tf.global_variables_initializer()
        sess.run(init)
        #开始训练
        for epoch in range(5000):
            sess.run(optimizer,feed_dict={x:x_train,y:y_train})
            loss_list.append(sess.run(loss,feed_dict={x:x_train,y:y_train}))

        print('train accuracy:',sess.run(accuracy,feed_dict={x:x_train,y:y_train}))
        print('test accuracy:',sess.run(accuracy,feed_dict={x:x_test,y:y_test}))
        return (loss_list)


if __name__ == '__main__':
    data = pd.read_csv('iris.txt', header=None)
    dummies = pd.get_dummies(data[4])
    data.drop(4, axis=1, inplace=True)
    data = data.join(dummies)
    data = data.values
    X = data[:, :-3]
    Y = data[:, -3:]
    KF = KFold(n_splits=5)
    i = 1
    for train_index, test_index in KF.split(X):
        print('for %d fold' % i)
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        loss_list = softmax_function(X_train,Y_train,X_test,Y_test)
        plt.figure()
        plt.plot(range(5000),loss_list)
        plt.title('%d fold loss'%i)
        plt.xlabel('iter times')
        plt.ylabel('loss')
        plt.savefig("%s -fold loss fig.png"%i)
        i += 1