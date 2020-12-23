import random
import numpy as np
import matplotlib.pyplot as plt

def simulateRolls(iter):
    # frequency count is a dictionary that counts the number of dice in common with eachother where 1 indicates that none of the dice
    #share a common value and 5 indicates that all dice share a common value
    frequency_count = {1:0, 2:0, 3:0, 4:0, 5:0}
    for turns in range(iter):
        roll_outcome = np.random.randint(1,7, size = 5)
        unique = np.unique(roll_outcome)
        frequency_count[6-len(unique)] += float(1/iter)

    plt.bar(*zip(*frequency_count.items()))
    plt.ylabel('Percentage of first rolls')
    plt.xlabel('Number of dice in common')
    plt.show()
    #probability of getting a yahtzee on the first roll
    #print(frequency_count[5]/iter)

#smart player picks the highest number of dice to keep and rolls the others
def randomRoll(prev_roll, dice_indices):
    for i in dice_indices:
        prev_roll[i] = random.randint(1,6)
    return prev_roll

def findHighestFrequency(nth_roll):
    freq = [0,0,0,0,0,0]
    for i in range(len(nth_roll)):
        freq[nth_roll[i]-1] += 1

    max = -1
    index = -1
    for j in range(5,-1,-1):
        if freq[j] > max:
            max = freq[j]
            index = j

    common_num = index+1

    indices_to_scramble = []
    for k in range(len(nth_roll)):
        if nth_roll[k] != common_num:
            indices_to_scramble.append(k)

    return indices_to_scramble

def rollTimesN(N, iter):
    prev_roll = [0,0,0,0,0]
    dice_indices = [0,1,2,3,4]
    for n in range(N):
        nth_roll = randomRoll(prev_roll, dice_indices)
        print(nth_roll)
        prev_roll = nth_roll
        dice_indices = findHighestFrequency(prev_roll)


rollTimesN(3,4)