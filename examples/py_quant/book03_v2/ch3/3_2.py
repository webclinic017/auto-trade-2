import numpy as np
import matplotlib.pyplot as plt

def gd(x_start, step, g):
    x = x_start
    xarr = [x]
    for i in range(20):
        grad = g(x)
        x -= grad * step
        xarr.append(x.copy())
        print('[ Epoch {0} ] grad = {1}, x = {2}'.format(i, grad, x))
        if sum(abs(grad)) < 1e-6:
            break;
    return x, xarr

def momentum(x_start, step, g, discount = 0.7):   
    x = np.array(x_start, dtype='float64')
    pre_grad = np.zeros_like(x)
    xarr = [x.copy()]
    for i in range(50):
        grad = g(x)
        pre_grad = pre_grad * discount + grad * step
        x -= pre_grad
        xarr.append(x.copy())
      
        print('[ Epoch {0} ] grad = {1}, x = {2}'.format(i, grad, x))
        if sum(abs(grad)) < 1e-6:
            break;
    return x, xarr

def f(x):
    return x[0] * x[0] + 50 * x[1] * x[1]
def g(x):
    return np.array([2 * x[0], 100 * x[1]])
xi = np.linspace(-200,200,1000)
yi = np.linspace(-100,100,1000)
X,Y = np.meshgrid(xi, yi)
Z = X * X + 50 * Y * Y

def contour(X,Y,Z, arr = None):
    plt.figure(figsize=(15,7))
    xx = X.flatten()
    yy = Y.flatten()
    zz = Z.flatten()
    plt.contour(X, Y, Z, colors='black')
    plt.plot(0,0,marker='*')
    if arr is not None:
        arr = np.array(arr)
        for i in range(len(arr) - 1):
            plt.plot(arr[i:i+2,0],arr[i:i+2,1])
    plt.show()

contour(X,Y,Z)

# normal step
res, x_arr = gd([150,75], 0.016, g)
contour(X, Y, Z, x_arr)

# large step
res, x_arr = gd([150,75], 0.019, g)
contour(X, Y, Z, x_arr)

# extreme step
res, x_arr = gd([150,75], 0.02, g)
contour(X, Y, Z, x_arr)

# momentum 
res, x_arr = momentum([150,75], 0.016, g)
contour(X, Y, Z, x_arr)

def nesterov(x_start, step, g, discount = 0.7):   
    x = np.array(x_start, dtype='float64')
    pre_grad = np.zeros_like(x)
    x_arr = [x.copy()]
    for i in range(50):
        x_future = x - step * discount * pre_grad
        grad = g(x_future)
        pre_grad = pre_grad * 0.7 + grad 
        x -= pre_grad * step
        x_arr.append(x.copy())
        
        print('[ Epoch {0} ] grad = {1}, x = {2}'.format(i, grad, x))
        if abs(sum(grad)) < 1e-6:
            break;
    return x, x_arr

res, x_arr = nesterov([150, 75], 0.012, g)
contour(X, Y, Z, x_arr)

