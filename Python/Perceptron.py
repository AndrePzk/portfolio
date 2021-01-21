import numpy as np
from sklearn.datasets import load_iris
from sklearn import metrics


#Custom made perceptron to separate one group of flowers from the others

#Initialization of a random weight

def init() :
    w = np.random.normal(size=2)
    b = 0
    return w, b

def preActivation(features, w, b) :
    return np.dot(features, w) + b

#sigmoid function for the activation of the perceptron

def activation(z) :
    return 1 / (1 + np.exp(-z))

#diminishing the learning rate to get to a minimum

def correction(w, b, a, y) :
    global last_grad, learn_rate
    grad = (a - y)
    if last_grad and (grad * last_grad) < 0 : learn_rate += 1
    corr = grad * 10**(-learn_rate)
    last_grad = grad
    return w - corr * a, b + corr


#beginning of the program

dat, target = load_iris(return_X_y=True)
seuil = 0.001
loss = 1
learn_rate = 1
last_grad = 0
score = 0
w, b = init()
target = (target > 0).astype(int)
target_score = 1

while score < target_score :
    old_score = score
    good = 0
    pred = []

    #Start of the epoch, improvement of the perceptron over the data

    for n in range(len(dat)) :

        features = np.array([dat[n, 0], dat[n, 1]])
        y = target[n]
        z = preActivation(features, w, b)
        a = activation(z)
        if y != np.rint(a) :
            w, b = correction(w, b, a, y)

    #End of the epoch, test of the perceptron over the training data

    for n in range(len(dat)) :

        features = np.array([dat[n, 0], dat[n, 1]])
        y = target[n]

        z = preActivation(features, w, b)
        a = activation(z)
        if y == np.rint(a) : good += 1
        pred.append(np.rint(a))

    score = good/len(dat)
    print(score)
    print(metrics.confusion_matrix(pred, target))

    #re-randomization of the parameters if the function gets stuck in a local minimum

    if old_score == score :
        w, b = init()
        learn_rate = 1

#results

print(w, b)

