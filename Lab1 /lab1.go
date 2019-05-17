package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"github.com/notnil/combos"
)

var trainingSet = map[[4]uint8]uint8{
	{0, 0, 0, 0}: 1,
	{0, 0, 0, 1}: 0,
	{0, 0, 1, 0}: 1,
	{0, 0, 1, 1}: 1,

	{0, 1, 0, 0}: 1,
	{0, 1, 0, 1}: 0,
	{0, 1, 1, 0}: 1,
	{0, 1, 1, 1}: 1,

	{1, 0, 0, 0}: 1,
	{1, 0, 0, 1}: 1,
	{1, 0, 1, 0}: 1,
	{1, 0, 1, 1}: 1,

	{1, 1, 0, 0}: 1,
	{1, 1, 0, 1}: 0,
	{1, 1, 1, 0}: 1,
	{1, 1, 1, 1}: 1,
}

var booleanTable = [][4]uint8{
	{0, 0, 0, 0},
	{0, 0, 0, 1},
	{0, 0, 1, 0},
	{0, 0, 1, 1},
	{0, 1, 0, 0},
	{0, 1, 0, 1},
	{0, 1, 1, 0},
	{0, 1, 1, 1},
	{1, 0, 0, 0},
	{1, 0, 0, 1},
	{1, 0, 1, 0},
	{1, 0, 1, 1},
	{1, 1, 0, 0},
	{1, 1, 0, 1},
	{1, 1, 1, 0},
	{1, 1, 1, 1},
}

type neuron struct {
	weights       [5]float64
	aFunction     func(x float64) float64
	aFunctionName string
	learningRate  float64
}

func (n *neuron) netFunction(set [4]uint8) float64 {
	var sum float64
	for i, x := range set {
		sum += float64(x) * n.weights[i+1]
	}
	return n.weights[0] + sum
}

func (n *neuron) calculate(set [4]uint8) uint8 {
	net := n.netFunction(set)
	out := n.aFunction(net)
	if out >= 0.5 {
		return 1
	}
	return 0
}
func thresholdFunction(x float64) float64 {
	if x >= 0 {
		return 1
	}
	return 0
}
func sigmoidFunc(x float64) float64 {
	arg := float64(-x)
	return float64(1 / (1 + math.Exp(arg)))
}

func (n neuron) getMultiplier(set [4]uint8) float64 {
	var result float64
	if n.aFunctionName == "threshold" {
		result = 1
	} else if n.aFunctionName == "sigmoid" {
		net := n.netFunction(set)
		tmp := 1 - sigmoidFunc(net)
		result = sigmoidFunc(net) * tmp
	}
	return result
}
func (n *neuron) correctWeight(delta int, set [4]uint8) {
	multiplier := n.getMultiplier(set)
	n.weights[0] = n.learningRate*float64(delta) + n.weights[0]
	for i, x := range set {
		n.weights[i+1] = n.learningRate*float64(delta)*float64(x)*multiplier + n.weights[i+1]
	}
}
func printResults(results map[[4]uint8]uint8) {
	fmt.Println("Results:")
	for k, v := range results {
		fmt.Println(k, v)
	}
}
func (n *neuron) train(trainSet map[[4]uint8]uint8) bool {
	epoch := 0
	for {
		var results = map[[4]uint8]uint8{}
		fmt.Println("\n------\nEpoch:", epoch)
		fmt.Println("Weights:", n.weights)
		summaryErr := 0
		for set, idealValue := range trainSet {
			result := n.calculate(set)
			results[set] = result
			if result != idealValue {
				summaryErr++
				delta := int(idealValue) - int(result)
				n.correctWeight(delta, set)
			}
		}
		fmt.Println("Summary error:", summaryErr)
		if summaryErr == 0 {
			fmt.Println("---Done---")
			printResults(results)
			break
		}
		if epoch > 30 {
			return false
		}
		epoch++
	}
	return true
}
func getMinSet(n neuron) {
	for i := 0; i < 16; i++ {
		for _, indexArray := range combos.New(16, i) {
			fmt.Println(indexArray)
			newTrainSet := make(map[[4]uint8]uint8)
			for j := 0; j < len(indexArray); j++ {
				newTrainSet[booleanTable[j]] = trainingSet[booleanTable[j]]
			}
			if n.train(newTrainSet) {
				set := make([][4]uint8, 0)
				for k := range newTrainSet {
					set = append(set, k)
				}
				fmt.Println("Done ! Min set is :", set)
				return
			}
		}
	}
}
func main() {
	fmt.Println("-----\nstart with threshold function")
	n1 := neuron{weights: [5]float64{0, 0, 0, 0, 0}}
	n1.aFunction = thresholdFunction
	n1.aFunctionName = "threshold"
	n1.learningRate = 0.3
	n1.train(trainingSet)

	fmt.Println("-----\nstart with sigmoid function")
	n2 := neuron{weights: [5]float64{0, 0, 0, 0, 0}}
	n2.aFunction = sigmoidFunc
	n2.aFunctionName = "sigmoid"
	n2.learningRate = 0.3
	n2.train(trainingSet)

	n3 := neuron{weights: [5]float64{0, 0, 0, 0, 0}}
	n3.aFunction = thresholdFunction
	n3.aFunctionName = "threshold"
	n3.learningRate = 0.3
	getMinSet(n3)
	getMinSet(n1)
	scan := bufio.NewScanner(os.Stdin)
	fmt.Println("input set for test:")
	for scan.Scan() {
		var testSet [4]uint8
		rawText := scan.Text()
		splitedText := strings.Split(rawText, ",")
		fmt.Println("input :", splitedText)
		for i, element := range splitedText {
			parsed, err := strconv.Atoi(element)
			if err != nil {
				return
			}
			testSet[i] = uint8(parsed)
		}
		fmt.Println("With threshold:", n1.calculate(testSet))
		fmt.Println("With sigmoid:", n2.calculate(testSet))
	}
}
