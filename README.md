# Yahtzee!


1) ----------------------------------------------------------------------------
Hungarian algorithm to the assignment problem to solve Yahtzee! problem

I've been looking into some of the math behind Yahtzee! and I wanted to write a program to explore the game more. This code simulates 6 random rolls (each roll consists of 5 dice) and this is stored into an array. The top scoreboard in Yahtzee! is below:

Category 1: 1*(number of 1s rolled)

Category 2: 2*(number of 2s rolled)

Category 3: 2*(number of 3s rolled)

Category 4: 2*(number of 4s rolled)

Category 5: 2*(number of 5s rolled)

Category 6: 2*(number of 6s rolled)

So once I had the 6 rolls, I wanted to optimize the score that you could get knowing your 6 rolls. While this wouldn't happen in a real game because you wouldn't know your scores before you actually rolled them, I thought it would be interesting to start to see optimization strategies. For example, it wouldn't be wise if you rolled 4 6's to count them in Category 1. To optimize the score, an inverse probelm was minimizing the "cost matrix" and is a problem that I learned was called the "assignment problem". Worst case algorithmic time for this would be n! but there is an algorithmically less taxing way to solve the assigment problem using a technique called the Hungarian algorithm. I'm not actually sure if my code solved it more efficently, but it was fun to see and code a different approach to the classic solution to the assignment problem!   


2) -----------------------------------------------------------------------------------
Frequency Graph

Here, I graphed the number of dice in common over an arbitrary amount of rolls. From this graph, I saw that the most common number of dice in common on the first roll was 2 dice. In this function, it was also possible to calculate the probability of getting a Yahtzee! on the first roll. Mathematically, this probability is 6*(1/6)^5 and in my program, the limit as iter->infinity converged to this probability. 

I then simulated a "smart" yahtzee player who wanted to roll a Yahtzee. In this simulation, the player kept the most common dice and rolled the rest over and over again. The probability for a Yahtzee increased for the third roll and converged to 1 over as the number of rolls increased towards infinity. 

