import tkinter as tk
import random
import time
import statistics
import matplotlib.pyplot as plt

test_matrix= [[0] * 4 for _ in range(4)]
GameOver = False
score = 0


#Debug
debuggame = False
#Settings
fitnessIsScore = True
numbergames = 1000



class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.start_game()
        self.AI()
    # Move Functions

    def left(self):
        if debuggame == True: print("Left")
        self.stack()
        self.combine()
        self.stack2()
        self.game_over()
        if GameOver == False:
            self.add_new_tile()


    def right(self):
        if debuggame == True: print("Right")
        self.reverse()
        self.stack()
        self.combine()
        self.stack2()
        self.game_over()
        if GameOver == False:
            self.reverse()
            self.add_new_tile()


    def up(self):
        if debuggame == True: print("Up")
        self.transpose()
        self.stack()
        self.combine()
        self.stack2()
        self.game_over()
        if GameOver == False:
            self.transpose()
            self.add_new_tile()


    def down(self):
        if debuggame == True: print("Down")
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack2()
        self.game_over()
        if GameOver == False:
            self.reverse()
            self.transpose()
            self.add_new_tile()




    def start_game(self):
        if debuggame == True: print("start game")
        # create matrix of zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.score = 0




    # Matrix Manipulation Functions
    #first stacking
    def stack(self): 
        if debuggame == True: print(" stack1")
        global test_matrix
        test_matrix= [[0] * 4 for _ in range(4)]
        test_matrix = self.matrix
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    #second stacking
    def stack2(self):
        if debuggame == True: print(" stack2")    
        global test_matrix
        global new_matrix
        global GameOver  
       # print(test_matrix)
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
                fill_position = 0
                for j in range(4):
                 if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix
        if test_matrix == self.matrix:
            GameOver = True


    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]


    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix


    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix


    # Add a new 2 or 4 tile randomly to an empty cell

    def add_new_tile(self):
        if debuggame == True: print(" add new tile")
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    def AI(self):
        while GameOver == False:
            if debuggame == True: 
                print("AI")
                time.sleep(1)
            randomchoice=random.randint(0,3)        #random numbers 0-3
            if randomchoice == 0:
                self.left()
            if randomchoice == 1:
                self.right()
            if randomchoice == 2:
                self.up()
            if randomchoice == 3:
                self.down()
        

    # Check if Game is Over (Win/Lose)         
    def game_over(self):
        global score
        if any(2048 in row for row in self.matrix):
            print("win")
        elif GameOver==True:
            if fitnessIsScore == True:
                score = self.score              #stats
            else:
                score = (max(max(self.matrix)))
            if debuggame == True: print("game over")


def run():
    global GameOver
    scorelist=[]
    xvalues = []

#Runs Game for 'numbergames' times
    for i in range(numbergames):
        Game()
        GameOver = False
        scorelist.append(score)
        xvalues.append(i)
        plt.plot(i, score)
        i+=1

#Prints Stats
    average = statistics.mean(scorelist)
    median = statistics.median(scorelist)
    print('\nWorst Value:\n{!s}'.format(min(scorelist)))
    print('\nBest Value:\n{!s}'.format(max(scorelist)))
    print('\nAverage Value:\n{!s}'.format(average))
    print('\nMedian:\n{!s}'.format(median))
    print('\nStandard deviation:\n{!s}'.format(statistics.stdev(scorelist)))
    print('\nCV:\n{!s}'.format(statistics.variance(scorelist)))

#Plotts Stats
    plt.scatter(xvalues, scorelist, s=1, label='Score')
    plt.plot([0, len(xvalues)], [average, average], color='red', label='Average')       #line for average
    plt.plot([0, len(xvalues)], [median, median], color='green', label='Median')        #line for median
    plt.plot([0, len(xvalues)], [average+statistics.stdev(scorelist), average+statistics.stdev(scorelist)], color='yellow', label='Standard deviation')       #line for Standard deviation
    plt.plot([0, len(xvalues)], [average-statistics.stdev(scorelist), average-statistics.stdev(scorelist)], color='yellow')
    plt.legend(loc='best')
    plt.title('Score ')
    plt.savefig('RandomStatistic.pdf')
    plt.show()

    #Distribution
    maxdis= scorelist.count(max(set(scorelist), key=scorelist.count))
    plt.close()
    plt.hist(scorelist, bins=max(scorelist))
    plt.plot([average, average], [0, maxdis], color='red', label='Average')
    plt.plot([median, median], [0, maxdis], color='green', label='Median')
    plt.plot([average+statistics.stdev(scorelist), average-statistics.stdev(scorelist)], [maxdis, maxdis], color='yellow', label='Standard deviation')
    plt.title("Random Distribution")
    plt.legend(loc='best')
    plt.savefig('Random distribution.pdf')
    plt.savefig('Random distribution.png')
    plt.show()







if __name__ == '__main__':
    run()
