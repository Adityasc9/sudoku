"""
STORE TIME
game finish by user and not by solve button
hashing passwords
range of difficulties: 5 easy 5 normal 5 hard
"""

'''Imports'''
import pygame  # Pygame is the GUI module I chose to use becase of familiarity
import time  # Time is used for keeping track of how long the user has been playing a board for
from elements import Button  # Elements is my python file containing the element classes
from elements import InputBox
import sudoku_solver  # Sudoku_solver is my python file containing all the functions used in solving the boards
import re  # RE is a libary for regular expressions. I will use this for password complexities
import sqlite3 as sql  # SQLite 3 is used for communicating between python and databases
import random  # I will use random to generate a random 16 character salt or password security

conn = sql.connect("data.db")
'''This creates the database if it does not already exist. If it exists, sql establishes a connection with the datbase.'''
db = conn.cursor()
db.execute(
    'CREATE TABLE IF NOT EXISTS "users" (\n'  # This command creates a users table if it does not already  exist.
    '	"username"	TEXT NOT NULL,\n'  # creates username field which cannot be null
    '	"password"	TEXT NOT NULL,\n'  # creates password field which cannot be null
    '	"salt"	TEXT NOT NULL,\n'  # creates a salt field where I will store the random salt of the password
    '	PRIMARY KEY("username")\n'')')  # username is the primary key of this table

db.execute(
    'CREATE TABLE IF NOT EXISTS "defaultBoards" (\n'  # This command creates a defaultBoards table if it does not already exist.
    '	"BoardNumber" INTEGER NOT NULL,\n'  # BoardNumber is an integer which cannot be null
    '	"Board"	TEXT NOT NULL,\n'  # Creates Board field which cannot be null
    '	"Difficulty" TEXT,\n'  # creates difficulty field
    '	PRIMARY KEY("BoardNumber"))')  # BoardNumber is the primary key of this table

allBoards = ['041089000\n052003847\n080502039\n205307001\n807054003\n030900576\n600430950\n500076310\n413200700',
             '083070901\n970830500\n001209807\n610703090\n000916408\n798000610\n009057046\n105024080\n407100052',
             '509002063\n170480002\n004605017\n008021605\n023906100\n605030720\n090360501\n067500290\n850240070',
             '103700024\n702041060\n009023018\n396000870\n000978106\n870305090\n007409603\n930650200\n065030907',
             '008004796\n750900801\n094781000\n000018409\n301609020\n946050130\n070462305\n415090070\n200100084',
             '795048000\n201009407\n040710050\n002004700\n000532000\n006800900\n010023070\n504100603\n000460821',
             '006018030\n703020608\n050060740\n500002004\n008691500\n100400002\n081070020\n605040107\n070180300',
             '790681200\n100200000\n002004006\n903120040\n010000020\n020048107\n800400500\n000003009\n001569072',
             '507601400\n000090070\n100070002\n013786200\n008040600\n009153840\n800030009\n060010000\n002509708',
             '026040708\n870300900\n100800040\n709106000\n030485090\n000709402\n090003001\n007004029\n205010370',
             '058000203\n000009048\n040080507\n034900000\n010704080\n000003750\n302090070\n190800000\n405000920',
             '805000000\n160200000\n740600020\n000476052\n036090180\n570381000\n080003075\n000007013\n000000809',
             '004300051\n630000072\n072040009\n040200003\n000090000\n200005080\n700020390\n820000046\n490007200',
             '309000000\n004000060\n206000300\n900060250\n600910000\n000073000\n000602040\n000000008\n020048001',
             '108000000\n040007000\n503900000\n720090300\n030060010\n006010094\n000004207\n000500040\n000000801',
             '003020600\n900305001\n001806400\n008102900\n700000008\n006708200\n002609500\n800203009\n005010300',
             '000000907\n000420180\n000705026\n100904000\n050000040\n000507009\n920108000\n034059000\n507000000',
             '200080300\n060070084\n030500209\n000105408\n000000000\n402706000\n301007040\n720040060\n004010003',
             '001900003\n900700160\n030005007\n050000009\n004302600\n200000070\n600100030\n042007006\n500006800',
             '000900002\n050123400\n030000160\n908000000\n070000090\n000000205\n091000050\n007439020\n400007000',
             '480006902\n002008001\n900370060\n840010200\n003704100\n001060049\n020085007\n700900600\n609200018',
             '043080250\n600000000\n000001094\n900004070\n000608000\n010200003\n820500000\n000000005\n034090710',
             '100920000\n524010000\n000000070\n050008102\n000000000\n402700090\n060000000\n000030945\n000071006',
             '020810740\n700003100\n090002805\n009040087\n400208003\n160030200\n302700060\n005600008\n076051090',
             '030050040\n008010500\n460000012\n070502080\n000603000\n040109030\n250000098\n001020600\n080060020']  # a list of every board to store. There is too much to show in the word document

db.execute(
    'CREATE TABLE IF NOT EXISTS "BoardUserLink" (\n'  # This command creates a BoardUserLink table  if it does not already exist.
    '	"username"	TEXT NOT NULL,\n'  # creates username field which cannot be null
    '	"BoardNumber"	INTEGER NOT NULL,\n'  # creates BoardNumber field which cannot be null
    '	"Completed"	TEXT NOT NULL,\n'  # creates Completed field which cannot be null
    '	"Time"	INTEGER,\n'  # Time is an integer and will be stored in seceonds
    '	"SavedBoard"	TEXT,\n'  # creates SavedBoard field.
    '	"hintCount"	INTEGER,\n'  # creates  hintCount field
    '	PRIMARY KEY("username","BoardNumber"),\n'  # username and BoardNumber make up a composite primary key
    '	FOREIGN KEY("username") REFERENCES "users"("username"),\n'  # This makes username from  the users table a foreign key in the boardUserLink table.
    '	FOREIGN KEY("BoardNumber") REFERENCES "defaultBoards"("BoardNumber")\n'  # This makes BoardNumber from  the defaultBoards table a foreign key in the boardUserLink table.
    ')')

count = db.execute("SELECT COUNT(*) FROM defaultBoards").fetchone()[
    0]  # check to see if defaultBoards is an empty table
if count == 0:  # if table is empty, fill table with boards
    for boardNo in range(1, len(allBoards) + 1):  # for every BoardNo in the allBoards list:

        if 0 < boardNo < 6:  # first 5 boards are easy
            difficulty = 'Easy'
        elif 5 < boardNo < 11:  # next 5 boards are medium
            difficulty = 'Medium'
        elif 10 < boardNo < 16:
            difficulty = 'Hard'  # next 5 boards are hard
        else:
            difficulty = 'Random'  # last 10 boards are of random difficulties

        db.execute(
            f"INSERT INTO defaultBoards ('BoardNumber', 'Board', 'Difficulty') VALUES ({boardNo}, '{allBoards[boardNo - 1]}', '{difficulty}')")
        # inserting each boardNumber, Board and the Difficulty on the table
        conn.commit()  # commiting changes

'''Main'''
HEIGHT = 550  # Height of the window. Constant value
WIDTH = 900  # Width of the window. Constant value
BACKGROUND_COLOR = (255, 255, 255)
pygame.init()  # initialise pygame

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku!")


def main():  # This is the start point of the program. This function includes the login system.
    window.fill(BACKGROUND_COLOR)  # Fill the entire screen white
    pygame.font.init()
    font = pygame.font.SysFont('Calluna', 100)
    text = font.render("Sudoku!", True, pygame.Color('burlywood1'))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))  # blit renders text

    pygame.display.update()
    username = InputBox(400, 250, 200, 32, 'username: ')  # prompt for this Inputbox is username:
    password = InputBox(400, 300, 200, 32, 'password: ', textType='password')  # prompt for this Inputbox is password:
    input_boxes = [username, password]
    registerButton = Button(500, 350, 100, 32, 'Register')
    loginButton = Button(400, 350, 70, 32, 'Login')

    while True:  # While on main screen
        for event in pygame.event.get():  # an event can include anything that happens while on the GUI such as mouse movements and switching tabs
            if event.type == pygame.QUIT:  # if the quit window button is clicked, quit program
                quit()

            for box in input_boxes:
                box.handle_event(event)  # Handles any event given to it.

            registerButton.handle_event(event)

            if registerButton.active:  # If register button is clicked:
                registerButton.active = False
                register(username.userInput,
                         password.userInput)  # Passes the username and password to register function.

            loginButton.handle_event(event)
            if loginButton.active:  # If login butotn is clicked:
                loginButton.active = False

                if login(username.userInput,
                         password.userInput):  # Passes the username and password to the login function which returns true if login is successful
                    usermenu(username.userInput)  # Passes username to usermenu so that user can access their profile

        for box in input_boxes:
            box.update(window)  # resizes the input box if text is too long

        for box in input_boxes:
            box.draw(window)  # renders the input boxes to the screen

        registerButton.draw(window)  # renders the buttons to the screen
        loginButton.draw(window)
        pygame.display.update()  # updates display


def login(u, p):  # login function which takes in username and password
    if len(u) == 0 or len(p) == 0:  # if username or password is empty: prompt user to fill fields
        font = pygame.font.SysFont('ComicSans MS', 20)
        text = font.render('Please complete all fields', True, (0, 0, 0))
        window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
        pygame.display.update()
        return

    db.execute(f"SELECT username FROM users")  # selects all the usernames from the table users
    UsersOnDb = db.fetchall()  # These are all the usernames in a list of tuples
    exists = False
    for tup in UsersOnDb:  # for every tuple in the list
        if u in tup:  # If username is in tuple, username exists
            exists = True
            break  # if username if found, quit loop

    if exists:
        passOnDB = db.execute(
            f"SELECT password from users WHERE username = '{u}'").fetchone()[
            0]  # Password for that username  is selected

        salt = db.execute(f"SELECT salt from users WHERE username = '{u}'").fetchone()[0]
        if hash(p + salt) == passOnDB:  # If hashed password the user enters is the same as the hashed password stored on the database, login sucessful
            return True

        else:  # password is incorrect
            font = pygame.font.SysFont('ComicSans MS', 20)
            text = font.render('Incorrect password.', True, (0, 0, 0))
            window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
            pygame.display.update()

    else:  # username does not exist on the database
        font = pygame.font.SysFont('ComicSans MS', 20)
        text = font.render('Username does not exist.', True, (0, 0, 0))
        window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
        pygame.display.update()


def hash(p):
    a = 5381  # prime hash multiplier
    for x in p:  # for every character in password,
        a = ((a << 5) + a) + ord(x)  # a = a left shifted by 5 + a + the ASCII value of the character in password
    return hex(a & 0xFFFFFFFF)  # return the hexadecimal value of a AND -1 (logical AND)


def register(u, p):  # Register function which takes in username and password
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"  # This is the regular expression a password must comply with to be valid
    pattern = re.compile(reg)
    if len(u) == 0 or len(p) == 0:  # If username and password is empty, user is prompted ot fill all the fields
        font = pygame.font.SysFont('ComicSans MS', 20)
        text = font.render('Please complete all fields', True, (0, 0, 0))
        window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
        pygame.display.update()
        return

    db.execute(f"SELECT username FROM users")  # all usernames are selected
    UsersOnDb = db.fetchall()
    exists = False
    for tup in UsersOnDb:  # for every tuple in the list
        if u in tup:  # If username is in tuple, username exists
            exists = True
            break  # if username if found, quit loop

    if exists:  # if username exists, prompt user to change username
        print('username already exists, please try again')
        font = pygame.font.SysFont('ComicSans MS', 20)
        text = font.render('username already exists, please try again.', True, (0, 0, 0))
        window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
        pygame.display.update()


    else:  # if username does not already exist:
        if re.search(pattern, p):  # if password complies with the regular expression
            salt = ''
            for x in range(16):
                char = str(chr(random.randint(37, 129)))
                salt += char

            db.execute(f"INSERT INTO users(username, password, salt) VALUES ('{u}','{hash(p + salt)}', '{salt}')")
            # insert the new username, hashed password and the salt into the database. This may seem counter intuitive as I’m giving away
            # half the password to a potential hacker but using a salt means that I he will not be able to use a lookup rainbow table to
            # reverse hash the passwords easily.

            conn.commit()  # commit the changes to the database
            font = pygame.font.SysFont('ComicSans MS', 20)
            text = font.render('Successfully registered', True, (0, 0, 0))
            window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
            pygame.display.update()


        else:  # if password does not comply with the regular expression, user is given the requirements for a strong password
            font = pygame.font.SysFont('ComicSans MS', 17)
            text = font.render(
                "password should have at least: one uppercase letter, one lowercase letter, one number, one symbol(!#$...)",
                True, (0, 0, 0))
            window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear the previous text
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))
            pygame.display.update()
            return


'''User Menu'''

def merge(arr):
    if len(arr) > 1:  # if the length of each sub array is more than one
        lefta = arr[:len(arr)//2]  # split array from the start to the middle point
        righta = arr[len(arr)//2:]  # split array from the middle point to the end

        merge(lefta)  # recurse until each array only consists of 1 element
        merge(righta) # recurse until each array only consists of 1 element

        i = j = k = 0

        while i < len(lefta) and j < len(righta):  # while i is less than the length of left array and j is less than the length of the right array
            if lefta[i] < righta[j]:  # if the element at pointer of left array is less than the element at pointer of right array
                arr[k] = lefta[i]  # set array position k to the element at pointer of left array
                i+=1  # increment left pointer by 1

            else:  # if element at pointer of left array is greater than or equal to the elemet at pointer of right array
                arr[k] = righta[j]  # set array position k to the element at pointer of right array
                j+=1  # increment right pointer by 1

            k+=1  # increment k by one


        # run this while i is still less than the length of the left array
        while i < len(lefta):  # while i is less than the length of the left array
            arr[k] = lefta[i]  # set element at position k in array to the element at i in left array
            i+=1  # increment left pointer by 1
            k+=1  # increment k by 1

        # run this while j is still less than the length of the right array
        while j < len(righta):  # while j is less than the length of the right array
            arr[k] = righta[j]  # set element at position k in array to the element at j in right array
            j+=1  # increment right pointer by 1
            k+=1  # increment k by 1

        return arr  # return the sorted array

    else:  # already sorted
        return arr

def usermenu(u):  # usermenu takes in username of the user that logged in.
    window.fill(BACKGROUND_COLOR)  # entire screen is filled to display users profile
    font = pygame.font.SysFont('Soria', 60)
    text = font.render(f"{u}'s profile", True, pygame.Color('burlywood1'))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

    NBoardsCompleted = list(db.execute(
        f"SELECT BoardNumber FROM BoardUserLink WHERE username = '{u}' AND Completed = 'True' ORDER BY BoardNumber DESC").fetchall())  # selects all the board numbers which have been completed by the user

    font = pygame.font.SysFont('Soria', 35)
    if len(NBoardsCompleted) == 0:  # If no boards have been completed by user:
        NBoardsCompletedText = font.render(f"No boards have been completed by {u}", True, (0, 0, 0))
        window.blit(NBoardsCompletedText, (WIDTH // 2 - NBoardsCompletedText.get_width() // 2, 170))

    else:  # If boards have been completed by user:
        NBoardsCompleted = [x[0] for x in NBoardsCompleted]  # make a list of the first element from each tuple in NBoardsCompleted
        NBoardsCompleted = merge(NBoardsCompleted)  # sort list in ascending order using merge sort
        NBoardsCompleted = map(str, NBoardsCompleted)  # make every value in the list a string
        NBoardsCompletedText = font.render(f"Boards completed by {u}: {', '.join(NBoardsCompleted)}", True, (0, 0, 0))
        window.blit(NBoardsCompletedText, (WIDTH // 2 - NBoardsCompletedText.get_width() // 2, 170))

    NBoardsIncomplete = list(db.execute(
            f"SELECT BoardNumber FROM BoardUserLink WHERE username = '{u}' AND Completed = 'False' ORDER BY BoardNumber DESC").fetchall())  # select all the board numbers which have not been completed by the user
    if len(NBoardsIncomplete) == 0:  # If no boards have been started:
        NBoardsIncompleteText = font.render(f"No boards have been started", True, (0, 0, 0))
        window.blit(NBoardsIncompleteText, (WIDTH // 2 - NBoardsIncompleteText.get_width() // 2, 120))

    else:
        NBoardsIncomplete = [x[0] for x in NBoardsIncomplete]  # make a list of the first element from each tuple in NBoardsIncomplete
        NBoardsIncomplete = merge(NBoardsIncomplete)  # sort list in ascending order using merge sort
        NBoardsIncomplete = map(str, NBoardsIncomplete) # make every value in the list a string
        NBoardsIncompleteText = font.render(f"Incomplete boards: {', '.join(NBoardsIncomplete)}", True, (0, 0, 0))
        window.blit(NBoardsIncompleteText, (WIDTH // 2 - NBoardsIncompleteText.get_width() // 2, 120))

    NumberOfBoards = db.execute("SELECT COUNT(*) FROM defaultBoards").fetchone()[0]  # Select number of rows in defaultBoards
    NumberOfBoardsText = font.render(f"Number of available boards: {NumberOfBoards}", True,
                                     (0, 0, 0))  # displays the number of available boards
    window.blit(NumberOfBoardsText, (WIDTH // 2 - NumberOfBoardsText.get_width() // 2, 70))

    BoardsCompletedAlgo = list(db.execute(
        f"SELECT BoardNumber FROM BoardUserLink WHERE username = '{u}' AND Completed = 'SolvedWithAlgo' ORDER BY BoardNumber DESC").fetchall())  # select all boards which have been completed by algorithm

    if len(BoardsCompletedAlgo) > 0:  # if any boards have been completed by algorithm:
        BoardsCompletedAlgo = [x[0] for x in BoardsCompletedAlgo]  # make a list of the first element from each tuple in BoardsCompletedAlgo
        BoardsCompletedAlgo = merge(BoardsCompletedAlgo)
        BoardsCompletedAlgo = map(str, BoardsCompletedAlgo)  # make every value of the list a tring
        BoardsCompletedAlgoText = font.render(f"Boards completed by algorithm: {', '.join(BoardsCompletedAlgo)}", True,
                                              (0, 0, 0))  # display the board numbers solved by algorithm
        window.blit(BoardsCompletedAlgoText,
                    (WIDTH // 2 - BoardsCompletedAlgoText.get_width() // 2, 220))  # render text

    LaunchNumber = InputBox(600, 350, 32, 32, 'Enter board number to launch: ',
                            textType='int')  # creates an input box for user to enter board number to launch
    Launch = Button(WIDTH // 2 - 87 // 2, 450, 87, 32, 'Launch')
    pygame.display.update()

    LogOut = Button(805, 10, 86, 32, 'Logout')  # creates a log out button.

    while True:  # While on user menu
        for event in pygame.event.get():  # an event can include anything that happens while on the GUI such as mouse movements and switching tabs
            if event.type == pygame.QUIT:  # if the quit window button is clicked, quit program
                quit()

            Launch.handle_event(event)
            LaunchNumber.handle_event(event)
            LogOut.handle_event(event)

            if LogOut.active:  # if log out button is clicked, user is taken back to log in page
                main()

            if Launch.active:
                if LaunchNumber.userInput != '':
                    if 0 < int(LaunchNumber.userInput) <= NumberOfBoards:
                        BoardNumber = LaunchNumber.userInput  # boardNumber to launch is user input number

                        try:  # try launching a board number,
                            # if the board number has already been played by that user,
                            # an error is generated as inserting the same board number and username in one row causes composite key to be ununique
                            board = db.execute(f'SELECT Board FROM "main"."defaultBoards" WHERE '
                                               f'BoardNumber = {BoardNumber}').fetchone()[0]  # select the board from default boards where board number is the user inputted board number

                            board = [list(map(int, line)) for line in board.splitlines()]  # splits the text board into a 2d array.
                            og_board = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]  # og board is the same as the unedited board
                            db.execute(f'INSERT INTO "main"."BoardUserLink" ("username", "BoardNumber", "Completed", "Time", "hintCount") '
                                       f'VALUES ("{u}", {BoardNumber}, "False", 0, 0)')  # insert a new row for the game with a uniqe primary key of this username and board number

                            conn.commit()  # commit changes to database
                            gameloop(u, BoardNumber, board, og_board)  # launch game

                        except sql.IntegrityError:  # if the game has already taken place before, launch the saved game

                            board = db.execute(f'SELECT SavedBoard from "main"."BoardUserLink" WHERE '
                                               f'username = "{u}" AND BoardNumber = {BoardNumber}').fetchone()[0]  # select the saved board form this game

                            board = [list(map(int, line)) for line in board.splitlines()]  # splits the text board into a 2d array.
                            og_board = db.execute(f'SELECT Board from "main"."defaultBoards" WHERE '
                                                  f'BoardNumber = {BoardNumber}').fetchone()[0]  # select default board for that board number and make this the og board

                            og_board = [list(map(int, line)) for line in og_board.splitlines()]  # splits the og baord into a 2d array.
                            gameloop(u, BoardNumber, board, og_board)  # launch saved game

                    else:  # if board number that user enters does not exist:
                        font = pygame.font.SysFont('ComicSans MS', 20)
                        text = font.render(f'Board number {LaunchNumber.userInput} does not exist.', True, (0, 0, 0))
                        window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear previous text
                        window.blit(text, (WIDTH // 2 - text.get_width() // 2, 400))  # render text informing the user that the board number does not exist
                        pygame.display.update()


                elif LaunchNumber.userInput == '':
                    font = pygame.font.SysFont('ComicSans MS', 20)
                    text = font.render(f'Please enter a board number', True, (0, 0, 0))
                    window.fill(BACKGROUND_COLOR, (0, 400, WIDTH, 29))  # clear previous text
                    window.blit(text, (
                        WIDTH // 2 - text.get_width() // 2, 400))  # render text alerting the user to fill the text box
                    pygame.display.update()

        LaunchNumber.update(window)  # update size of input box if text is too long
        LaunchNumber.draw(window)  # render the input box along with its prompt

        Launch.draw(window)  # render launch game button
        LogOut.draw(window)  # render logout button
        pygame.display.update()  # update display


'''Game Screen'''


def gameloop(u, BoardNumber, board, og_board):  # gameloop takes in username of the user that is logged in, board number they input, the board/saved board, and the original board

    solved_board = sudoku_solver.BT([[og_board[x][y] for y in range(len(board[0]))] for x in range(len(board))])
    # this is the board that is solved using the recursion algorithm and will be used for hints

    start_time = int(time.time())  # timer starts when game is launched

    update_gui(board, og_board, 'full')
    solveButton = Button(700, 400, 70, 30, 'Solve')
    solveButton.draw(window)

    MenuButton = Button(720, 20, 130, 30, f"{u}'s menu")
    MenuButton.draw(window)

    pygame.display.update()

    timePlayed = db.execute(
        f"SELECT Time from 'main'.'BoardUserLink' WHERE username = '{u}' AND BoardNumber = {BoardNumber}").fetchone()[
        0]  # select the time already played on that game

    timeInSec = 0 + timePlayed  # add the selected time to start time
    timeTaken = convert(timeInSec)

    font = pygame.font.SysFont('Comic SansMs', 15)
    text = font.render("Click 0 or the number in the cell to delete a value.", True, (0,0,0))
    window.blit(text, (525, HEIGHT//2 - text.get_height()//2))
    text = font.render("Click h or H to get a hint.", True, (0,0,0))
    window.blit(text, (525, HEIGHT//2 - text.get_height()//2 + 50))  # renders time taken text
    pygame.display.update()  # updates display

    while True:
        if solved_board != False:
            completed = db.execute(
                f"SELECT Completed from 'main'.'BoardUserLink' WHERE username = '{u}' AND BoardNumber = {BoardNumber}").fetchone()[
                0]  # selects the state of the board in that game

            if completed == 'False':  # if board is completed, total time taken is recorded.
                timeInSec = int(time.time()) - start_time + timePlayed
                timeTaken = convert(timeInSec)  # seconds is converted into hh:mm:ss format

            font = pygame.font.SysFont('Comic SansMs', 20)
            text = font.render(f'Time: {timeTaken}', True, (0, 0, 0))
            window.fill(BACKGROUND_COLOR, (100, 510, WIDTH, 29))  # removes previous text
            window.blit(text, (220, 510))  # renders time taken text
            pygame.display.update()  # updates display

            hintCount = db.execute(
                f"SELECT hintCount from 'main'.'BoardUserLink' WHERE username = '{u}' and BoardNumber = {BoardNumber}").fetchone()[
                0]
            text = font.render(f'Hints remaining: {3 - hintCount}', True, (0, 0, 0))
            window.fill(BACKGROUND_COLOR, (100, 10, 190 + text.get_width() + 5, 29))  # removes previous text
            window.blit(text, (190, 10))  # renders time taken text
            pygame.display.update()  # updates display

            if board == solved_board and completed != 'SolvedWithAlgo':  # save that board is completed to users db
                db.execute(
                    f"UPDATE 'main'.'BoardUserLink' SET (Completed, Time) = ('True', {timeInSec}) WHERE username = '{u}' and BoardNumber = {BoardNumber}")  # update the status of the board and the time taken to solve board.

                conn.commit()  # commit changes to database

                font = pygame.font.SysFont('Soria', 40)
                text = font.render("Correct!", True, pygame.Color('burlywood1'))
                window.blit(text, (550, HEIGHT // 2 - text.get_height()))

            elif board == solved_board and completed == 'SolvedWithAlgo':  # if board is solved using algorithm:
                font = pygame.font.SysFont('Soria', 40)
                text = font.render("Solved With Algorithm", True, pygame.Color('burlywood1'))
                # inform the user that the board was solved by algorithm.
                window.blit(text, (550, HEIGHT // 2 - text.get_height()))

            for event in pygame.event.get():  # for every event that takes place:
                if event.type == pygame.QUIT:  # if the quit window button is clicked, save the board to the game in the database
                    boardString = ''
                    for sub_list in board:
                        boardString = boardString + (
                            ''.join(str(digit) for digit in sub_list)) + '\n'  # convert 2d array into a text board
                    db.execute(
                        f'UPDATE "main"."BoardUserLink" SET (SavedBoard, Time) = ("{boardString}", {timeInSec}) WHERE username = "{u}" AND BoardNumber = {BoardNumber}')  # update the board to the saved board
                    conn.commit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:  # if the mouse button is clicked:
                    pos = pygame.mouse.get_pos()  # get the position of mouse [x,y]
                    solveButton.handle_event(event)  # handle all the events for the solve button
                    MenuButton.handle_event(event)  # handle all the events for the menu button
                    i = pos[1] // 50 - 1  # get position of mouse in terms of 2d grid
                    j = pos[0] // 50 - 1  # get position of mouse in terms of 2d grid

                    if solveButton.active:  # if solve button is clicked
                        db.execute(
                            f"UPDATE 'main'.'BoardUserLink' SET (Completed, Time) = ('SolvedWithAlgo', {timeInSec}) WHERE username = '{u}' and BoardNumber = {BoardNumber}")  # update the board state and the time for that game
                        conn.commit()  # commit changes to database
                        board = solved_board  # board is solved board
                        update_gui(board, og_board, 'half')  # update the GUI to display solved board

                    elif MenuButton.active:  # if menu button is clicked
                        boardString = ''
                        for sub_list in board:
                            boardString = boardString + (''.join(
                                str(digit) for digit in
                                sub_list)) + '\n'  # convert 2d array board to text to save board
                        db.execute(
                            f'UPDATE "main"."BoardUserLink" SET (SavedBoard, Time) = ("{boardString}", {timeInSec}) WHERE username = "{u}" AND BoardNumber = {BoardNumber}')  # save the board and the time taken in this session
                        conn.commit()  # commit changes to database
                        usermenu(u)  # go back to user menu

                    elif -1 < i < 9 and -1 < j < 9 and board != solved_board:  # if user clicks the mouse button between the dimensions of the 2d board and the board is not solved yet:
                        insert(i, j, board, og_board, solved_board, u,
                               BoardNumber)  # insert a value into  that position


                    else:
                        pass

        else:
            font = pygame.font.SysFont('Soria', 60)  # font size is 60
            text = font.render(f'Board is unsolvable', True, (0, 0, 0))  # initailises the text
            window.fill((255, 255, 255))  # fills the entire screen white
            window.blit(text, (WIDTH // 2 - text.get_width() // 2,
                               HEIGHT // 2 - text.get_height() // 2))  # renders the text in the middle of the screen
            db.execute(
                f"DELETE FROM 'main'.'BoardUserLink' WHERE username = '{u}' AND boardNumber = {BoardNumber}")  # deletes the game from the link table
            db.execute(
                f"DELETE FROM 'main'.'defaultBoards' WHERE boardNumber = {BoardNumber}")  # deletes the invalid boards from the default boards table so it can never be played again
            conn.commit()  # commit changes to database
            pygame.display.update()  # updates display
            time.sleep(5)  # waits 5 seconds on the 'Board cannot be solved' screen and returns back to the user menu.
            usermenu(u)


def convert(second):  # converts seconds to the format hourrs: minutes: seconds
    second = second % (24 * 3600)
    hour = second // 3600
    second %= 3600
    minutes = second // 60
    second %= 60

    return f"{hour}:{minutes}:{second}"


def update_gui(board, og_board, mode):  # update gui takes in board, og board and the mode

    if mode == 'half':  # if mode is half, clear the sudoku board
        pygame.draw.rect(window, BACKGROUND_COLOR, (50, 50, 450, 450))
    elif mode == 'full':  # if mode is full, clear entire screen
        pygame.draw.rect(window, BACKGROUND_COLOR, (0, 0, 900, 550))

    font = pygame.font.SysFont('ComicSans MS', 35)

    for i in range(0, 10):  # draw 10 rows and columns to make board
        pygame.draw.line(window,
                         color=(0, 0, 0),
                         start_pos=(50 + 50 * i, 50),
                         end_pos=(50 + 50 * i, 500),
                         width=4 if i % 3 == 0 else 2)  # every 3 columns, make the column wider to make a 3x3 grid visible
        pygame.draw.line(window,
                         color=(0, 0, 0),
                         start_pos=(50, 50 + 50 * i),
                         end_pos=(500, 50 + 50 * i),
                         width=4 if i % 3 == 0 else 2)  # every 3 rows, make the row wider to make a 3x3 grid visible

    font = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(9):  # for every column
        for j in range(9):  # for every row in column

            if str(board[i][j]) in '123456789':  # if a user enters a value on the board
                if board[i][j] != og_board[i][j]:
                    valid = sudoku_solver.check_valid(board, board[i][j], [i,
                                                                           j])  # check if it is a valid input (does not produce any clashes)
                    if not valid:
                        fontColor = (255, 90, 90)  # if a clash is produced, make number red
                    else:
                        fontColor = (50, 50, 255)  # if no clash is produced, make number blue

                else:  # if board value for that cell is a fixed value
                    valid = sudoku_solver.check_valid(board, board[i][j], [i, j])  # check if it is a valid input
                    if not valid:
                        fontColor = (
                        200, 0, 0)  # if clash is produced, make number darker red to show that it is a fixed value
                    else:
                        fontColor = (0, 0, 0)  # if no clash is produced, make number black

                value = font.render(str(board[i][j]), True, fontColor)
                window.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))  # render the numbers on the board for each cell
    pygame.display.update()  # update display


def insert(i, j, board, og_board, solved_board, u,
           BoardNumber):  # insert is a function for the user to input values on to the board
    while True:
        for event in pygame.event.get():  # for every event:
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # get mouse pos
                i = pos[1] // 50 - 1  # get position of mouse in terms of 2d grid
                j = pos[0] // 50 - 1
                if -1 < i < 9 and -1 < j < 9 and board != solved_board:
                    insert(i, j, board, og_board, solved_board, u, BoardNumber)
                    # recursion. so that user can click on another cell after clicking on one cell and still be able to edit it
                else:
                    return

            elif event.type == pygame.KEYDOWN and -1 < i < 9 and -1 < j < 9:  # if event on the board is a key press on the keyboard:

                if og_board[i][j] != 0:  # if board value is not fixed, dont change anything
                    return

                if event.key == 48 or event.key - 48 == board[i][
                    j]:  # if the user presses 0 or the number in the cell, delete the value
                    board[i][j] = 0  # 0 denotes an empty cell
                    update_gui(board, og_board, 'half')  # update the board
                    return

                if 0 < event.key - 48 < 10:  # if key press is the numbers between 0 and 10

                    board[i][j] = event.key - 48  # board value for that cell is the key the user presses
                    update_gui(board, og_board, 'half')
                    return

                if event.key == 72 or event.key == 104:
                    hintCount = db.execute(
                        f"SELECT hintCount from 'main'.'BoardUserLink' WHERE username = '{u}' and BoardNumber = {BoardNumber}").fetchone()[
                        0]  # number of hints used per game

                    if hintCount < 3:  # if key press is the letter h/H and user has used less than 3 hints
                        board[i][j] = solved_board[i][j]  # give the correct answer for that cell
                        update_gui(board, og_board, 'half')
                        hintCount += 1  # increment hint count by 1
                        db.execute(
                            f"UPDATE 'main'.'BoardUserLink' SET hintCount = {hintCount} WHERE username = '{u}' AND BoardNumber = {BoardNumber}")
                        conn.commit()

                        return

            else:
                pass


main()  # run the main function
