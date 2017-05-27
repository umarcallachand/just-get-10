import pygame, sys
from random import random
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)
CYAN = (35,253,255)
PURPLE = (115,55,139)
GB = (55,240,118)
YELLOW = (255,208,63)
BROWN = (235,152,78)
GRAY = (133,146,158)
PINK = (229,118,168)
OLIVE = (180,210,30)
MAROON = (250,60,60)
BLUE = (90,90,255)
LGREY = (220,225,230)

def probability(prob):
    #the function which will randomly return 1, 2, 3 & 4
    #number of 1 > 2 > 3 > 4
    #0 < x1 < x2 < x3 < 1
    #prob = (0.05, 0.18, 0.5), probability of getting a 4: 0.05, 3:0.18-0.05 = 0.013, 2:0.5 - 0.18 = 0.32, 1:1 - 0.5 = 0.5
    x1, x2, x3 = prob
    ran = random()
    if ran < x1:
        return 4
    elif ran > x1 and ran < x2:
        return 3
    elif ran > x2 and ran < x3:
        return 2
    else:
        return 1

def newBoard(prob,n):
    #returns the random values in a 2D list
    #depends on n which is the number of rows and columns
    board = [[probability(prob) for row in range(n)] for col in range(n)]
    return board

def adjacent(n, board, i, j):
    #checks whether a coordinate (i, j) has an adjacent cell with the same value
    #if yes the function returns True
    xs = range(1,11)
    sum_same_val = 0
    for x in xs:
        #checks row above but same column
        if i > 0:
            if board[i][j] == x and board[i-1][j] == x:
                sum_same_val += 1
        #checks column to the left but same row
        if j > 0:
            if board[i][j] == x and board[i][j-1] == x:
                sum_same_val += 1
        #check row below but same column
        if i < (n-1):
            if board[i][j] == x and board[i+1][j] == x:
                sum_same_val += 1
        #check column to the right but same row
        if j < (n-1):
            if board[i][j] == x and board[i][j+1] == x:
                sum_same_val += 1

    #if sum_same_value > 0, it implies that at least one adjacent cell..
    # to a particular coordinate has the same value
    #thus it returns True
    if sum_same_val > 0:
        return True

def possible(n, board):
    #check whether there are possible moves
    #i.e checks that atleast one cell has adjacent cell with same value
    #hence for each row and column, we verify...
    #if the adjacent function is true
    #and if it is the game continues else stops
    for row in range(n):
        for column in range(n):
            if adjacent(n, board, row, column) == True:
                return True 

def propagation(n, board, liist):
    #liist contain a tuple of the coordinates of the cell which has been clicked
    #this function will append all coordinates...
    #of the clicked cell's adjacent cases...
    #with same value
    for cord in liist:
        (i, j) = cord
        number = board[i][j]
        #checks if value is same in row above but same column
        if i > 0:
            if board[i-1][j] == number and (i-1, j) not in liist: #it also checks if the coordinates is in the list or not
                liist.append((i-1,j))
        #checks if value is same in row down but same column
        if i < (n-1):    
            if board[i+1][j] == number and (i+1, j) not in liist:
                liist.append((i+1,j))
        #checks if value is same in column to the left but same row
        if j > 0:    
            if board[i][j-1] == number and (i, j-1) not in liist:
                liist.append((i,j-1))
        #checks if value is same in column to the right but same row
        if j < (n-1):        
            if board[i][j+1] == number and (i, j+1) not in liist:
                liist.append((i,j+1))
    #if value is same as that specified coordinate's value, the list is returned.
    return liist

def modification(n, board, liist):
    #the first coordinate in the list is taken and its value incremented by 1
    #and all the other coordinates in the list are set to 0
    #the list referred to here is the list which is returned in the ...
    #propagation function, i.e the 'liist'

    #liist[0] is the first coordinate from liist
    i, j = liist[0]
    number = board[i][j]
    #the value is here incremented by 1
    board[i][j] = number + 1

    #here all the values of the other coordinates in the liist are set to 0
    for coordinates in liist[1:]:
        i, j = coordinates
        board[i][j] = 0
    
    return board

def gravity(n, board, prob):
    #here the cells where value = 0 are swapped from their coordinate till...
    #they reach the top
    for _ in range(n-1):
    #the cells are swapped (n-1) times so that if a cell at the bottom = 0, it will reach the top
        for row in range(1,n):
            for col in range(n):
                #if a cell's value = 0
                if board[row][col] == 0:
                    #it is swapped up till the top
                    board[row][col] = board[row -1][col]
                    board[row -1][col] = 0
    #then all the swapped cells where value = 0 are allocated random values
    #by the use of the probability function
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                board[i][j] = probability(prob)
                
    return board  

def maxval(n, board):
    #returns the maximum value of the board
    #each row's maximum value is appended to the list 'lst'
    lst = []
    for row in range(n):
        lst.append(max(board[row]))

    return max(lst)

def score(n, board, surface):
    #the score is the maximum value on the board
    #this is obtained by the maxval function
    maximum = maxval(n,board)
    
    text = pygame.font.SysFont("comicsansms", 50).render('Current Score: ' + str(maximum) + '  ', True, BLACK,LGREY)
    surface.blit(text, (590,100))

def drawBoard(n, board, surface):
    #the size of a square in the board is 500//number of rows and columns(n) to obtain a proper size for each square
    #the size of each number is 350//n to obtain a presentation of the numbers
    size = 500//n
    font_size = 350//n
    #here each number is assigned to a particular color
    colors = {0:BLACK, 1 : GB, 2: BLUE, 3: YELLOW, 4:PINK, 5:GRAY, 6:CYAN, 7:OLIVE, 8:MAROON, 9:BROWN, 10:PURPLE}
    #here we derive a formula so as to display all the squares ...
    #representing the board
    for i in range(n):
        for j in range(n):
            for val in range(11):
                #the square is drawn depending on x and y
                #x and y depend on i and j, i.e row and column respectively
                #so for each coordinate a square is drawn
                #we left a 50px space from the left and from the top
                x = size * i + 50
                y = size * j + 50
                #here each square of specific value take its assigned color
                if board[i][j] == val:
                    color = colors.get(val)
                    #the board is displayed with their values and colors
                    pygame.draw.rect(surface,color,(y,x,size,size))
                    #the value is displayed centered and in black 
                    basicfont = pygame.font.SysFont("comicsansms", font_size)
                    text = basicfont.render(str(val), True, BLACK)
                    surface.blit(text, (y+30,x))
                    #the save game is displayed
                    text1 = pygame.font.SysFont("comicsansms", 35).render('Save game(press s)', True, BLACK,LGREY)
                    surface.blit(text1, (600,200))


def modifyBoard(n, board, liist, prob, surface):
    #the board is modified by these functions respectively and drawn again
    modification(n, board, liist)
    gravity(n, board, prob)
    score(n, board, surface)
    drawBoard(n,board,surface)
    
    pygame.display.update()
                    
def parameter(board, n, surface,i,j,liist):
    size = 500//n
    font_size = 350//n
    #the board is drawn again so as after each click, only the cells selected is highlighted in white
    drawBoard(n,board,surface)
    
    liist = propagation(n, board, liist)
    for cord in liist:
        (i,j) = cord
        x = size * i + 50
        y = size * j + 50
        value = board[i][j]

        #the cells contained in the list are drawn again but in white                        
        pygame.draw.rect(surface,WHITE,(y,x,size,size))
        
        basicfont = pygame.font.SysFont("comicsansms", font_size)
        text = basicfont.render(str(value), True, BLACK)
        surface.blit(text, (y+30,x))
                                
        pygame.display.update()

               
def game_over(board,n,surface):
    #this function displays the texts that appears in case game is over
    #the texts appear in their associated fonts and colors
    #maximum is the maxval on the board when the game is over
    maximum = maxval(n,board)
    
    #final score is displayed with the maximum value
    text1 = pygame.font.SysFont("comicsansms", 55).render(' Final Score: ' + str(maximum) + '  ', True, BLACK,LGREY)
    surface.blit(text1, (580,100))
    
    #play again is displayed
    text2 = pygame.font.SysFont("comicsansms", 35).render('Play Again(press p)', True, BLACK,LGREY)
    surface.blit(text2, (600,300))

    #quit is displayed
    text3 = pygame.font.SysFont("comicsansms", 35).render('QUIT(press ESC)', True, BLACK,LGREY)
    surface.blit(text3, (600,400))

    #load game is displayed
    text4 = pygame.font.SysFont("comicsansms", 35).render('Load game(press L)', True, BLACK,LGREY)
    surface.blit(text4, (600,200))
                    
    pygame.display.update()

def animation(surface):
    #a mp3 sound is loaded and played
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    
    #it loads and blit the image on the screen when the player wins
    win = pygame.image.load('win.jpg')
    winner = pygame.image.load('trophy.jpg')
    
    x,y = 0,0
    while True:
        surface.fill(WHITE)
        surface.blit(win,(400,50))
        surface.blit(winner,(x,y))
        #x and y changes so that the image appear to be moving
        x += 0.5
        y += 0.5
        #when the image disappear 
        if y > 600:
            return False
        
        pygame.display.update()

def difficulty(surface):
    #this function displays the first texts to appear upon running the game
    #the user must a difficulty level
    
    surface.fill(LGREY)
    basicfont = pygame.font.SysFont("comicsansms", 45)

    text = pygame.font.SysFont("comicsansms", 25).render('**Left click to select, Right click to merge**', True, BLACK,LGREY)
    surface.blit(text, (20,10))
    
    text1 = basicfont.render('Easy(6x6)(press 6)', True, BLACK,LGREY)
    surface.blit(text1, (70,100))

    text2 = basicfont.render('Normal(5x5)(press 5)', True, BLACK,LGREY)
    surface.blit(text2, (70,200))

    text3 = basicfont.render('Hard(4x4)(press 4)', True, BLACK,LGREY)
    surface.blit(text3, (70,300))

    text4 = basicfont.render('Load game(press L)', True, BLACK,LGREY)
    surface.blit(text4, (70,400))

    pygame.display.update()

def main():
    pygame.init()

    surface = pygame.display.set_mode((1000,600))
    pygame.display.set_caption('Just Get 10!')
    #surface.fill(LGREY)
    
    choosed = False

    #the difficulties or loading of the previous game is displayed
    difficulty(surface)
    #probability of the display of value 1 > 2 > 3 > 4
    prob = (0.05, 0.18, 0.5)    
    drawn = False
    loaded = False
    
    while True: 
        for event in pygame.event.get():
            #to quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                #if the ESC key is pressed, the game is closed
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #if the P key is pressed, you can play again
                #i.e you get back to the main where you can choose your ...
                #level of difficulty and play again
                if event.key == K_p:
                    drawn = False
                    choosed = False
                    loaded = False
                    difficulty(surface)

                #if 6 is pressed, number of rows and columns will be 6
                #and the level of difficulty will be easy
                if event.key == K_6:
                    n = 6
                    choosed = True

                #if 5 is pressed, number of rows and columns will be 5
                #and the level of difficulty will be normal
                if event.key == K_5:
                    n = 5
                    choosed = True

                #if 4 is pressed, number of rows and columns will be 4
                #and the level of difficulty will be hard
                if event.key == K_4:
                    n = 4
                    choosed = True

                #load board from saving.txt
                if event.key == K_l:            
                    drawn = False
                    choosed = True
                    #file is open on read mode
                    file = open('saving.txt','r')
                    text = file.read()
                    #to determine how many rows and columns there are, i.e n
                    if len(text) == 56:
                        n = 4
                    elif len(text) == 85:
                        n = 5
                    else:
                        n = 6

                    row = 0
                    column = 0
                    board = newBoard(prob,n)    # a new board with n rows and columns is created again so as to get the format of the 2D list
                    #to convert str(board) back to a list which can be used as the board:
                    for a in text:
                        if a != '[' and a != ']' and a != ',' and a != ' ':
                            b = int(a)
    
                            board[row][column] = b
    
                            column += 1
    
                            if column > n-1:
                                column = 0
                                row += 1
                    loaded = True
                    file.close() #the file is closed to liberate memory

                #save the board to saving.txt
                if event.key == K_s:            
                    file = open('saving.txt','w')
                    text = file.write(str(board))
                    file.close()
                    
            if choosed == True and drawn == False:    
                size = 500//n

                if loaded != True:   #if loaded = True the board will not be created again                
                    board = newBoard(prob, n)

                score(n, board, surface)

                drawBoard(n,board,surface)
                
                drawn = True    #drawn = True if the board has been drawn

            #if the player has choosen n or loaded a game, then the MOUSEBUTTONUP will have effects           
            if choosed == True and event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    i = int((y - 50)//size)
                    j = int((x - 50)//size)

                    #if player clicks outside board, nothing happens        
                    if i in range(n) and j in range(n):         
                        if adjacent(n, board, i, j) == True:    
                            liist = [(i,j)]
                            parameter(board, n, surface,i,j,liist)

                            #event.button == 3 means right click and the board will be modified
                            if event.button == 3:               
                                modifyBoard(n, board, liist, prob, surface)
                                
                                #if there is no adjacent cells with same value or maximum value = 10, the game is over
                                if possible(n, board) != True:
                                    game_over(board,n,surface)

                                if maxval(n, board) == 10:
                                    
                                    animation(surface)
                                    surface.fill(LGREY)
                                    game_over(board,n,surface)
            
        pygame.display.update()
            
main()

#Umar Callachand & Souheila Mungroo
#All Copyrights Reserved
