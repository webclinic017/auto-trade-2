# tensorflow v1
import tensorflow as tf
# tensorflow v2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_eager_execution()

a = tf.constant(1.0)
b = tf.constant(1.0)
c = a + b
g = tf.compat.v1.get_default_graph()
print(g.get_operations())
grad = tf.gradients(ys=c, xs=[a,b])
print(g.get_operations())
tf.compat.v1.summary.FileWriter("logs", g).close()