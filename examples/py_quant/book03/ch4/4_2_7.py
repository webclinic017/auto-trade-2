# tensorflow v1
import tensorflow as tf
# tensorflow v2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_eager_execution()

add_arg_scope = tf.contrib.framework.add_arg_scope
arg_scope = tf.contrib.framework.arg_scope


@add_arg_scope
def func1(*args, **kwargs):
    return (args, kwargs)

with arg_scope((func1,), a=1, b=None, c=[1]):
    args, kwargs = func1(0)
    print(args)
    print(kwargs)