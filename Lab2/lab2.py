import math
import numpy
import matplotlib.pyplot as mplt

class Neuron:
    def __init__(self, lr = 0.5, p = 4):
        self.learningRate = lr
        self.p = p
        self.weights = [0 for i in range (p + 1)]
    
    def calc_net(self, xlist):
        net = 0
        for k in range(len(xlist)):
            net += self.weights[k] * xlist[k]
        net += self.weights[-1]
        return net
        
    def correct_weight(self, delta, x):
        for k in range(len(x)):
            deltaw = self.learningRate * delta * x[k]
            self.weights[k] += deltaw

def calc_summary_err(ideal, results):
    sum_ = 0
    for i, res in enumerate(results):
        sum_ += (ideal[i] - res)**2
    return math.sqrt(sum_)

def print_epoch_results(results, epoch, error, weights):
    formatted_results = ['%.5f' % r for r in results]
    print('-'*50, '\nresults:\n', formatted_results, '\n', '-'*50)
    print('Epoch:', epoch, "Summary error: {:5f}".format (error))
    formatted_weights = ['%.5f' % w for w in weights]
    print('Weights:', formatted_weights)

def train(neuron, trainset, max_epoch = None):
    epoch = 0
    p = neuron.p
    while True:
        summaryErr = 0
        results = []
        for i in range(p, len(trainset)):
            net = neuron.calc_net(trainset[i-p:i]) #result = net
            results.append(net)
            delta = trainset[i] - net 
            if delta:
                neuron.correct_weight(delta, trainset[i-p:i])
                summaryErr += delta **2
        summaryErr = math.sqrt(summaryErr)
        print_epoch_results(results, epoch, summaryErr, neuron.weights)
        if summaryErr < 0.001:
            print('Done!')
            return
        if max_epoch is not None:
            if epoch > max_epoch:
                print('max epoch reached')
                return 
        epoch += 1
    
def predict(neuron, trainset):
    tset = trainset[:]
    i = 20 - neuron.p
    while i < 35:
        result = neuron.calc_net(tset[-neuron.p:])
        tset.append(result)
        i += 1
    return tset

def calc_train_set(a, b):
    t_set = []
    step = 0.2
    for t in numpy.arange(a, b + step, step):
        tmp = 0.5*math.cos(0.5*t)- math.sin(t)
        t_set.append(tmp)
    return t_set

def calc_real_x(a, b):
    t_set = []
    step = 0.2
    for t in numpy.arange(a, 2*b + step, 0.2):
        tmp = 0.5*math.cos(0.5*t) - math.sin(t)
        t_set.append(tmp)
    return t_set

if __name__ == "__main__":
    n1 = Neuron(0.4, 4)
    n2 = Neuron(0.8, 4)
    a = 0
    b = 4
    trainset = calc_train_set(a, b)
    train(n1, trainset, 2000)
    train(n2, trainset, 5000)

    predicted = predict(n1, trainset)
    predicted2 = predict(n2, trainset)
    print('-'*50,'\npredicted:\n', predicted)
    
    mplt.plot(calc_real_x(a, b), color = 'r')
    mplt.plot(predicted, color='g')
    mplt.plot(predicted2, color = 'b')
    mplt.show()
