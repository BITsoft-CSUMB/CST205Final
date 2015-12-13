import random
import copy


random.seed()


cardStates = ['unselected', 'selected', 'matched']


def play():
  boardSize  = 4 # change to increase difficulty, maybe let them select
  cardCount  = boardSize * boardSize
  maxMatches = cardCount / 2
    
  cardStates = ['unselected', 'selected', 'matched']
  gameCard = {'x': -1, 'y': -1, 'cardState': cardStates[0], 'imageName': 'none'}
  
  #quit = false # set to 1 to stop playing
  gameState  = 0 # -1 is lose, 1 is win, 0 is playing
  quit = 0
  while quit == 0:
  #while gameState == 0:
  #setup game
    gameState  = 0 # -1 is lose, 1 is win, 0 is playing
   
    gameCard = {'uniqueID': -1, 'x': -1, 'y': -1, 'cardState': cardStates[0], 'imageName': 'none'}
    gameBoard  = [[copy.copy(gameCard) for x in range(boardSize)]for x in range(boardSize)]
    fillBoard(gameBoard, maxMatches)
    
    matches = 0 # how many successful matches do we have?
    
    while gameState == 0:
      
      showBoard(gameBoard)
      try:
        pickA = getSelection(gameBoard, cardCount)
      except:
        if pickA == -2:
          gameState = -1
        else:
          continue
          
      gameBoard[pickA['y']][pickA['x']]['cardState'] = cardStates[1]      
      showBoard(gameBoard)
      
      try:
        pickB = getSelection(gameBoard, cardCount)
      except:
        if pickB == -2:
          gameState = -1
        else:
          continue
      gameBoard[pickB['y']][pickB['x']]['cardState'] = cardStates[1]
                
      if pickA['uniqueID'] == pickB['uniqueID']:
        gameBoard[pickA['y']][pickA['x']]['cardState'] = cardStates[2]
        gameBoard[pickB['y']][pickB['x']]['cardState'] = cardStates[2]
        matches = matches + 1
        print("Match, way to go!")
      else:
        gameBoard[pickA['y']][pickA['x']]['cardState'] = cardStates[0]
        gameBoard[pickB['y']][pickB['x']]['cardState'] = cardStates[0]
        print("No match.")
        
      if matches == maxMatches:
        print("All cards matched!")
        gameState = 1
    quit = 1   
  
  
# fill the game board with pairs of numbers, these numbers can reference images or anything else later
def fillBoard(gameBoard, maxMatches):
    size = len(gameBoard)
    values = [0 for x in range(maxMatches)]
    
    for x in range(maxMatches):
      values[x] = 0
    
    for y in range(size):
      for x in range(size):
        gameBoard[y][x]['x'] = x
        gameBoard[y][x]['y'] = y
        while gameBoard[y][x]['uniqueID'] == -1:
          proposedValue = random.randint(0, maxMatches - 1)
          if(values[proposedValue] < 2): # only 2 matches allowed per value
            values[proposedValue] = values[proposedValue] + 1
            gameBoard[y][x]['uniqueID'] = proposedValue
    print gameBoard
    


# show the game board based on the state of each card
def showBoard(gameBoard):
  size = len(gameBoard)
  
  for y in range(size):
    line = ""
    for x in range(size):
      cardState = gameBoard[y][x]['cardState']  
      if cardState == cardStates[0]: #----------Unselected card
        line += "X "
      elif cardState == cardStates[1]: #-------Selected card
        line += "Y "
      else: #-----------------------------------Matched card
        line += "Z "
    print line
      
      
# let the user select a valid game tile      
def getSelection(gameBoard, cardCount):
  selection = -1
  
  while selection == -1:
    input = raw_input("Please select a card (0, 1, 2, 3, etc...): ") 
    value = -1
    
    # special exit case
    if input == "q" or input == "quit":
      return -2
    
    # lets see if they can follow directions
    try:
      value = int(input)
    except ValueError:
      print "Invalid input, please try again."
      continue
    
    #against all odds the user input something good
    if value > -1 and value < cardCount:
      y = value / len(gameBoard)
      x = value % len(gameBoard)
      if gameBoard[y][x]['cardState'] == cardStates[0]:
        return gameBoard[y][x]
      else:
        print "This card is already in use..."
    else:
      print "This is not a valid card number"
play()