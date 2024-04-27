import tkinter as tk
import random
import os
import time
import neat
import statistics
import matplotlib.pyplot as plt
import visualize
start = time.process_time()
test_matrix= [[0] * 4 for _ in range(4)]
GameOver = False
AIfitness =0
yAIscore = []
xAIscore = []

#Debug
debuggame = False

#Settings
fitnessIsScore = True       #Fitness is Score/Tile
InputScore = False          #change config!             if True: 17 inputs, if False: 16 inputs
numbergames = 1000          #games for validation
showstats = True            #shows+saves Stats or just saves them
showNEATstats = False



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
        test_matrix = self.matrix                       #to compare before/after move
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
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
                fill_position = 0
                for j in range(4):
                 if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix
        if test_matrix == self.matrix:          #if both is the same nothing changed -> game over
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
            flat_list = [item for sublist in self.matrix for item in sublist]       #convert two-dimensional list in flat list
            if InputScore == True: flat_list.append(self.score)                     #score as input
            AIoutput=net.activate(flat_list)                                        #AI
        
            #Digit of with highes value
            if AIoutput.index(max(AIoutput)) == 0:
                self.left()
            if AIoutput.index(max(AIoutput)) == 1:
                self.right()
            if AIoutput.index(max(AIoutput)) == 2:
                self.up()
            if AIoutput.index(max(AIoutput)) == 3:
                self.down()
        

    # Check if Game is Over (Win/Lose)         
    def game_over(self):
        global AIfitness
        global score
        if any(2048 in row for row in self.matrix):         #win
            print("win")
        if GameOver==True:
            if fitnessIsScore == True:
                AIfitness = self.score                      #sets fitness = score
            else:
                AIfitness = (max(max(self.matrix)))         #sets fitness = highest tile
            score = self.score                              #stats
            if debuggame == True: print("game over")






def Run(genomes, config):
    global net
    global GameOver
    global yAIscore
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        Game()                                                                          
        genome.fitness = AIfitness                                 
        yAIscore.append(score)                                  #for Satistic during training
        if debuggame == True: print (score)
        GameOver = False


def validationrun(bestgenome, config):
    global GameOver
    global net
    print("\n########## run ##########")
    net = neat.nn.FeedForwardNetwork.create(bestgenome, config)
    scorelist=[]
    xvalues = []

    #Runs Game for 'numbergames' times
    for i in range(numbergames):
        Game()
        GameOver = False
        scorelist.append(score)
        xvalues.append(i)
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
    print('\nTime for calculating:\n{!s}'.format(time.process_time()-start)+'s')
    #writes info to a file
    with open('info.txt', 'w') as f:
        f.write('\nWorst Value:\n{!s}'.format(min(scorelist)))
        f.write('\nBest Value:\n{!s}'.format(max(scorelist)))
        f.write('\nAverage Value:\n{!s}'.format(average))
        f.write('\nMedian:\n{!s}'.format(median))
        f.write('\nStandard deviation:\n{!s}'.format(statistics.stdev(scorelist)))
        f.write('\nCV:\n{!s}'.format(statistics.variance(scorelist)))
        f.write('\nTime for calculating:\n{!s}'.format(time.process_time()-start)+'s')
        f.write('\nFitness is Score: {!s}'.format(fitnessIsScore))



    #stats during run
    plt.plot([0, len(xvalues)], [average, average], color='red', label='Average')       #line for average
    plt.plot([0, len(xvalues)], [median, median], color='green', label='Median')        #line for median
    plt.scatter(xvalues, scorelist, s=1, color='blue', label='Score')                   #Dots for Score
    plt.plot([0, len(xvalues)], [average+statistics.stdev(scorelist), average+statistics.stdev(scorelist)], color='yellow', label='Standard deviation')       #line for Standard deviation
    plt.plot([0, len(xvalues)], [average-statistics.stdev(scorelist), average-statistics.stdev(scorelist)], color='yellow')
    plt.legend(loc='upper left')                              #legend
    plt.title("Score during run")
    plt.savefig('Score during run.pdf')
    plt.savefig('Score during run.png')
    if showstats==True: plt.show()
    plt.close()

    #Distribution during run
    maxdis= scorelist.count(max(set(scorelist), key=scorelist.count))
    plt.hist(scorelist, bins=max(scorelist))
    plt.plot([average, average], [0, maxdis], color='red', label='Average')
    plt.plot([median, median], [0, maxdis], color='green', label='Median')
    plt.plot([average+statistics.stdev(scorelist), average-statistics.stdev(scorelist)], [maxdis, maxdis], color='yellow', label='Standard deviation')
    plt.title("Distribution during run")
    plt.savefig('Distribution during run.pdf')
    plt.savefig('Distribution during run.png')
    if showstats==True: plt.show()
    plt.close()
    

def Stats(config, winner, stats):
    for i in range(len(yAIscore)):                                          #Genomes of one generation for statistics on top of each other (30genomes/generation)
        xAIscore.append(int(i/30))
    plt.scatter(xAIscore, yAIscore, s=1, color='blue', label='Score')
    plt.legend(loc='upper left')             #legend
    plt.title("Score during training")
    plt.savefig('Score during training.pdf')
    plt.savefig('Score during training.png')
    if showstats==True: plt.show()

    

    #Distribution during training
    plt.close()
    plt.hist(yAIscore, bins=max(yAIscore))
    plt.title("Distribution during training")
    plt.savefig('Distribution during training.pdf')
    plt.savefig('Distribution during training.png')
    if showstats==True: plt.show()
    plt.close()

    #visualisation stats 
    visualize.draw_net(config, winner, showNEATstats)
    visualize.plot_stats(stats, ylog=False, view=showNEATstats)
    visualize.plot_species(stats, view=showNEATstats)


def main(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))                                    #remove this line if you don't want to see the status in the promt
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 3000 generations.
    winner = p.run(Run, 30)
    bestgenome = stats.best_genome()
    # Display the best genome.
    print('\nGenome with the highest fitness:\n{!s}'.format(bestgenome))

    #validationrun
    validationrun(bestgenome, config)
    
    #stats during training
    Stats(config, bestgenome, stats)
    




if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    main(config_path)