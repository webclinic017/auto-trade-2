# tensorflow v1
import tensorflow as tf
# tensorflow v2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_eager_execution()

a = tf.Variable(1.0 ,name='a')
loss = a - 1
opt = tf.train.GradientDescentOptimizer(0.1)
g = tf.get_default_graph()
print(g.get_operations())
grad = opt.compute_gradients(loss)
print(g.get_operations())
train_op = opt.apply_gradients(grad)
print(g.get_operations())
tf.summary.FileWriter("logs", g).close()