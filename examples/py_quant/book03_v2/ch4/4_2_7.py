# tensorflow v1
import tensorflow as tf
import tensorflow.compat.v1 as tfv1
tfv1.disable_v2_behavior()

# tensorflow v2
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_eager_execution()

# tfv1
add_arg_scope = tfv1.contrib.framework.add_arg_scope
arg_scope = tfv1.contrib.framework.arg_scope

# tf v2 暂时不支持 add_arg_scope arg_scope
# add_arg_scope = tfv1.layers.add_arg_scope
# arg_scope = tfv1.layers.arg_scope


@add_arg_scope
def func1(*args, **kwargs):
    return (args, kwargs)

with arg_scope((func1,), a=1, b=None, c=[1]):
    args, kwargs = func1(0)
    print(args)
    print(kwargs)