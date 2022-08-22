"""
1.11 逻辑回归器的 Python 实现
1.12 优化模型的参数
1.13 评估模型损失
"""

import numpy as np

np.random.seed(1)

# X 矩阵数据
X = np.array(
    [[0,1,0],              
    [1,0,0],              
    [1,1,1],              
    [0,1,1]])

# y 数据
y = np.array([[0,1,1,0]]).T

# 激活函数
def sigmoid(x):    
    return 1/(1+np.exp(-x)) 

# 损失函数
def bce_loss(y,y_hat):    
    N = y.shape[0]    
    loss = -1/N * np.sum((y*np.log(y_hat) + (1 - y)*np.log(1-y_hat)))    
    return loss

W = 2*np.random.random((3,1)) - 1
b = 0

alpha = 1
epochs = 20

N = y.shape[0]
losses = []

for i in range(epochs):   
    # Forward pass    
    z = X.dot(W) + b    
    A = sigmoid(z)    
     
    # Calculate loss    
    loss = bce_loss(y,A)    
    print('Epoch:',i,'Loss:',loss)    
    losses.append(loss)  
     
    # Calculate derivatives    
    dz = (A - y)   
    dW = 1/N * np.dot(X.T,dz)    
    db = 1/N * np.sum(dz,axis=0,keepdims=True)    
    
    # Parameter updates    
    W -= alpha * dW    
    b -= alpha * db

# 上面代码将会获得如下执行结果。

# Epoch: 0 Loss: 0.822322582088
# Epoch: 1 Loss: 0.722897448125
# Epoch: 2 Loss: 0.646837651208
# Epoch: 3 Loss: 0.584116122241
# Epoch: 4 Loss: 0.530908161024
# Epoch: 5 Loss: 0.48523717872
# Epoch: 6 Loss: 0.445747750118
# Epoch: 7 Loss: 0.411391164148
# Epoch: 8 Loss: 0.381326093762
# Epoch: 9 Loss: 0.354869998127
# Epoch: 10 Loss: 0.331466036109
# Epoch: 11 Loss: 0.310657702141
# Epoch: 12 Loss: 0.292068863232
# Epoch: 13 Loss: 0.275387990352
# Epoch: 14 Loss: 0.260355695915
# Epoch: 15 Loss: 0.246754868981
# Epoch: 16 Loss: 0.234402844624
# Epoch: 17 Loss: 0.22314516463
# Epoch: 18 Loss: 0.21285058467
# Epoch: 19 Loss: 0.203407060401

import matplotlib.pyplot as plt

plt.plot(losses)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()
