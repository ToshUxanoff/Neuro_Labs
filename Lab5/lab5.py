import math
#train set
#---
trainset = {
    'zero': [1, 1, 1, 1, 1,
             1,-1,-1,-1, 1,
             1,-1,-1,-1, 1,
             1,-1,-1,-1, 1,
             1, 1, 1, 1, 1],

    'one':  [-1,-1, 1,-1,-1,
             -1, 1, 1,-1,-1,
              1,-1, 1,-1,-1,
              -1,-1, 1,-1,-1,
              1, 1, 1, 1, 1],
    'nine': [1, 1, 1, 1, 1,
             1,-1,-1,-1, 1,
             1, 1 ,1 ,1 ,1,
             -1,-1,-1,-1, 1,
             1, 1, 1, 1, 1],
}
checkset = {
    'zero': [1,-1,-1, 1, 1,
             1,-1,-1,-1, 1,
             1,-1,-1,-1, 1,
             1,-1,-1,-1, 1,
             1, 1, 1, 1, 1],

    'one':  [ -1,-1, 1,-1,-1,
              -1, 1, 1, 1,-1,
               1,-1, 1,-1, 1,
              -1,-1, 1,-1,-1,
               1, 1, 1, 1, 1],
    'nine': [ 1, 1, 1, 1, 1,
              1,-1, 1,-1, 1,
              1, 1 ,1 ,1 ,1,
             -1,-1,-1,-1, 1,
              1, 1, 1, 1, 1],
}
#1 1 1 1 1
#1 0 0 0 1
#1 0 0 0 1
#1 0 0 0 1
#1 1 1 1 1
    
#0 0 1 0 0 
#0 1 1 0 0 
#1 0 1 0 0
#0 0 1 0 0
#1 1 1 1 1  

#1 1 1 1 1
#1 0 0 0 1
#1 1 1 1 1
#0 0 0 0 1
#1 1 1 1 1
#---


    
class NeuralNet:
    def __init__(self):
        self.weights_matrix = []
        self.K = 25
        self.Y = []
        self.nets = []
        for i in range(self.K):
            self.weights_matrix.append([0 for j in range(self.K)])
            
    
    def initialize(self):
        for j in range(self.K):
            for i in range(self.K):
                if i == j:
                    self.weights_matrix[j][i] = 0
                else:
                    summ = 0
                    for key, set_ in trainset.items():
                        summ += set_[j]*set_[i]
                    self.weights_matrix[j][i] = summ

    def calc_out(self, net, epoch):
        result = 0
        if net > 0:
            result = 1
        elif net < 0:          
            result = -1
        else:
            return self.calc_out(self.nets[epoch-1], epoch - 1)
        return result

    def work(self, image):
        epoch = 1
        self.Y = image
        while True:
            y = []
            this_net = []
            last_net = this_net
            for k in range(self.K):
                net = 0
                sum1 = 0
                for j in range(k):
                    sum1 += self.weights_matrix[j][k]*self.Y[j]
                sum2 = 0
                for j in range(k+1, self.K):
                    sum2 += self.weights_matrix[j][k]*self.Y[j]
                net = sum1 + sum2
                out = self.calc_out(net, epoch)
                if out != self.Y[k]:
                    self.Y[k] = out
                self.nets.append(net)
                this_net.append(net)
                y.append(out)
            
            if  last_net == this_net:
                result_print(y)
                return y
            if epoch > 200:
                print('cant recognize')
                return
            epoch +=1
            
def result_print(result):
    tmp = ""
    for i in range(len(result)):
        if i % 5 == 0:
            tmp += '\n'
        if result[i] == -1:
            tmp+= ' '
        else:
            tmp+= '#'
    print(tmp)
if __name__ == '__main__':
    nn = NeuralNet()
    nn.initialize()
    print('Wrong images:')
    result_print(checkset['one'])
    result_print(checkset['nine'])
    result_print(checkset['zero'])
    print('-'*50)
    print('Result:')
    nn.work(checkset['one'])
    nn.work(checkset['nine'])
    nn.work(checkset['zero'])
