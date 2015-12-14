import random
import copy

#setMediaPath() # where are the pictures at??

random.seed() # Initialize random number generator.
cardStates = ['unselected', 'selected', 'matched']
gameStates = {'quit': -2, 'lose': -1, 'playing': 0, 'win': 1}

cardImages = []
# Pull regions from this background pic if we want to reset tiles, etc.
backgroundPic = makePicture(getMediaPath("Background.jpg"))
# Draw over this picture with new regions as the game progresses.
gameScreen = makePicture(getMediaPath("Background.jpg")) 


def play():
  """
  Begin the memory card game.
  The order is:
    1) setup program
    2) setup main game loop
    3) run main game loop
  """
  global cardStates
  global cardImages
  global gameStates
  global gameScreen # background modified as game progresses
  global backgroundPic # original, clean background
  boardSize = 4
  cardCount = boardSize * boardSize
  maxMatches = cardCount / 2
  isQuit = False

  cardImages = loadDeck()
  show(gameScreen)

  # Loop outside the active game, so player can replay, show final score, etc.
  while not isQuit: 
    # Setup game
    matches = 0 # number of successful matches
    gameState = gameStates['playing']
    gameBoard = getNewGameBoard(boardSize)
    fillBoard(gameBoard, maxMatches)
    
    # Actual, active game loop
    while gameState == gameStates['playing']:
      showBoard(gameBoard)

      try:
        pickA = getSelection(gameBoard, cardCount)
      except:
        if pickA == gameStates['quit']:
          gameState = gameStates['lose']
        continue
  
      gameBoard[pickA['y']][pickA['x']]['cardState'] = cardStates[1]      
      gameBoard[pickA['y']][pickA['x']]['stateChanged'] = true
      showBoard(gameBoard)
      
      # ?Does getSelection throw an error?
      # no but it would be nice for having the special quit case that's not a
      # card
      # We should either intentionally throw an error/exception with "raise"
      # or check for the type returned. Right now this doesn't appear to work.
      try:
        pickB = getSelection(gameBoard, cardCount)
      except:
        if pickB == gameStates['quit']:
          gameState = gameStates['lose']
        continue

      gameBoard[pickB['y']][pickB['x']]['cardState'] = cardStates[1]
      gameBoard[pickB['y']][pickB['x']]['stateChanged'] = true 
                
      if pickA['uniqueID'] == pickB['uniqueID']:
        gameBoard[pickA['y']][pickA['x']]['cardState'] = cardStates[2]
        gameBoard[pickB['y']][pickB['x']]['cardState'] = cardStates[2]
        matches = matches + 1
        printNow("Match, way to go!")
      else:
        
        gameBoard[pickA['y']][pickA['x']]['cardState'] = cardStates[0]
        gameBoard[pickB['y']][pickB['x']]['cardState'] = cardStates[0]
        printNow("No match.")
        
      if matches == maxMatches:
        printNow("All cards matched!")
        gameState = gameStates['win']
    isQuit = True 


def getNewGameBoard(boardSize):
  """
  """
  global cardStates
  gameCard = {
      'uniqueID': -1,
      'x': -1,
      'y': -1,
      'cardState': cardStates[0],
      'stateChanged': false,
      'image': makeEmptyPicture(100,100)
  }
  row = [copy.copy(gameCard) for x in range(boardSize)]
  return [row for x in range(boardSize)]


def fillBoard(gameBoard, maxMatches):
  """
  Fill the game board with pairs of numbers, these numbers can reference
  images or anything else later.
  """
  size = len(gameBoard)
  values = [0] * maxMatches
  global cardImages
  
  for x in range(maxMatches):
    values[x] = 0

  for y in range(size):
    for x in range(size):
      gameBoard[y][x]['x'] = x
      gameBoard[y][x]['y'] = y
      while gameBoard[y][x]['uniqueID'] == -1:
        proposedValue = random.randint(0, maxMatches - 1)
        if values[proposedValue] < 2: # only 2 matches allowed per value
          values[proposedValue] = values[proposedValue] + 1
          gameBoard[y][x]['uniqueID'] = proposedValue
          try:
            gameBoard[y][x]['image'] = cardImages[proposedValue]
          except:
            # If we don't have enough images, just use some trees. Don't trip.
            gameBoard[y][x]['image'] = cardImages[0]
  # TODO: Remove the displayed game cards. This is for testing purposes.
  #printNow(gameBoard)


# new and improved graphical game board!
def showBoard(gameBoard):
  """
  Show the game board based on the state of each card.
  """
  printNow("empty function show graphical board")  
  size = len(gameBoard)
  for y in range(size):
    line = "\n"
    for x in range(size):
      cardState = gameBoard[y][x]['cardState']
      stateChanged = gameBoard[y][x]['stateChanged']
      if cardState == cardStates[0] and stateChanged:
        # --Unselected card--
        # Redraw the background on this tile.
        print("draw background tile") # need something just so it doesnt error
      elif cardState == cardStates[1]:
        # --Selected card--
        # Draw the regular card face on this tile.
        cardImage = cardImages[y * len(gameBoard) + x]
        copyInto(cardImage, gameScreen, 100 * x, 100 * y)
      else:
        # --Matched card--
        # Highlight this tile.
        print("highlight tile")
      stateChanged = False # reset state changed flag
  repaint(gameScreen)


# # Old text based game board still here for debugging purposes.
# def showBoardOld(gameBoard):
#   """
#   Show the game board based on the state of each card.
#   """
#   size = len(gameBoard)
  
#   for y in range(size):
#     line = "\n"
#     for x in range(size):
#       cardState = gameBoard[y][x]['cardState']
#       if cardState == cardStates[0]: #----------Unselected card
#         line += "X "
#       elif cardState == cardStates[1]: #-------Selected card
#         line += "Y "
#       else: #-----------------------------------Matched card
#         line += "Z "
#     printNow(line)


def getSelection(gameBoard, cardCount):
  """
  Let the user select a valid game tile.
  Parameters: gameBoard -> The game board (array).
              cardCount -> The total number of cards that can be selected
                           from (int).
  Returns: Selected card if the user selects something valid, or a game state
           if they use a command to quit.
  Throws: TODO: raise exception
          Use exception handling to catch the quit case when they don't select
          a card.
  """
  global gameStates
  while True:
    # Reset the user's card selection to -1, which is an invlid card entry.
    value = -1
    input = raw_input("Please select a card (0, 1, 2, 3, etc...): ")
    # Exit case.
    if input == "q" or input == "quit":
      return gameStates['quit']
    # User must redo their card selection if their entered value can't be cast
    # to an integer.
    try:
      value = int(input)
    except ValueError:
      printNow("Invalid input, please try again.")
      continue
    # User must redo their card selection if their entered value isn't valid.
    if value < 0 or value >= cardCount:
      printNow("This is not a valid card number")
      continue
    # Against all odds, the user input something good.
    y = value / len(gameBoard)
    x = value % len(gameBoard)
    if gameBoard[y][x]['cardState'] == cardStates[0]:
      return gameBoard[y][x]
    else:
      printNow("This card is already in use...")


def loadDeck():
  """
  Load the deck of cards and return an array that represents the cards. The
  card image files should go from 0.jpg to n.jpg, with 0 being the default.
  This makes it easy to match "uniqueID" for the game board tiles with images.
  This deck array will store all of the unmodified original images. Then, we
  can modify the images for each tile independently after copying from the
  deck.
  Parameters: (none)
  Returns: Array that represents the cards.
  """
  # find all images in the /cardImages directory
  images = []
  for file in os.listdir(getMediaPath()):
    if file.endswith(".jpg") and file is not "background.jpg":
      images.append(makePicture(file))
  return images # list of card images to use for the game


def makeMatchImages(deck):
  """
  Pre-generate images for matched cards (green filter, whatever) so we dont
  lag while playing maybe save the too for re-use?
  """
  # For every card image, apply filter.
  #return [image0, image1, image2, ..., imageN]


play()
