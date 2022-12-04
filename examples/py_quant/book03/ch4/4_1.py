import numpy as np
# tensorflow v1
import tensorflow as tf
# tensorflow v2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_eager_execution()

data_x = np.array([[0,0],[0,1],[1,0],[1,1]], dtype=np.float32)
data_y = np.array([[0],[1],[1],[0]], dtype=np.float32)

x = tf.placeholder(tf.float32, shape=[None, 2], name='input')
w1 = tf.Variable(tf.random_uniform([2,4], -1, 1), name='w1')
b1 = tf.Variable(tf.zeros(4, dtype=np.float32), name='b1')
# tensorflow v1
w2 = tf.get_variable('w2', shape=[4,1], initializer=tf.contrib.layers.xavier_initializer())
# tensorflow v2
# w2 = tf.get_variable('w2', shape=[4,1], initializer=tf.initializers.GlorotUniform()) # 0r
# w2 = tf.get_variable('w2', shape=[4,1], initializer=tf.keras.initializers.glorot_normal())
b2 = tf.get_variable('b2', initializer=tf.constant(0.0))
z1 = tf.sigmoid(tf.matmul(x, w1) + b1)
z2 = tf.sigmoid(tf.matmul(z1, w2) + b2)
y = tf.placeholder(tf.float32, shape=[None, 1], name='output')
loss = tf.nn.l2_loss(z2 - y )
opt = tf.train.GradientDescentOptimizer(0.05)
train_op = opt.minimize(loss)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for iter in range(100000):
        loss_val, _ = sess.run([loss, train_op], feed_dict={x:data_x, y:data_y})
        if iter % 10000 == 0:
            print('{}:loss={}'.format(iter, loss_val))
    graph = tf.get_default_graph()
    print(graph.get_operations())