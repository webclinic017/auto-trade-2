# tensorflow v1
import tensorflow as tf
# tensorflow v2
# import tensorflow.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()
tf.compat.v1.disable_eager_execution()
import numpy as np
import sys

def wrong1():
    with tf.compat.v1.name_scope('normal'):
        x = tf.compat.v1.placeholder(tf.float32, [],'x')
        a = tf.Variable(0.0, 'a')
        c = tf.random.uniform([], 0.0, 1.0)
        op = a.assign(c)
        with tf.control_dependencies([op]):
            f = a * x
            g = tf.gradients(ys=f, xs=x)
    with tf.compat.v1.Session() as s:
        s.run(tf.compat.v1.global_variables_initializer())
        print(s.run([f,g], feed_dict={x:1}))

def wrong2():
    with tf.compat.v1.name_scope('normal'):
        x = tf.compat.v1.placeholder(tf.float32, [],'a')
        a = tf.Variable(0.0, 'w')
        c = tf.random.uniform([], 0.0, 1.0)
        op = a.assign(c)
        c2 = tf.random.uniform([], 0.0, 1.0)
        op2 = a.assign(c2)
        with tf.control_dependencies([op]):
            f = a * x
            with tf.control_dependencies([op2]):
                g = tf.gradients(ys=f, xs=x)
    with tf.compat.v1.Session() as s:
        s.run(tf.compat.v1.global_variables_initializer())
        print(s.run([f, g], feed_dict={x: 1}))

def right1():
    with tf.compat.v1.name_scope('normal'):
        x = tf.compat.v1.placeholder(tf.float32, [],'a')
        a1 = tf.random.uniform([], 0.0, 1.0)
        a2 = tf.random.uniform([], 0.0, 1.0)
        f1 = a1 * x
        f2 = a2 * x
        f = f2 + tf.stop_gradient(f1 - f2)
        g = tf.gradients(ys=f, xs=x)
    with tf.compat.v1.Session() as s:
        s.run(tf.compat.v1.global_variables_initializer())
        print(s.run([f, g], feed_dict={x: 1}))

def right2():
    @tf.RegisterGradient("mult_grad")
    def _mult_grad(op, grad):
        c2 = np.random.uniform(0.0, 1.0)
        return  op.inputs[1] * grad, c2 * grad

    g = tf.compat.v1.get_default_graph()
    x = tf.compat.v1.placeholder(tf.float32, [])
    a = tf.random.uniform([], 0.0, 1.0)
    with g.gradient_override_map({"Mul":"mult_grad"}):
        f = tf.multiply(a, x)
        g = tf.gradients(ys=f, xs=x)
    with tf.compat.v1.Session() as s:
        s.run(tf.compat.v1.global_variables_initializer())
        print(s.run([f, g], feed_dict={x: 1}))

if __name__ == '__main__':
    if sys.argv[1] == '1':
        wrong1()
    elif sys.argv[1] == '2':
        wrong2()
    elif sys.argv[1] == '3':
        right1()
    elif sys.argv[1] == '4':
        right2()