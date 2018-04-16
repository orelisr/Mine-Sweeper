'''
* Student name: Orel Israeli
* Course Exercise Group: 01
* Exercise name: ex7.py
'''
import random
import turtle
import argparse  # mandatory


def recorsConvertor(a, n):
    '''
   This function converts nunbers to binary/octal/decimal etc..
   the function print the numbers in reverse
   the function can't get negative numbers

   Keyword arguments:
   a - number
   n - basis number
   return: no outout
   '''
    if a != 0:
        temp = a % n
        print temp
        a = a / n
        recorsConvertor(a, n)


class Sierpinski(object):

    def __init__(self):
        '''
        This function opens screen and create turtle

        Keyword arguments:
        no args
        return: no outout
        '''
        self.window = turtle.Screen()
        self.sierpinski_turtle = turtle.Turtle()
        self.sierpinski_turtle.speed(0)

    def draw_sierpinski(self, length, depth):
        """
        draws a sierpinski tree
        :param length: the length of the base of the all tree
        :param depth: the depth of the tree recursion
        :return:
        """
        # I used stackOverflow for this mission
        # in case depth==0
        if depth == 0:
            for i in range(0, 3):
                self.sierpinski_turtle.fd(length)
                self.sierpinski_turtle.left(120)
        # in case depth!=0, keep draw and call draw_sierpinski again
        else:
            self.draw_sierpinski(length / 2, depth - 1)
            self.sierpinski_turtle.fd(length / 2)
            self.draw_sierpinski(length / 2, depth - 1)
            self.sierpinski_turtle.bk(length / 2)
            self.sierpinski_turtle.left(60)
            self.sierpinski_turtle.fd(length / 2)
            self.sierpinski_turtle.right(60)
            self.draw_sierpinski(length / 2, depth - 1)
            self.sierpinski_turtle.left(60)
            self.sierpinski_turtle.bk(length / 2)
            self.sierpinski_turtle.right(60)

    def finish_draw(self):
        '''
        This function closes the screen

        Keyword arguments:
        no args
        return: no outout
        '''
        self.window.bye()

    def save_draw(self, length, depth):
        '''
        This function saves the turtle

        Keyword arguments:
        nameSav = name of the turtle file
        return: no outout
        '''
        self.sierpinski_turtle.hideturtle()
        nameSav = ("sierpinski_%d_%d" % (length, depth)) + ".svg"
        self = turtle.getscreen().getcanvas()
        self.postscript(file=nameSav)


class GameStatus(object):
    """Enum of possible Game statuses."""
    __init__ = None
    NotStarted, InProgress, Win, Lose = range(4)


class BoardCell(object):
    """
    Represents a cell in the minesweeper board game and is current status in the game

    """

    def __init__(self):
        """
        Initializes a board cell with no neighboring mines and status is hidden

        Args:
            None

        Returns:
            None (alters self)
        """

        self.status = "hidden"
        # 0 represents not mine, 1 represents mine
        self.isMine = 0
        self.val = 0

    def is_mine(self):
        """
        returns true if this cell contains a mine false otherwise

        Args:
            None

        Returns:
            true if this cell contains a mine false otherwise
        """
        # if cell is mine
        if self.isMine == 1:
            return True
        else:
            return False

    def is_hidden(self):
        """
        returns true if this cell is hidden false otherwise

        Args:
            None

        Returns:
            true if this cell is hidden false otherwise
        """
        if self.status == "hidden":
            return True
        else:
            return False

    def get_cell_value(self):
        """
        returns the number of adjacent mines

        Args:
            None

        Returns:
            the number of adjacent mines in int or the charcter '*' if this cell is a mine
        """
        if self.is_mine() == True:
            return '*'
        else:
            return self.val

    def uncover_cell(self):
        """
        uncovers this cell. when a cell is uncovered then is status is the value of the mines near it or * if the
        cell is a mine
        Args:
            None

        Returns:
            None (alters self)

        """
        self.status = self.get_cell_value()

    def update_cell_value(self, cellValue):
        """
        updates the value of the how many neighboring mines this cell has

        Args:
            numOfNearMine - the new number of the how many neighboring mines this cell has

        Returns:
            None (alters self)
        """
        numOfNearMine = cellValue
        self.val = numOfNearMine
        if self.val == '*':
            self.isMine = 1

    def add_one_to_cell_value(self):
        """
        adds one to the number of near mine

        Args:
            None

        Returns:
            None (alters self)
        """
        # add 1 to cell val
        if self.is_mine() == False:
            self.val = int(self.val) + 1

    def set_has_mine(self):
        """
        changes this cell to a cell with a mine in it

        Args:
           None

        Returns:
            None (alters self)
        """
        self.update_cell_value('*')
        self.isMine = 1


class Board(object):
    """Represents a board of minesweeper game and its current progress."""

    def __init__(self, rows, columns):
        """Initializes an empty hidden board.

        The board will be in the specified dimensions, without mines in it,
        and all of its cells are in hidden state.

        Args:
            rows: the number of rows in the board
            columns: the number of columns in the board

        Returns:
            None (alters self)
        """
        self.numRows = rows
        self.numColumns = columns
        # starts a board with row*col board cells
        self.board = [[BoardCell() for _ in range(columns)] for _ in range(rows)]

    def neighbors(self, row, column):
        """
        return valid neighbors of cell

        Args:
            neighborsPositions: diffrent positions
            neighbours: neighbours positions around cell
            validNeighbours: neighbours valid positions around cell

        Returns:
            valid neighbours
        """
        neighborsPositions = ((-1, -1), (-1, 0), (-1, 1),
                              (0, -1), (0, 1),
                              (1, -1), (1, 0), (1, 1))
        neighbours = ()
        for (i, j) in neighborsPositions:
            neighbours = neighbours + ((row + i, column + j),)
        validNeighbours = []
        for (r, c) in neighbours:
            # check if position is in range of board
            if (r >= 0 and c >= 0 and r < self.numRows and c < self.numColumns):
                validNeighbours.append((r, c))
        # return validNeighbours positions
        return validNeighbours

    def put_mines(self, mines, seed=None):
        """Randomly scatter the requested number of mines on the board.

        At the beggining, all cells on the board are hidden and with no mines
        at any of them. This method scatters the requested number of mines
        throughout the board randomly, only if the board is in the beginning
        state (as described here). A cell can host only one mine.
        This method not only scatters the mines on the board, but also updates
        the cells around it (so they will hold the right digit).

        Args:
            mines: the number of mines to scatter
            seed: the seed to give the random function. Default value None

        Returns:
            None (alters self)

        """
        listOfCellsIndex = [(numRow, numCol) for numRow in range(self.numRows) for numCol in range(self.numColumns)]
        # randomly choosing cells in the board to place mines in
        random.seed(seed)
        listOfMineCells = random.sample(listOfCellsIndex, mines)
        # You need to implement the rest
        for i in listOfMineCells:
            x = i[0]
            y = i[1]
            # set position (x,y) as mine
            self.board[x][y].set_has_mine()
            # add one to neighbors cell value
            for r, c in self.neighbors(x, y):
                self.board[r][c].add_one_to_cell_value()

    def print_board(self):
        """prints the board according to the game format
            DO NOT CHANGE ANYTHING IN THIS FUNCTION!!!!!!!
        Args:
            None
        Returns:
            None
        """
        # creates the printing format
        printFormatString = "%-2s " * self.numColumns
        printFormatString += "%-2s"
        # prints the first line of the board which is the line containing the indexes of the columns
        argList = [" "]
        argList.extend([str(i) for i in range(self.numColumns)])
        print printFormatString % tuple(argList)
        # goes over the board rows and prints each one
        for i in range(self.numRows):
            argList = [str(i)]
            for j in range(self.numColumns):
                if self.board[i][j].is_hidden():
                    argList.append("H")
                else:
                    argList.append(str(self.board[i][j].get_cell_value()))
            print printFormatString % tuple(argList)

    def load_board(self, lines):
        """Loads a board from a sequence of lines.

        This method is used to load a saved board from a sequence of strings
        (that usually represent lines). Each line represents a row in the table
        in the following format:
            XY XY XY ... XY
        Where X is one of the characters: 0-8, * and Y is one of letters: H, S.
        0-8 = number of adjusting mines (0 is an empty, mine-free cell)
        * = represents a mine in this cell
        H = this cell is hidden

        The lines can have multiple whitespace of any kind before and after the
        lines of cells, but between each XY pair there is exactly one space.
        Empty or whitespace-only lines are possible between valid lines, or after/before them.
        It is safe to assume that the values are correct (the number represents the number of mines around
        a given cell) and the number of mines is also legal.

        Note that this method doesn't get the first two rows of the file (the
        dimensions) on purpose - they are handled in __init__.

        Args:
            lines: a sequence (list or tuple) of lines with the above restrictions
            cell: each cell in lines arr (string)
            value: cell val (char)
            status: cell status (char)

        Returns:
            None (alters self)
        """
        board = self.board
        # loop over board rows
        for i in range(0, self.numRows):
            # loop over board columns
            for j in range(0, self.numColumns):
                cell = lines[0]
                value = cell[0]
                status = cell[1]
                # update cell val
                if value == '*':
                    self.board[i][j].set_has_mine()
                else:
                    self.board[i][j].update_cell_value(int(value))
                # update cell status
                if status == 'S':
                    self.board[i][j].uncover_cell()
                # remove item from lines arr
                lines.remove(lines[0])

    def get_value(self, row, column):
        """Returns the value of the cell at the given indices.

        The return value is a string of one character, out of 0-8 + '*'.

        Args:
            row: row index (integer)
            column: column index (integer)

        Returns:
            If the cell is empty and has no mines around it, return '0'.
            If it has X mines around it (and none in it), return 'X' (digit
            character between 1-8).
            If it has a mine in it return '*'.

        """
        # if cell val is 0
        if (self.board[row][column].get_cell_value() == 0):
            return 0
        # if cell is mine
        elif (self.board[row][column].get_cell_value() == '*'):
            return '*'
        # return number of mines neighbors
        else:
            return self.board[row][column].get_cell_value()

    def is_hidden(self, row, column):
        """Returns if the given cell is in hidden or uncovered state.

        Args:
            row: row index (integer)
            column: column index (integer)

        Returns:
            'H' if the cell is hidden, or 'S' if it's uncovered (can be seen).
        """
        if ((self.board[row][column].is_hidden()) == True):
            return 'H'
        else:
            return 'S'

    def uncover(self, row, column):
        """Changes the status of a cell from hidden to seen.

        Args:
            row: row index (integer)
            column: column index (integer)

        Returns:
            None (alters self)
        """
        self.board[row][column].uncover_cell()


class Game(object):
    """Handles a game of minesweeper by supplying UI to Board object."""

    def __init__(self, board):
        """Initializes a Game object with the given Board object.

        The Board object can be a board in any given status or stage.

        Args:
            board: a Board object to continue (or start) playing.

        Returns:
            None (alters self)
        """
        self.gameBoard = board

    def get_status(self):
        """Returns the current status of the game.

        The current status of the game is as followed:
            NotStarted: if all cells are hidden.
            InProgress: if some cells are hidden and some are uncovered, and
            no cell with a mine is uncovered.
            Lose: a cell with mine is uncovered.
            Win: All non-mine cells are uncovered, and all mine cells are
            covered.
        Args:
        numOfHiddenCells: number of hidden cells of board (int)
        numOfAllCells: number of board cells (int)
        numOfMines: number of mines (int)

        Returns:
            one of GameStatus values (doesn't alters self)

        """
        numOfHiddenCells = 0
        numOfAllCells = (self.gameBoard.numColumns) * (self.gameBoard.numRows)
        numOfMines = 0
        for i in range(0, self.gameBoard.numRows):
            for j in range(0, self.gameBoard.numColumns):
                if self.gameBoard.is_hidden(i, j) == 'H':
                    numOfHiddenCells += 1
                if self.gameBoard.get_value(i, j) == '*':
                    numOfMines += 1
                if self.gameBoard.get_value(i, j) == '*' and self.gameBoard.is_hidden(i, j) == 'S':
                    # return "Lose" if mine is uncover
                    return GameStatus.Lose
        if (numOfHiddenCells == numOfAllCells):
            # return "NotStarted" if all cells are coverd
            return GameStatus.NotStarted
        elif (numOfAllCells - numOfMines) == (numOfAllCells - numOfHiddenCells):
            # return "Win" if all not-mine cells are uncovered
            return GameStatus.Win
        else:
            return GameStatus.InProgress

    def make_move(self, row, column):
        """Makes a move by uncovering the given cell and unrippling it's area.

        The move flow is as following:
        1. Uncover the cell
        2. If the cell is a mine - return
        3. if the cell is not a mine, ripple (if value = 0) and uncover all
            adjacent cells, and recursively on this cells if needed (if they are empty cells)

        Args:
            row: row index (integer)
            column: column index (integer)

        Returns:
            the cell's value.
        """
        self.gameBoard.uncover(row, column)
        # if cell is mine
        if self.gameBoard.get_value(row, column) == '*':
            return
        elif self.gameBoard.get_value(row, column) != 0:
            return
        # if cell val is 0
        elif self.gameBoard.get_value(row, column) == 0:
            # loop neighbors of cell
            # in a recorsive way uncover cells with val 0 and status H
            for i, j in self.gameBoard.neighbors(row, column):
                if self.gameBoard.is_hidden(i, j) == 'H':
                    # call make move again
                    self.make_move(i, j)

    def run(self):
        """Runs the game loop.

        At each turn, prints the following:
            current state of the board
            game status
            available actions
        And then wait for input and act accordingly.
        More details are in the project's description.

        Args:
        option: user's selection (char)
        status: enum status
        statusString: string of enum value
        row: number of row (int)
        column: number of column (int)



        Returns:
            None
        """
        option = '0'
        while option != '1':
            # call print_board()
            self.gameBoard.print_board()
            # convert enum to string
            status = vars(GameStatus).values().index(self.get_status())
            statusString = (vars(GameStatus).keys()[status])
            # print game status
            print "Game status: " + statusString
            # check if status is lose or win
            if self.get_status() == GameStatus.Lose or self.get_status() == GameStatus.Win:
                print "Available actions: (1) Exit"
            # status is inProgress or notStarted
            else:
                print "Available actions: (1) Exit | (2) Move"
            option = raw_input("Enter selection:\n ")
            # if potion ==1, print "Goodbye :)" and close the program
            if option == '1':
                print "Goodbye :)"
                return
            # if option==2' keep playing
            elif option == '2' and (
                    self.get_status() == GameStatus.InProgress or self.get_status() == GameStatus.NotStarted):  # and not win/lose status:
                move = raw_input("Enter row then column (space separated): \n")
                row, column = move.split()
                row = int(row)
                column = int(column)
                # check if selection valid
                if row < 0 or row >= self.gameBoard.numRows or column < 0 or column >= self.gameBoard.numColumns or self.gameBoard.is_hidden(
                        row, column) == 'S':
                    print "Illegal move values"
                else:
                    self.make_move(row, column)
            else:
                print "Illegal choice"


def main():
    """Starts the game by parsing the arguments and initializing.
    Act according to the exercise explanation

    Regarding mine swiper:
    If an input file argument was given, the file is loaded (even if other
    legal command line argument were given).

    If input file wasn't given, create a board with the rows/columns/mines

    In case both an input file was given and other parameters, ignore the
    others and use only the input file.
    For example, in case we get "-i sample -r 2 -c 2" just use
    the input file and ignore the rest (even if there are missing parameters).

    Args:
    turtleObject: Sierpinski object
    board: Board object
    twice: temp parameter (temp)
    rows: number of rows (int)
    columns: number of columns (int)
    arrOfCells: array of cells (strings)
    parametersEachLine: cells each line (strings)
    numberOfMines: number of mines on board (int)

    Returns:
        None

    """
    # argparse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest="p", type=int)
    parser.add_argument('-a', dest="a", type=int)
    parser.add_argument('-n', dest="n", type=int)
    parser.add_argument('-d', dest="d", type=int)
    parser.add_argument('-l', dest="l", type=int)
    parser.add_argument('-r', dest="r", type=int)
    parser.add_argument('-c', dest="c", type=int)
    parser.add_argument('-m', dest="m", type=int)
    parser.add_argument('-i', dest="i", type=argparse.FileType("r"))
    parser.add_argument('-s', dest="s", type=float)
    args = parser.parse_args()

    # call recorsConvertor
    if args.p == 1:
        recorsConvertor(args.a, args.n)
    # create Sierpinski turtle
    elif args.p == 2:
        # create Sierpinski object
        turtleObject = Sierpinski()
        # call draw_sierpinski function
        turtleObject.draw_sierpinski(args.l, args.d)
        # call save_draw function
        turtleObject.save_draw(args.l, args.d)
        # call finish_draw function
        turtleObject.finish_draw()
    # if option ==3
    else:
        # check if parameters valid
        if ((1 <= args.r <= 20 and 2 <= args.c <= 50) and args.m <= (((args.r) * (args.c)) - 1)):
            # create board object
            board = Board(args.r, args.c)
            # call put mines function
            board.put_mines(args.m, args.s)
            # create game object
            gameBoard = Game(board)
            # call run function
            gameBoard.run()
        # if args.i is not null
        elif args.i != None:
            twice = 0
            rows = 0
            columns = 0
            # arry of cells
            arrOfCells = []
            # loop each line in board file
            for line in args.i:
                line = line.replace('\n', '')
                line = line.strip()
                parametersEachLine = line.split(' ')
                for cell in parametersEachLine:
                    if cell != '':
                        # add cells to arrOfCells
                        arrOfCells.append(cell)
            # casting from char to int
            rows = int(arrOfCells[0])
            columns = int(arrOfCells[1])
            # remove first two lines
            for i in arrOfCells:
                arrOfCells.remove(arrOfCells[0])
                twice = twice + 1
                if twice == 2:
                    break
            # check if values valid
            if ((1 <= rows <= 20 and 2 <= columns <= 50) and args.m <= (((rows) * (columns)) - 1)):
                # create board object
                board = Board(rows, columns)
                # call load board func
                board.load_board(arrOfCells)
                # create game object
                gameBoard = Game(board)
                # number of mines
                numberOfMines = 0
                for i in range(0, board.numRows):
                    # loop over board columns
                    for j in range(0, board.numColumns):
                        if board.get_value(i, j) == '*':
                            numberOfMines += 1
                # check if number of mines is valid
                if (numberOfMines <= ((rows * columns) - 1)):
                    # call run func
                    gameBoard.run()
                else:
                    print "Illegal board"
            # print error if parameters are not valid
            else:
                print "Illegal board"
                return
        else:
            print "Illegal board"
            return


if __name__ == '__main__':
    main()

# ADD NO CODE OUTSIDE MAIN() OR OUTSIDE A FUNCTION/CLASS (NO GLOBALS), EXCEPT IMPORTS WHICH ARE FINE

