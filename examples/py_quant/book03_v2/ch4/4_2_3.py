# tensorflow v1
import tensorflow as tf
# tensorflow v2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_eager_execution()

a = tf.compat.v1.get_variable('a',1)
b = tf.compat.v1.get_variable('b',2)
c = a + b
g = tf.compat.v1.get_default_graph()
print(g.get_operations()[-1])