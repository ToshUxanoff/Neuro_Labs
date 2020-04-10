import math
import matplotlib.pyplot as mplt
from itertools import combinations

boolean_table = [
	(0, 0, 0, 0),
	(0, 0, 0, 1),
	(0, 0, 1, 0),
	(0, 0, 1, 1),
	(0, 1, 0, 0),
	(0, 1, 0, 1),
	(0, 1, 1, 0),
	(0, 1, 1, 1),
	(1, 0, 0, 0),
	(1, 0, 0, 1),
	(1, 0, 1, 0),
	(1, 0, 1, 1),
	(1, 1, 0, 0),
	(1, 1, 0, 1),
	(1, 1, 1, 0),
	(1, 1, 1, 1)
]

class Neuron:
    def __init__(self, func_type):
        self.weights = [0 for i in range(5)]
        self.learning_rate = 0.3
        self.function_type = func_type

    def calc_net(self, input_):
        net = 0
        for i in range(len(input_)):
            net += self.weights[i+1]*input_[i]
        net += self.weights[0]
        return net

    def calc_thr_out(self, net):
        if net >= 0:
            return 1
        return 0

    def calc_sig_out(self, net):
        return (0.5 * ( (net / (1 + abs(net)) + 1) ) )

    def correct_weights(self, delta, input_, multiplier):
        self.weights[0] += self.learning_rate * delta * multiplier
        for i in range(len(input_)):
            deltaweight = self.learning_rate * delta * multiplier * input_[i]
            self.weights[i+1] += deltaweight

    #for correct_weights
    def get_multiplier(self, net):
        if self.function_type == 'threshold':
            return 1
        elif self.function_type == 'sigmoid':
            return 0.5 * ( 1 / (1 + abs(net)**2) )

    def calc_out(self, net):
        out = 0
        if self.function_type == 'threshold':
            out = self.calc_thr_out(net)
        elif self.function_type == 'sigmoid':
            out =self.calc_sig_out(net)
        if out >= 0.5:
            return 1
        else:
            return 0

    def check(self, t_set, quiet = True):
        for vector, ideal_out in t_set.items():
            net = self.calc_net(vector)
            real_out = self.calc_out(net)
            if not quiet:
                print('Vector:', vector,'Neuronet out:', real_out, '\tIdeal out:', ideal_out)
            if real_out != ideal_out:
                if not quiet:
                    print('error')
                return False
        return True

    def train(self, training_set, quiet = False):
        epoch = 0
        errors_data = []
        while True:
            if not quiet:
                print('weights before epoch', epoch, ': ', self.weights)
            summaryError = 0
            results = []
            for vector in training_set.keys():
                net = self.calc_net(vector)
                real_out = self.calc_out(net)
                results.append(real_out)
                delta = training_set[vector] - real_out
                if delta:
                    summaryError += 1
                    multiplier = self.get_multiplier(net)
                    self.correct_weights(delta, vector, multiplier)
            errors_data.append(summaryError)
            if summaryError == 0:
                if not quiet:
                    print_epoch_results(results, epoch, summaryError)
                    print('--Done--')
                return True, errors_data
            if not quiet:
                print_epoch_results(results, epoch, summaryError, self.weights)
            if epoch >= 50:
                print('fail')
                return False, errors_data
            epoch += 1

def print_epoch_results(results, epoch, error, weights = None):
    print('#'*50, '\nEpoch:', epoch, 'Summary error:', error)
    print('results:\n', results, '\n')
    if weights is not None:
        formatted_weights = ['%.7f' % w for w in weights]
        print('Weights (after correct):', formatted_weights)

def inverted(x) :
    return not x
#boolean function defined here
def calculate_training_set():
    result_vector = []
    for vector in boolean_table:
        result = int( (inverted(vector[0]) or inverted(vector[1]) or inverted(vector[2])) and (inverted(vector[1]) or inverted(vector[2]) or vector[3]) ) #by variant
        result_vector.append(result)
    return result_vector

def calc_min_training_set(t_set):
    for i in range(1, 16):
        for sets in combinations(boolean_table, i):
            neuron = Neuron('threshold')
            min_train_set = dict()
            for one_set in sets:
                min_train_set[one_set] = t_set[one_set]
            result, errors_data = neuron.train(min_train_set, quiet = True)
            if result:
                check = neuron.check(t_set)
                if check:
                    print('@'*50, '\nmin set is ', min_train_set)
                    return neuron, errors_data

if __name__ == '__main__':
    t_set = calculate_training_set()

    t_set = dict(zip(boolean_table, t_set))
    print(t_set.items())

    n1  = Neuron('threshold')
    _, errors_n1 = n1.train(t_set)
    n2 = Neuron('sigmoid')
    _, errors_n2 = n2.train(t_set)

    n3 = Neuron('threshold')
    n4, errors_min = calc_min_training_set(t_set)

    mplt.plot(errors_n1, color='g')
    mplt.plot(errors_n2, color='b')
    mplt.plot(errors_min, color='r')

    print(calculate_training_set())
    mplt.show()
