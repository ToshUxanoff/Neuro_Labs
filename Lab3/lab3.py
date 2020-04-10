import math
import matplotlib.pyplot as mplt
from itertools import combinations
#constants
RBF_number = 3
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

class HiddenNeuron:
    c_set = ()
    def __init__(self, set_):
        self.c_set = set_
    def calculate(self, input_set):
        result = 0
        sum = 0
        for i in range(0, 4):
            sum += (input_set[i] - self.c_set[i])**2
        result = math.exp(-sum)
        return result


class Neuron:
    weights = [0 for i in range(RBF_number + 1)]
    learningRate = 0.3
    def calculate_output(self, input_list):
        net = 0
        for i in range(len(input_list)):
            net += self.weights[i] * input_list[i]
        net += self.weights[-1]
        if net >= 0:
            return 1
        else:
            return 0

    def correct_weight(self, delta, f):
        self.weights[-1] += self.learningRate * delta
        for j in range(RBF_number):
            deltaw = self.learningRate * delta * f[j]
            self.weights[j] += deltaw

def check(hidden_layer, neuron, training_set, quiet = True):
    for vector, ideal_out in training_set.items():
        hidden_layer_out = []
        for hidden_neuron in hidden_layer:
            hidden_layer_out.append(hidden_neuron.calculate(vector))
        real_out = neuron.calculate_output(hidden_layer_out)
        if not quiet:
            print('Vector:', vector,'Neuronet out:', real_out, '\tIdeal out:', ideal_out)
        if real_out != ideal_out:
            if not quiet:
                print('fail!')
            return False
    return True

def train(hidden_layer, neuron, training_set, quiet = False):
    epoch = 0
    errors_data = []
    while True:
        summaryError = 0
        results = []
        for vector in training_set.keys():
            hidden_layer_out = []
            for hidden_neuron in hidden_layer:
                hidden_layer_out.append(hidden_neuron.calculate(vector))
            real_out = neuron.calculate_output(hidden_layer_out)
            results.append(real_out)
            delta = training_set[vector] - real_out
            if delta:
                summaryError += 1
                neuron.correct_weight(delta, hidden_layer_out)
        errors_data.append(summaryError)
        if summaryError == 0:
            if not quiet:
                print_epoch_results(results, epoch, summaryError, None)
                print('--Done--')
            return True, errors_data
        if not quiet:
            print_epoch_results(results, epoch, summaryError, neuron.weights)
        if epoch > 50:
            print('fail')
            return False, errors_data
        epoch += 1
            
def print_epoch_results(results, epoch, error, weights):
    print('-'*50, '\nresults:\n', results, '\n', '-'*50)
    print('Epoch:', epoch, "Summary error: {:5f}".format (error))
    if weights is not None:
        formatted_weights = ['%.7f' % w for w in weights]
        print('Weights:', formatted_weights)

def inverted(x) :
    return not x

def calculate_training_set():
    result_vector = []
    centers = []
    for vector in boolean_table:
        result = int( (inverted(vector[0]) or inverted(vector[1]) or inverted(vector[2])) and (inverted(vector[1]) or inverted(vector[2]) or vector[3]) ) #by variant
        result_vector.append(result)
        if result == 0: #in this case (13 var) zeros < ones (3 vs 13)
            centers.append(vector)
    return result_vector, centers

def calc_min_training_set(hidden_layer, t_set):
    for i in range(1, 16):
        for sets in combinations(boolean_table, i):
            neuron = Neuron()
            neuron.weights = [0 for i in range(RBF_number + 1)]
            min_train_set = dict()
            for one_set in sets:
                min_train_set[one_set] = t_set[one_set]
            result, errors_data = train(hidden_layer, neuron, min_train_set, quiet=True)
            if result:
                ch = check(hidden_layer, neuron, t_set)
                if ch:
                    print('@'*50, '\nmin set is ', min_train_set)
                    return neuron, errors_data

if __name__ == '__main__':
    training_set, centers = calculate_training_set()
    print(training_set)
    hidden_layer = []
    for i in range(RBF_number):
        rbf_neuron = HiddenNeuron(centers[i])
        hidden_layer.append(rbf_neuron)
        print('Added neuron with :',rbf_neuron.c_set)
    n1 = Neuron()
    training_set = dict(zip(boolean_table, training_set))
    status, errors = train(hidden_layer, n1, training_set)

    mplt.plot(errors, color='g')
    n, errors_min = calc_min_training_set(hidden_layer, training_set)
    mplt.plot(errors_min, color='r')
    mplt.show()
    print('weights:', n.weights)