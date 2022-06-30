import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

x = sp.Symbol('x')
f = sp.sin(x) / x

limit = sp.limit(f, x, 'oo')

print(f'limit {f} : {limit} ')

x1 = np.arange(-100, 100, 0.01)
y1 = np.sin(x1) / x1

plt.figure(figsize = (12, 5))
plt.title('y = sin(x) / x')
plt.plot(x1, y1)
plt.show()

# def graph(formula, x_range):  
#     x = np.array(x_range)  
#     y = eval(formula)
#     plt.plot(x, y)  
#     plt.show()

# graph('x**3+2*x-4', range(-10, 11))