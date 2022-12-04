import tensorflow as tf
# 网络参数
num_input = 28 # 数据输入的维度
timesteps = 28 # 数据输入的总时长
num_hidden = 128 # 隐含层的维度
num_classes = 10 # 算法最终的输出维度

# placeholder
X = tf.placeholder("float", [None, timesteps, num_input])
Y = tf.placeholder("float", [None, num_classes])

# 定义LSTM之外的全连接层的参数
weights = {
    'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([num_classes]))
}

if False:
    import tensorflow.compat.v1 as tfv1
    tfv1.disable_v2_behavior()
    tfv1.disable_eager_execution()
    rnn = tfv1.nn.rnn_cell
else:
    rnn = tf.contrib.rnn

def RNN(x, weights, biases):
    x = tf.unstack(x, timesteps, 1)
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)
    outputs, states = tf.contrib.rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    return tf.matmul(outputs[-1], weights['out']) + biases['out']