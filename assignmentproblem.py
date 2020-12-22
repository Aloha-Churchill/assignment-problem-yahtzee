import numpy as np

#upper board
# Category 1: 1*(number of 1s rolled)
# Category 2: 2*(number of 2s rolled)
# Category 3: 2*(number of 3s rolled)
# Category 4: 2*(number of 4s rolled)
# Category 5: 2*(number of 5s rolled)
# Category 6: 2*(number of 6s rolled)

#goal 1: player is allowed 1 roll for each turn, this simulates 6 turns and calculates optimal score by checking all categories
#this program aims to optimize the scores by allocating different dice rolls to different categories.
#Ex: if you roll 5 6's, its better to count as category 6 (score 36) rather than category 1 (score 0)

def simulateRoll(iter):
    all_rolls = []
    for turns in range(iter):
        roll_outcome = np.random.randint(1,7, size = 5)
        all_rolls.append(roll_outcome.tolist())
    return all_rolls

def countScore(player_rolls):
    score_arr = []
    #roll_category_scores is keeping track of what the score would be if you marked the roll as ith category i from 1-6
    for roll_num in range(0,6):
        roll_category_scores = np.zeros(6).astype(int)
        for category_num in range(1, 7):
            count = np.count_nonzero(np.array(player_rolls[roll_num])==category_num)
            this_score = count*category_num
            roll_category_scores[category_num-1] = this_score
        score_arr.append(roll_category_scores.tolist())
    return score_arr

#helper function counts minimum number of lines needed to cross out all zeroes
def crossLines(arr):
    # first create second array with num zeroes row-wise (positive) and col-wise (negative) for each element
    arr_t = np.transpose(arr)
    min_lines_arr = np.zeros((6, 6), dtype=int)
    for row in range(0, 6):
        row_zeroes = 6 - np.count_nonzero(arr[row])
        for col in range(0, 6):
            col_zeroes = 6 - np.count_nonzero(arr_t[col])
            if (col_zeroes > row_zeroes):
                min_lines_arr[row][col] = col_zeroes * -1
            else:
                min_lines_arr[row][col] = row_zeroes

    # loop through min_lines_arr and if the corresponding element is zero in original arr and unmarked (positive)
    # where marked is negative then look at sign of min_lines_arr and put line either h or v through row/col
    line_count = 0
    for row in range(0, 6):
        for col in range(0, 6):
            if (arr[row][col] == 0):
                line_count += 1
                if (min_lines_arr[row][col] > 0):
                    # mark all horizontal
                    arr[row] = np.repeat(500, 6) + arr[row]
                else:
                    # mark all vertical
                    arr = np.transpose(arr)
                    arr[col] = np.repeat(500, 6) + arr[col]
                    arr = np.transpose(arr)

    return line_count

#helper function to choose optimal solution based on reduced matrix
def chooseOptimalSolution(arr):
    solution_arr = [-1, -1, -1, -1, -1, -1]
    unassigned_rows = [0,1,2,3,4,5]

    exist_single_zero = True
    while(exist_single_zero == True):
        num_zeroes_counter = 0
        for r in unassigned_rows:
            num_zeroes = 6 - np.count_nonzero(arr[r])
            if(num_zeroes == 1):
                num_zeroes_counter += 1
                unassigned_rows.remove(r)
                for c in range(0,6):
                    if (arr[r][c] == 0):
                        solution_arr[r] = c
                        arr = np.transpose(arr)
                        arr[c] = np.repeat(500, 6) + arr[c]
                        arr = np.transpose(arr)
        if(num_zeroes_counter == 0):
            exist_single_zero = False

    # arbitrarily sets ties to first zero in row
    exist_multiple_zeroes = True
    while(exist_multiple_zeroes):
        num_zeroes_counter = 0
        for r in unassigned_rows:
            num_zeroes = 6 - np.count_nonzero(arr[r])
            if num_zeroes > 0:
                num_zeroes_counter +=1
                unassigned_rows.remove(r)
                for c in range(0,6):
                    if(arr[r][c] == 0):
                        solution_arr[r] = c
                        arr = np.transpose(arr)
                        arr[c] = np.repeat(500, 6) + arr[c]
                        arr = np.transpose(arr)
                        break
        if(num_zeroes_counter == 0):
            exist_multiple_zeroes = False

    #sets rows with no assignment
    for i in range(0,6):
        if(solution_arr[i] == -1):
            solution_arr[i] = unassigned_rows[0]
            unassigned_rows.pop()

    return solution_arr


#uses hungarian method to assignment problem but for maximization
def optimizeScore(score_arr):
    #turning into maximization instead of minimization problem
    arr = np.asarray(score_arr).reshape(6,6)
    max = np.repeat(np.amax(score_arr), 36).reshape(6,6)
    arr = np.subtract(max,arr)

    #subtracting min element from each row
    for i in range(0,6):
        min_row = np.repeat(np.amin(arr[i]), 6)
        arr[i] = arr[i] - min_row

    #subtracting min element from each col
    arr = np.transpose(arr)
    for j in range(0,6):
        min_col = np.repeat(np.amin(arr[j]),6)
        arr[j] = arr[j] - min_col
    arr = np.transpose(arr)

    #using minimum number of lines to cross out zeroes
    line_count = crossLines(arr)

    # check if line_count = dimension of array
    while(line_count < 6):
        #find minimum value remaining
        min_remaining = 500
        for r in range(0,6):
            for c in range(0,6):
                if(arr[r][c] < 500 and min_remaining > arr[r][c]):
                    min_remaining = arr[r][c]
        #subtracting min from remaining elements and adding to elements with 2 lines
        for r in range(0,6):
            for c in range(0,6):
                if(arr[r][c] < 500):
                    arr[r][c] = arr[r][c]-min_remaining
                if(arr[r][c]>=1000):
                    arr[r][c] = arr[r][c] + min_remaining

        #recover original array
        arr = np.mod(arr, np.repeat(500, 36).reshape(6,6))
        line_count = crossLines(arr)

    arr = np.mod(arr, np.repeat(500, 36).reshape(6, 6))
    return chooseOptimalSolution(arr)

def sum_score(score_arr, optimal_solution):
    sum = 0
    for i in range(0,6):
        sum += score_arr[i][optimal_solution[i]]
    return sum

def play():
    player_rolls = simulateRoll(6)
    score_arr = countScore(player_rolls)
    optimal_solution = optimizeScore(score_arr)
    print(sum_score(score_arr, optimal_solution))



play()
