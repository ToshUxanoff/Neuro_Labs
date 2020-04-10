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
    for i, res in zip(ideal, results):
        try:
            sum_ += (i - res)**2
        except OverflowError as e:
            print('Overflow!', e)
    return math.sqrt(sum_)

def print_epoch_results(results, epoch, error, weights):
    formatted_results = ['%.5f' % r for r in results]
    print('-'*50, '\nresults:\n', formatted_results, '\n', '-'*50)
    print('Epoch:', epoch, "Summary error: {:5f}".format (error))
    formatted_weights = ['%.5f' % w for w in weights]
    print('Weights:', formatted_weights)

def train(neuron, trainset, max_epoch = None, quiet = False):
    epoch = 0
    p = neuron.p
    error_list = []
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
        if not quiet:
            print_epoch_results(results, epoch, summaryErr, neuron.weights)
        if summaryErr < 0.001:
            if not quiet:
                print('Done! Summary error less than 0.001')
            return summaryErr
        if max_epoch is not None:
            if epoch > max_epoch:
                return summaryErr
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
    step = 0.05
    for t in numpy.arange(a, b + step, step):
        tmp = math.sin((0.1*t**3) - (0.2*t**2) + t - 1)

        t_set.append(tmp)
    return t_set
        
if __name__ == "__main__":
    n1 = Neuron(0.4, 2)
    n2 = Neuron(0.4, 10)
    a = 0
    b = 1
    trainset = calc_train_set(a, b)
   
    err1 = train(n1, trainset, 5000)
    err2 = train(n2, trainset, 5000)
    
    predicted = predict(n1, trainset)
    predicted2 = predict(n2, trainset)
    print('Summary error 1st neuron:', err1, '\t\tSummary error 2nd neuron:', err2)
    print(err1, err2)
    mplt.plot(calc_train_set(a, 2*b), color = 'r') #ideal
    mplt.plot(predicted, color='g') 
    mplt.plot(predicted2, color = 'b')
    mplt.show()

    ideal = calc_train_set(1, 1.8)
    errors_by_norm = []
    for i in numpy.arange(0.1, 1.1, 0.1):
        n = Neuron(i, 4)
        train(n, trainset, 3000, quiet = True)
        pred = predict(n, trainset)[20:]
        err = calc_summary_err(ideal, pred)
        errors_by_norm.append(err)
    
    mplt.plot(numpy.arange(0.1, 1.1, 0.1), errors_by_norm, color='g')
    mplt.show()

    errors_by_window_width = []
    for i in numpy.arange(1, 15, 2):
        n = Neuron(0.4, i)
        train(n, trainset, 3000, quiet = False)
        pred = predict(n, trainset)[20:]
        err = calc_summary_err(ideal, pred)
        errors_by_window_width.append(err)
    
    mplt.plot(range(1,15,2), errors_by_window_width, color='b')
    mplt.show()
    
    errors_by_epoch = []
    for i in numpy.arange(500, 10000, 100):
        n = Neuron(0.4, 4)
        train(n, trainset, i, quiet = True)
        pred = predict(n, trainset)[20:]
        err = calc_summary_err(ideal, pred)
        errors_by_epoch.append(err)

    mplt.plot(range(500, 10000, 100), errors_by_epoch, color='r')
    mplt.show()
