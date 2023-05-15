import numpy as np
import adaboost as ada

X = [[-2,-2],[-3,-2],[-2,-3],[-1,-1],[-1,0],[0,-1],[1,1],[1,0],[0,1],[2,2],[3,2],[2,3]]
Y=[-1,-1,-1,1,1,1,-1,-1,-1,1,1,1]
f, alpha = ada.adaboost_train(X,Y,5)
acc = ada.adaboost_test(X,Y,f,alpha)
print("Accuracy:", acc)