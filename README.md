#BoltzmanMachine

The traveling salesman problem (TSP) was computed using a modified version of the Boltzmann machine. By having a matrix which represents the distances between cities and having an initially randomly generated binary activation matrix. Having this matrix and a user denoted temperature, bonus and penalty we compute the delta c and the probability of acceptance. We then compare the probability of acceptance with a randomly generated number and if the number is less than the probability of acceptance we change that element in the activation matrix to the opposite. We repeat this process for every element in the activation matrix randomly and then decrease the temperature by 5 per cent. We continue doing this until the temperature falls below a user denoted threshold. Then we acquire our local minimum distance traveled and the activation matrix. This process is repeated 10,000 times and from this we pick our best result which is our outputted minimum.

### Technology
Python 3, Neural Networks.
