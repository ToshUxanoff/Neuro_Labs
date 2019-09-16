#!/usr/bin/python3

import sys
import numpy as np
import copy

class Node:
    def __init__(self, length, level):
        self.weight = [np.float(1)] * length
        self.level = level
        self.result = None
        self.out = None
    
    def calc_net(self, x_array):
        res = 0
        for j in range(1, len(self.weight)):
            res += self.weight[j]*x_array[j-1]
        res += self.weight[0]
        self.result = res
    
    def func_activate(self):
        self.out = (1 - np.exp(-1 * self.result)) / (1 + np.exp(-1 * self.result))

    def get_result(self):
        self.func_activate()
        return self.out

    def calc_delta(self, delta_m):
        res = 0
        for ind in range(len(delta_m)):
            res += self.weight[ind] * delta_m[ind]
        return res

    def correct_weight(self, X, delta, nu=1):
        for ind in range(len(self.weight)):
            self.weight[ind] += nu * X[ind] * delta

def count_result(lvl1, lvl2, X):
    net1 = [1]
    for n1 in lvl1:
        n1.calc_net(X)
        net1.append(n1.get_result())
    result = []

    for n2 in lvl2:
        n2.calc_net(net1)
        result.append(n2.get_result())

    return net1, result

def derivate(out):
    res = 0.5 * (1 - (out**2))
    return res
N, J, M = (2, 1, 2)
def pprint(data):
    print('-'*20)
    print("структура нейронной сети {}-{}-{}".format(N, J, M))
    s1, s2, s3, s4, s5 = "номер эпохи", "вектор весов скрытого слоя", "вектор весов выходного слоя", "выходной вектор y", "суммарная ошибка e"
    print("|{:^11s}|{:^40s}|{:^40s}|{:^20s}|{:^3s}|\n".format(s1,s2,s3,s4,s5)+"-"*130)
    for elem in data:
        w1, w2, epoch, y_array, epsilon = elem
        y_array = list(map(lambda x: f"{x:.3f}", y_array))
        new_w1 = []
        for elem in w1:
            new_w1.append(list(map(lambda x: f"{x:.3f}", elem)))
        new_w2 = []
        for elem in w2:
            new_w2.append(list(map(lambda x: f"{x:.3f}", elem)))
        
        new_w1 = ['; '.join(elem) for elem in new_w1]
        w1 = ' && '.join(new_w1)

        new_w2 = ['; '.join(elem) for elem in new_w2]
        w2 = ' && '.join(new_w2)
        print(f"| {epoch:^9} | {w1:^38} |{w2:^38} |{','.join(y_array):^20} | {epsilon:^18} |")
        print('-'*130)

#N, J, M = (3, 3, 4)

def run_epoch(lvl1, lvl2, X, T):
    epoch = 0
    data = []
    while True:
        packet = []
        
        hide_weight = []
        for node in lvl1:
            hide_weight.append(copy.deepcopy(node.weight))
        packet.append(hide_weight)

        out_weight = []
        for node in lvl2:
            out_weight.append(copy.deepcopy(node.weight))
        packet.append(out_weight)
        
        #"First stage"
        net1, result = count_result(lvl1, lvl2, X)
        
        #"Second stage"
        delta_m = [derivate(result[ind]) * (T[ind] - result[ind]) for ind in range(M)]
        error = np.float(0)
        for ind in range(M):
            error += (T[ind] - result[ind])**2
        
        delta_j = [
            derivate(node.get_result()) * node.calc_delta(delta_m) 
            for node in lvl1]
        
        #Third stage
        for ind in range(J):
            lvl1[ind].correct_weight(X, delta_j[ind])
        
        for ind in range(M):
            lvl2[ind].correct_weight(net1, delta_m[ind])
        
        error = np.sqrt(error)
        packet.extend([epoch, result, error])
        data.append( packet )
        if error < 10**(-3):
            break
        epoch += 1
    
    return data


if __name__ == '__main__':
    sys.stdout = open('log.txt', 'w')
    
    Y_func = [0] * M

    nodes_lvl1 = [Node(N+1, 1) for i in range(J)]
    nodes_lvl2 = [Node(J+1, 2) for i in range(M)]

    #X = (1, 0.3, -0.1, 0.9)
    #T = (0.1, -0.6, 0.2, 0.7)
    X = (1, 2, 1)
    T = (0.2, 0.1)
    
    data = run_epoch(nodes_lvl1, nodes_lvl2, X, T)
    pprint(data)

    sys.stdout.close()
    
