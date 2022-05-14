# Library import
import tkinter
import math
import time
import random
from copy import deepcopy

# Variable setup
moves = 0

# Tkinter setup
root = tkinter.Tk()
screen = tkinter.Canvas(root, width=500, height=600, background="#222", highlightthickness=0)
screen.pack()

decentHeuristicMatrix = [
            [100 , -10 , 8  ,  6 ,  6 , 8  , -10 ,  100],
            [-10 , -25 ,  -4, -4 , -4 , -4 , -25 , -10 ],
            [8   ,  -4 ,   6,   4,   4,   6,  -4 ,  8  ],
            [6   ,  -4 ,   4,   0,   0,   4,  -4 ,  6  ],
            [6   ,  -4 ,   4,   0,   0,   4,  -4 ,  6  ],
            [8   ,  -4 ,   6,   4,   4,   6,  -4 ,  8  ],
            [-10 , -25 ,  -4,  -4, -4 , -4 , -25 , -10 ],
            [100 , -10 ,   8,   6,  6 , 8  , -10 ,  100]]
betterHeuristicMatrix = [
            [   5,  -3 ,   3,   3,   3,   3,   -3,    5],
            [  -3,   -1,   1,   1,   1,   1,   -1,   -3],
            [   3,    1,   1,   1,   1,   1,    1,    3],
            [   3,    1,   1,   1,   1,   1,    1,    3],
            [   3,    1,   1,   1,   1,   1,    1,    3],
            [   3,    1,   1,   1,   1,   1,    1,    3],
            [  -3,   -1,   1,   1,   1,   1,   -1,   -3],
            [   5,   -3,   3,   3,   3,   3,   -3,    5]]

class PvEBoard:
    def __init__(self, humanTurn):
        # White goes first (0 is white and player, 1 is black and computer)
        
        self.humanTurn = humanTurn
        self.player = 0
        self.passed = False
        self.won = False

        self.player_score = 0
        self.computer_score = 0

        # Initializing an empty board
        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)

        # Initializing center values
        self.array[3][3] = "w"
        self.array[3][4] = "b"
        self.array[4][3] = "b"
        self.array[4][4] = "w"

        # Initializing old values
        self.oldarray = self.array
        self.level = 0

    def visualUpdate(self):
        screen.delete("highlight")
        screen.delete("tile")

        for x in range(8):
            for y in range(8):
                if self.oldarray[x][y] == "w":
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif self.oldarray[x][y] == "b":
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")

        # Animation of new tiles
        screen.update()
        for x in range(8):
            for y in range(8):
                if self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "w":
                    screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#000", outline="#000")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#aaa", outline="#aaa")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile", fill="#aaa",
                                       outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile", fill="#fff",
                                       outline="#fff")
                    screen.update()

                elif self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "b":
                    screen.delete("{0}-{1}".format(x, y))
                    for i in range(21):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#aaa", outline="#aaa")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#000", outline="#000")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            time.sleep(0.01)
                        screen.update()
                        screen.delete("animated")

                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile", fill="#000",
                                       outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile", fill="#111",
                                       outline="#111")
                    screen.update()

        # Drawing of highlight circles
        for x in range(8):
            for y in range(8):
                if self.player == self.humanTurn:
                    if self.valid(self.array, self.player, x, y):
                        screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1),
                                           tags="highlight", fill="#008000", outline="#008000")

    # Updating the board to the screen
    def update(self):
        self.visualUpdate()
        if not self.won:
            # Draw the scoreboard and update the screen
            self.drawScoreBoard()
            screen.update()
            # If the player is AI, make a move
            if self.player != self.humanTurn:
                startTime = time.time()
                self.oldarray = self.array
                alphaBetaResult = self.MNABMove(self.array, 5, -math.inf, math.inf, 1)
                self.array = alphaBetaResult[1]

                if len(alphaBetaResult) == 3:
                    position = alphaBetaResult[2]
                    if self.humanTurn == 0:
                        self.oldarray[position[0]][position[1]] = "w"
                    else:
                        self.oldarray[position[0]][position[1]] = "b"

                self.player = 1 - self.player
                deltaTime = round((time.time() - startTime) * 100) / 100
                if deltaTime < 2:
                    time.sleep(2 - deltaTime)
                self.drawScoreBoard()
                self.visualUpdate()
                self.oldarray = self.array
                # Player must pass?
                self.passTest()

        else:
            message = None
            if self.player_score > self.computer_score:
                message = "The Human Player has won !"
            else:
                message = "The AI has bested Humanity !"
            screen.create_text(250, 550, anchor="center", font=("Consolas", 15), text=message)

    # Moves to position
    def boardMove(self, x, y):
        # Move and update screen
        self.oldarray = self.array
        if self.humanTurn == 0:
            self.oldarray[x][y] = "b"
        else:
            self.oldarray[x][y] = "w"
        self.array = self.move(self.array, x, y)

        # Switch Player
        self.player = 1 - self.player
        self.update()

        # Check if AI must pass
        self.passTest()
        self.update()

    # METHOD: Draws scoreboard to screen
    def drawScoreBoard(self):
        global moves
        # Deleting prior score elements
        screen.delete("score")

        # Scoring based on number of tiles
        self.player_score = 0
        self.computer_score = 0
        hc = ""
        cc = ""
        if self.humanTurn == 0:
            hc = "b"
            cc = "w"
        else:
            hc = "w"
            cc = "b"
        for x in range(8):
            for y in range(8):
                if self.array[x][y] == hc:
                    self.player_score += 1
                elif self.array[x][y] == cc:
                    self.computer_score += 1

        if self.player == self.humanTurn:
            player_colour = "green"
            computer_colour = "gray"
        else:
            player_colour = "gray"
            computer_colour = "green"

        screen.create_oval(5, 540, 25, 560, fill=player_colour, outline=player_colour)
        screen.create_oval(380, 540, 400, 560, fill=computer_colour, outline=computer_colour)

        # Pushing text to screen
        screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="white",
                           text=self.player_score)
        screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black",
                           text=self.computer_score)

        moves = self.player_score + self.computer_score

    # METHOD: Test if player must pass: if they do, switch the player
    def passTest(self):
        mustPass = True
        for x in range(8):
            for y in range(8):
                if self.valid(self.array, self.player, x, y):
                    mustPass = False
        if mustPass:
            self.player = 1 - self.player
            if self.passed:
                self.won = True
            else:
                self.passed = True
            self.update()
        else:
            self.passed = False

    # METHOD: Random AI - Chooses a random move
    def randomMove(self):
        # Generates all possible moves
        choices = []
        for x in range(8):
            for y in range(8):
                if self.valid(self.array, self.player, x, y):
                    choices.append([x, y])
        # Chooses a random move, moves there
        dumbChoice = random.choice(choices)
        return dumbChoice[0], dumbChoice[1]

    # Alpha - Beta pruning on the Mini - Max Tree
    # http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    def MNABMove(self, node, depth, alpha, beta, maximizing):
        boards = []
        choices = []

        for x in range(8):
            for y in range(8):
                if self.valid(self.array, self.player, x, y):
                    test = self.move(node, x, y)
                    boards.append(test)
                    choices.append([x, y])

        # Final Stand
        if depth == 0 or len(choices) == 0:
            if self.level == 1:
                return [self.betterHeuristic(node, maximizing), node]
            elif self.level == 2:
                return [self.decentHeuristic(node, maximizing), node]
            else:  # self.level == 3
                return [self.dynamicHeuristic(node, maximizing), node]

        if maximizing:
            v = -math.inf
            bestBoard = []
            bestChoice = []
            for board in boards:
                boardValue = self.MNABMove(board, depth - 1, alpha, beta, 0)[0] #Heuristic Value
                if boardValue > v:
                    v = boardValue
                    bestBoard = board
                    bestChoice = choices[boards.index(board)]
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return [v, bestBoard, bestChoice]
        else:
            v = math.inf
            bestBoard = []
            bestChoice = []
            for board in boards:
                boardValue = self.MNABMove(board, depth - 1, alpha, beta, 1)[0]
                if boardValue < v:
                    v = boardValue
                    bestBoard = board
                    bestChoice = choices[boards.index(board)]
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return ([v, bestBoard, bestChoice])

    # Simple heuristic. Compares number of each tile.
    def simpleHeuristic(self, array, player):
        score = 0
        # Set player and opponent colours
        if player != 0:
            colour = "w"
            opponent = "b"
        else:
            colour = "b"
            opponent = "w"
        # +1 if it's player colour, -1 if it's opponent colour
        for x in range(8):
            for y in range(8):
                if array[x][y] == colour:
                    score += 1
                elif array[x][y] == opponent:
                    score -= 1
        return score

    # Less simple but still simple heuristic. Weights corners and edges as more
    def betterHeuristic(self, array, player):
        score = 0
        # Set player and opponent colours
        if player != 0:
            colour = "w"
            opponent = "b"
        else:
            colour = "b"
            opponent = "w"
        # Go through all the tiles
        for x in range(8):
            for y in range(8):
                add=betterHeuristicMatrix[x][y]
                if array[x][y] == colour:
                    score += add
                elif array[x][y] == opponent:
                    score -= add
        return score

    # Heuristic that weights corner tiles and edge tiles as positive, adjacent to corners (if the corner is not yours) as negative
    # Weights other tiles as one point
    def decentHeuristic(self, array, player):
        score = 0
        # Set player and opponent colours
        if player != 0:
            colour = "w"
            opponent = "b"
        else:
            colour = "b"
            opponent = "w"

        # Go through all the tiles
        for x in range(8):
            for y in range(8):
                # Normal tiles worth 1
                add = decentHeuristicMatrix[x][y]
                if array[x][y] == colour:
                    score += add
                elif array[x][y] == opponent:
                    score -= add
        return score

    # Seperating the use of heuristics for early / mid / late game.
    def dynamicHeuristic(self, array, player):
        if moves <= 8:
            numMoves = 0
            for x in range(8):
                for y in range(8):
                    if self.valid(array, player, x, y):
                        numMoves += 1
            return numMoves + self.decentHeuristic(array, player)
        elif moves <= 52 and self.checkCorner(array)<2:
            return self.decentHeuristic(array, player)
        elif moves <= 58 or self.checkCorner(array)<4:
            return (2 * self.decentHeuristic(array, player) + 3 * self.simpleHeuristic(array,player)) / 5
        else:
            return self.simpleHeuristic(array, player)

    # Checks if a move is valid for a given array.
    def valid(self, array, player, x, y):
        # Sets player colour
        if player == 0:
            colour = "b"
        else:
            colour = "w"

        # If there's already a piece there, it's an invalid move
        if array[x][y] is not None:
            return False

        else:
            # Generating the list of neighbours
            neighbour = False
            neighbours = []
            for i in range(max(0, x - 1), min(x + 2, 8)):
                for j in range(max(0, y - 1), min(y + 2, 8)):
                    if array[i][j] is not None:
                        neighbour = True
                        neighbours.append([i, j])
            # If there's no neighbours, it's an invalid move
            if not neighbour:
                return False
            else:
                # Iterating through neighbours to determine if at least one line is formed
                valid = False
                for neighbour in neighbours:

                    neighX = neighbour[0]
                    neighY = neighbour[1]

                    # If the neighbour colour is equal to your colour, it doesn't form a line
                    # Go onto the next neighbour
                    if array[neighX][neighY] == colour:
                        continue
                    else:
                        # Determine the direction of the line
                        deltaX = neighX - x
                        deltaY = neighY - y
                        tempX = neighX
                        tempY = neighY

                        while 0 <= tempX <= 7 and 0 <= tempY <= 7:
                            # If an empty space, no line is formed
                            if array[tempX][tempY] is None:
                                break
                            # If it reaches a piece of the player's colour, it forms a line
                            if array[tempX][tempY] == colour:
                                valid = True
                                break
                            # Move the index according to the direction of the line
                            tempX += deltaX
                            tempY += deltaY
                return valid

    # Assumes the move is valid
    def move(self, passedArray, x, y):
        # Must copy the passedArray so we don't alter the original
        array = deepcopy(passedArray)
        # Set colour and set the moved location to be that colour
        if board.player == 0:
            colour = "b"
        else:
            colour = "w"
        array[x][y] = colour

        # Determining the neighbours to the square
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if array[i][j] != None:
                    neighbours.append([i, j])

        # Which tiles to convert
        convert = []

        # For all the generated neighbours, determine if they form a line
        # If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
            neighX = neighbour[0]
            neighY = neighbour[1]
            # Check if the neighbour is of a different colour - it must be to form a line
            if array[neighX][neighY] != colour:
                # The path of each individual line
                path = []

                # Determining direction to move
                deltaX = neighX - x
                deltaY = neighY - y

                tempX = neighX
                tempY = neighY

                # While we are in the bounds of the board
                while 0 <= tempX <= 7 and 0 <= tempY <= 7:
                    path.append([tempX, tempY])
                    value = array[tempX][tempY]
                    # If we reach a blank tile, we're done and there's no line
                    if value == None:
                        break
                    # If we reach a tile of the player's colour, a line is formed
                    if value == colour:
                        # Append all of our path nodes to the convert array
                        for node in path:
                            convert.append(node)
                        break
                    # Move the tile
                    tempX += deltaX
                    tempY += deltaY

        # Convert all the appropriate tiles
        for node in convert:
            array[node[0]][node[1]] = colour

        return array

    def checkCorner(self, array):
        count = 0
        for i in [0,7]:
            for j in [0,7]:
                if(array[i][j]):
                    count+=1
        return count
    
    def selectLevel(self, level):
        self.level = level
    
# Method for drawing the gridlines
def drawGridBackground(outline=False):
    # If we want an outline on the board then draw one
    if outline:
        screen.create_rectangle(50, 50, 450, 450, outline="#111")

    # Drawing the intermediate lines
    for i in range(7):
        lineShift = 50 + 50 * (i + 1)

        # Horizontal line
        screen.create_line(50, lineShift, 450, lineShift, fill="#111")

        # Vertical line
        screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

    screen.update()

# When the user clicks, if it's a valid move, make the move
def clickHandle(event):
    xMouse = event.x
    yMouse = event.y
    if running:
        if xMouse >= 450 and yMouse <= 50:
            screen.delete(tkinter.ALL)
            runMenu()
        elif xMouse <= 50 and yMouse <= 50:
            playGame(board.humanTurn, board.level)
        else:
            # Is it the player's turn?
            if board.player == board.humanTurn:
                # Delete the highlights
                x = int((event.x - 50) / 50)
                y = int((event.y - 50) / 50)
                # Determine the grid index for where the mouse was clicked

                # If the click is inside the bounds and the move is valid, move to that location
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board.valid(board.array, board.player, x, y):
                        board.boardMove(x, y)
    else:
        # Difficulty clicking
        if 300 <= yMouse <= 350:
            # One star
            if 25 <= xMouse <= 155:
                playGame(0,1)
            # Two star
            elif 180 <= xMouse <= 310:
                playGame(0,2)
            # Three star
            elif 335 <= xMouse <= 465:
                playGame(0,3)
        if 400 <= yMouse <= 450:
            # One star
            if 25 <= xMouse <= 155:
                playGame(1,1)
            # Two star
            elif 180 <= xMouse <= 310:
                playGame(1,2)
            # Three star
            elif 335 <= xMouse <= 465:
                playGame(1,3)

def keyHandle(event):
    symbol = event.keysym
    if symbol.lower() == "r":
        playGame()
    elif symbol.lower() == "q":
        root.destroy()

def create_ingame_buttons():
    # Restart button
    # Background/shadow
    screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
    screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

    # Arrow
    screen.create_arc(5, 5, 45, 45, fill="#000088", width="2", style="arc", outline="white", extent=300)
    screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

    # Quit button
    # Background/shadow
    screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
    screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")

    # "X"
    screen.create_line(455, 5, 495, 45, fill="white", width="3")
    screen.create_line(495, 5, 455, 45, fill="white", width="3")

def runMenu():
    global running
    running = False

    # Title and shadow
    screen.create_text(250, 203, anchor="center", text="Othello", font=("Consolas", 50), fill="#aaa")
    screen.create_text(250, 200, anchor="center", text="Othello", font=("Consolas", 50), fill="#fff")
    screen.create_text(75, 280, anchor="center", text="Go 1st", font=("Consolas", 20), fill="#fff")

    # Creating the difficulty buttons
    for i in range(3):
        # Background
        screen.create_rectangle(25 + 155 * i, 310, 155 + 155 * i, 355, fill="#000", outline="#000")
        screen.create_rectangle(25 + 155 * i, 300, 155 + 155 * i, 350, fill="#111", outline="#111")
        spacing = 130 / (i + 2)
        for x in range(i + 1):
            # Star with double shadow
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 325, anchor="center", text="\u2605",
                               font=("Consolas", 25), fill="#b29600")
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 325, anchor="center", text="\u2605",
                               font=("Consolas", 25), fill="#b29600")
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 325, anchor="center", text="\u2605",
                               font=("Consolas", 25), fill="#ffd700")
    
    screen.create_text(75, 380, anchor="center", text="Go 2nd", font=("Consolas", 20), fill="#fff")
    for i in range(3):
        # Background
        screen.create_rectangle(25 + 155 * i, 410, 155 + 155 * i, 455, fill="#000", outline="#000")
        screen.create_rectangle(25 + 155 * i, 400, 155 + 155 * i, 450, fill="#111", outline="#111")
        spacing = 130 / (i + 2)
        for x in range(i + 1):
            # Star with double shadow
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 425, anchor="center", text="\u2605",
                               font=("Consolas", 25), fill="#b29600")
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 425, anchor="center", text="\u2605",
                               font=("Consolas", 25), fill="#b29600")
            screen.create_text(25 + (x + 1) * spacing + 155 * i, 425, anchor="center", text="\u2605",
                               font=("Consolas", 25), fill="#ffd700")
    screen.update()

def playGame(turn, level):
    global board, running
    running = True
    screen.delete(tkinter.ALL)
    create_ingame_buttons()
    board = 0

    # Draw the background
    drawGridBackground()

    # Create the board and update it
    board = PvEBoard(turn)
    board.selectLevel(level)
    board.update()

def main():
    runMenu()

    # Binding, setting
    screen.bind("<Button-1>", clickHandle)
    screen.bind("<Key>", keyHandle)
    screen.focus_set()

    # Run forever
    root.wm_title("Othello")
    root.mainloop()


if __name__ == '__main__':
    main()
