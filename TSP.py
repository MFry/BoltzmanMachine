#!/usr/bin/env python
"""
Created on May 7, 2011
Refactored for readability on January 27th, 2016
"""
import math
import os
import random

__author__ = "Michal Frystacky"


class BasicMatrix:
    def __init__(self):
        self.name = ""
        self.data = [[0] * 23]*23
        self.distance = 0

    def __str__(self):
        format = "%3i, "
        str = "%s\n" % ("The %s:" % self.name)
        str += '-' * 126
        str += "\n"
        str += " " * 8
        for i in range(23):
            str += "C:%-2i " % i
        str += "\n"
        i = 0
        for row in self.data:
            str += "Row: %-2i [" % i
            i += 1
            for j in range(len(row)):
                str += format % row[j]
            str += "]\n"
        return str


class Matrix(BasicMatrix):
    def __init__(self, fileName):
        self.name = "Distance Matrix"
        self.data = [[]*23]
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                                          os.path.dirname(__file__)))
        f = open(os.path.join(self.__location__, fileName))
        for i in range(23):
            for j in range(23):
                temp = f.readline()
                if temp == ' ':  # We do not add the EOL character
                    pass
                else:
                    self.data[i].append(int(temp))


class ActivationMatrix(BasicMatrix):
    # TODO: Refactor to properly use inheritance and class structure
    def init(self, b, p, t):
        # BONUS PENALTY TEMPERATURE
        self.bonus = b
        self.penalty = p
        self.temperature = t
        self.name = "Activation Matrix"

    def gen_random_values(self):
        for row in self.data:
            i = 0
            while i < len(row):
                r = random.random()
            if (r < 0.6):
                row[i] = 1
            else:
                row[i] = 0
            i += 1

    def decay(self):
        self.temperature = self.temperature * 0.95

    def calcDeltaC(self, row, column, matrix):
        activation = self.data[row][column]
        step = (1.0 - 2.0 * activation)
        # sums the column before, the column after, the column we are in
        #  and the row we are in
        sum = 0
        if (column == 0):
            for i in range(len(matrix.data)):
                # sum += -1 * self.data[i][len(self.data[i]) - 1] * \
                #    matrix.data[row][i]
                sum += -1 * self.data[i][column + 1] * matrix.data[row][i]
        elif (column == (len(matrix.data) - 1)):
            for i in range(len(matrix.data)):
                sum += -1 * self.data[i][column - 1] * matrix.data[row][i]
                # sum += -1 * self.data[i][0] * matrix.data[row][i]
        else:
            for i in range(len(matrix.data)):
                sum += -1 * self.data[i][column - 1] * matrix.data[row][i]
                sum += -1 * self.data[i][column + 1] * matrix.data[row][i]
                # calculate the same row and column
        for i in range(len(matrix.data)):
            if (i != row):
                sum += -1 * self.data[i][column] * self.penalty
            else:
                pass
            if (i != column):
                sum += -1 * self.data[row][i] * self.penalty
            else:
                pass
        step *= ((self.bonus * activation) + sum)
        return step


def probability_acceptance(self, deltaC):
    return (1.0 / (1.0 + math.exp(-1.0 * \
                                  (deltaC / float(self.temperature)))))


class MatrixPacket(BasicMatrix):
    def copy_matrix(self, activationMatrix):
        self.name = "Activation(p) Matrix"
        for i in range(len(activationMatrix.data)):
            self.data[i] = activationMatrix.data[i][:]

    def calculateFinalDistance(self, disMatrix):
        calcDis = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):  # iterate over every row
                if (j == len(self.data[i]) - 1) and (self.data[j][i] == 0):
                    self.patchIt(i)
                    self.distance = 10000000
                    return False  # we did not successfully calculate the distance
            if self.data[j][i] != 1:
                continue
            else:
                calcDis += 1
            if calcDis == 1:
                temp1 = j
                start = j
            else:
                # @bug: At some this ran fine, but it seems that now there is bug in this part of the code
                self.distance += disMatrix.data[temp1][j]
                temp1 = j
                calcDis = 1
            break
        self.distance += disMatrix.data[j][start]
        return True

    def patchIt(self, column):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == 1:
                    break
                elif (j == len(self.data[i]) - 1) and (self.data[i][j] == 0):
                    self.data[i][column] = 1
                    return


def findSD(locMatrix):
    actMatrix = ActivationMatrix()
    actMatrix.gen_random_values()
    actMatrix.init(1600, 1750, 550)
    # print ("T",actMatrix.temperature, actMatrix)
    # generate every possibility
    # @todo: better explain what I am doing here
    positions = \
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    while (actMatrix.temperature > 50):
        for rows in positions:
            for i in range(23):
                rows.append(i)
        done = False

        while not done:
            # find which random element in the matrix we are calculating
            while True:
                row = random.randrange(0, len(positions))
                # checks if this row is not empty
                if len(positions[row]) > 0:
                    break
                    # if it is we try again
            # we know there is an element in this row
            element = random.randrange(0, len(positions[row]))
            # we have to extract the number not the position due to the fact that we delete elements
            column = positions[row][element]
            # removes the appropriate element
            if element + 1 >= len(positions[row]):  # checks if element was the last column
                positions[row] = positions[row][:element]
            else:
                positions[row] = positions[row][:element] + positions[row][element + 1:]
            deltaC = actMatrix.calcDeltaC(row, column, locMatrix)
            acceptance = actMatrix.probAcceptance(deltaC)
            r = random.random()
            if r < acceptance:
                actMatrix.data[row][column] = 1 - actMatrix.data[row][column]
            else:
                pass
            # print ("deltaC: ",deltaC, " ", "acceptance: ", acceptance, " ", "r: ", r, "\n",actMatrix)
            # print ("x & y coords: ", row, column)
            # check if we iterated over the entire matrix
            zeroRows = 0
            for i in range(len(positions)):
                if len(positions[i]) > 0:
                    done = False
                    break
            else:
                zeroRows += 1
            if zeroRows == len(positions):
                done = True
        actMatrix.decay()

    packet = MatrixPacket()
    packet.copy_matrix(actMatrix)
    if not packet.calculateFinalDistance(locMatrix):
        packet.calculateFinalDistance(locMatrix)
        packet.calculateFinalDistance(locMatrix)
    return packet


def main():
    file_name = "MatrixData"
    location_matrix = Matrix(file_name)
    print(location_matrix)
    random.seed(42)
    minPacket = findSD(location_matrix)
    for i in range(10000):
        tempPacket = findSD(location_matrix)
        if tempPacket.distance < minPacket.distance:
            minPacket = tempPacket
    print(minPacket, minPacket.distance)


if __name__ == '__main__':
    main()
