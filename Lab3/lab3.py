import math

#constanats
RBF_number = 7
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
        #print (input_set, self.c_set)
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

def train(hidden_layer, neuron, training_set):
    print('train')
    epoch = 0
    while True:
        vector_index = 0
        summaryError = 0
        results = []
        for vector in boolean_table:
            hidden_layer_out = []
            for hidden_neuron in hidden_layer:
                hidden_layer_out.append(hidden_neuron.calculate(vector))
            real_out = neuron.calculate_output(hidden_layer_out)
            results.append(real_out)
            delta = training_set[vector_index] - real_out
            if delta:
                summaryError += 1
                neuron.correct_weight(delta, hidden_layer_out)
            vector_index += 1
        if summaryError == 0:
            print_epoch_results(results, epoch, summaryError, neuron.weights)
            print('--Done--')
            return
        print_epoch_results(results, epoch, summaryError, neuron.weights)
        epoch += 1
            
def print_epoch_results(results, epoch, error, weights):
    print('-'*50, '\nresults:\n', results, '\n', '-'*50)
    print('Epoch:', epoch, "Summary error:", error)
    print('Weights:', weights)

def calculate_training_set():
    result_vector = []
    centers = []
    for vector in boolean_table:
        result = int(not ((vector[0] + vector[1])*vector[2] + vector[2]*vector[3]))
        result_vector.append(result)
        if result == 0: #in this case (15 var) zeros > ones (7 vs 9)
            centers.append(vector)
    return result_vector, centers



if __name__ == '__main__':
    training_set, centers = calculate_training_set()
    print(training_set)
    hidden_layer = []
    for i in range(RBF_number):
        rbf_neuron = HiddenNeuron(centers[i])
        hidden_layer.append(rbf_neuron)
        print('Added neuron with :',rbf_neuron.c_set)
    n1 = Neuron()
    train(hidden_layer, n1, training_set)