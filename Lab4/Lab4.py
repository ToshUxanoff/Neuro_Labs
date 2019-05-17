import math

class Neuron:
    learningRate = 0.3
    def __init__(self, weights_):
        self.weights = weights_

    def calc_net(self, input_):
        net = 0
        for i in range(1, len(input_)):
            net += self.weights[i] * input_[i]
        net += self.weights[0]
        return net

    def calc_out(self, net):
        return ((1-math.exp(-net))/(1+math.exp(-net)))

    def correct_weight(self, input_, delta):
        for j in range(len(self.weights)):
            weight = self.weights[j]
            deltaw = self.learningRate * delta * input_[j]
            self.weights[j] = weight + deltaw

class NeuralNet:
    Net = dict() #layer - neurons
    def __init__(self,  N, J , M):
        hidden_layer = []
        for i in range (J):
            hidden_layer.append(Neuron([1 for i in range(N+1)]))
        self.Net[0] = hidden_layer
        output_layer = []
        for i in range(M):
            output_layer.append(Neuron([1 for i in range(J+1)]))
        self.Net[1] = output_layer

    def calc_output(self, input_):
        hl_out = [1]
        for neuron in self.Net[0]:
            net = neuron.calc_net(input_)
            hl_out.append(neuron.calc_out(net))
            print('hl_out debug:', hl_out, net, input_)
        net_output = []
        for out_neuron in self.Net[1]:
            net = out_neuron.calc_net(hl_out)
            net_output.append(out_neuron.calc_out(net))
        
        return net_output, hl_out

    def train(self, input_ ,ideal):
        epoch = 0
        while True:
            summaryErr = 0
            #1st stage
            net_output, hidden_layer_output = self.calc_output(input_)
            
            print('out:', net_output)
            #2nd stage
            delta = ideal[0] - net_output[0]
            if delta:
                summaryErr += delta**2
            out_delta = delta * calc_derivative(net_output[0])

            hidden_layer_delta = calc_delta_hl(self.Net[1], hidden_layer_output, out_delta)
            print('\t\t\tHL_DELTA:', hidden_layer_delta)
            #3rd stage
            if hidden_layer_delta:
                i = 0
                for neuron in self.Net[0]:
                    print('correct in hidden layer, old =', neuron.weights, 'input:', input_, 'hl_delta[j]:', hidden_layer_delta[i])
                    
                    neuron.correct_weight(input_, hidden_layer_delta[i])
                    print
                    i += 1
            if out_delta:
                j = 0
                for neuron in self. Net[1]:
                    print('correct in out layer, old =', neuron.weights, 'hl_out:', hidden_layer_output, 'out_delta[j]:', out_delta)
                    neuron.correct_weight(hidden_layer_output, out_delta)
                    print('new =', neuron.weights)
                    j += 1
            #calc_err
            error = math.sqrt(summaryErr)
            if error <  0.0001:
                print('Done!')
                print_results(epoch, net_output, error)
                return
            print_results(epoch, net_output, error)
            epoch += 1

def print_results(epoch, out, err):
    print('-'*50, '\nresults:\n', out, '\n', '-'*50)
    print('Epoch:', epoch, "Summary error:", err)

def calc_summary_err(ideal, output):
    sum_ = 0
    #for i in range (len(ideal)):
    #    sum_ += (ideal[i] - output[i])**2
    tmp = abs(ideal[0] - output[0])
    return tmp

def calc_derivative(x):
    result = 0.5*(1-(x**2))
    return result

def calc_delta_hl(out_layer, hl_out, out_delta):
    delta_hl = []
    for j in range(len(hl_out)):
        deltaj = calc_derivative(hl_out[j])* out_layer[0].weights[j]*out_delta
        delta_hl.append(deltaj)
    return delta_hl
    
if __name__ == '__main__':
    nn = NeuralNet(1, 2, 1)
    nn.train([1, 2], [-3])