import math
import numpy
import matplotlib.pyplot as mplt

class Neuron:
    weights = [0 for i in range (5)]
    learningRate = 0.8
    p = 4
    
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
    sum = 0
    for i, res in enumerate(results):
        sum += (ideal[i] - res)**2
    return math.sqrt(sum)

def print_epoch_results(results, epoch, error, weights):
    print('-'*50, '\nresults:\n', results, '\n', '-'*50)
    print('Epoch:', epoch, "Summary error:", error)
    print('Weights:', weights)

def train(neuron, trainset):
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
        summaryErr = calc_summary_err(trainset, results)
        print_epoch_results(results, epoch, summaryErr, neuron.weights)
        if epoch > 60000:
         #   return
        #if summaryErr < 0.5:
            print('Done!')
            return
        epoch += 1
    
def predict(neuron, trainset):
    tset = trainset[:]
    i = 16
    while i < 35:
        result = neuron.calc_net(tset[-neuron.p:])
        tset.append(result)
        i += 1
    print('predicted length:', len(tset))
    return tset

def calc_train_set():
    t_set = []
    for t in numpy.arange(0, 4.2, 0.2):
        tmp = 0.5*math.cos(0.5*t)- math.sin(t)
        
        t_set.append(tmp)
    return t_set

def tmp():
    t_set = []
    for t in numpy.arange(0, 8, 0.2):
        tmp = 0.5*math.cos(0.5*t) - math.sin(t)
        
        t_set.append(tmp)
    print('length:', len(t_set))
    return t_set

if __name__ == "__main__":
    n1 = Neuron()
    trainset = calc_train_set()
    train(n1, trainset)
    
    print('ideal:', tmp())
    predicted = predict(n1, trainset)
    print('-'*50,'\npredicted:\n', predicted)
    
    y = [i for i in numpy.arange(0, 8, 0.2)]
    print(len(y))
    x = tmp()
    mplt.plot(y, x, color = 'r')
    x = predicted
    mplt.plot(y, x, color='g')
    mplt.show()
