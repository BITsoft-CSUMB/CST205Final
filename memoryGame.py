"""
Final Project - Memory Game
CST 205 Multimedia Design and Programming

Team #6
Matthew Valancy (Crenshaw)
Ashley Wallace
Brittany Mazza
John Lester
"""
import random # it's not a game if it's always the same
import copy # who needs class(es) when you've got lists to copy
import time # sleep between pic flashes

setMediaPath() # where are the pictures at??

cardStates = ['unselected', 'selected', 'matched']
gameStates = {'quit': -2, 'lose': -1, 'playing': 0, 'win': 1, 'topScore':0}
cardImages = []
# Restore this picture to have a clean board
backgroundPic = makePicture(getMediaPath("Background.jpg"))
# Draw over this picture with new regions as the game progresses.
gameScreen = makePicture(getMediaPath("Background.jpg"))
random.seed() # Initialize random number generator.

def playGame():
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
  pickSound = makeSound(getMediaPath("card-flip.wav"))
  matchSound = makeSound(getMediaPath("winner.wav"))
  # Don't use show from now on, just redraw gameScreen.
  show(gameScreen)
  # Loop outside the active game, so pl+ayer can replay, show final score, etc.
  while not isQuit:
    cardImages = loadDeck()
    printHelpMsg()
    # Setup game
    matches = 0 # number of successful matches
    incorrectMatches = 0 # number of incorrect matches
    gameState = gameStates['playing']
    gameBoard = getNewGameBoard(boardSize)
    fillBoard(gameBoard, maxMatches)
    
    # Actual, active game loop
    while gameState == gameStates['playing']:
      # Get guess #1.
      showBoard(gameBoard)
      try:
        pickA = getSelection(gameBoard, cardCount)
        pickA['cardState'] = cardStates[1]
        play(pickSound)
      except:
        if pickA == gameStates['quit']:
          gameState = gameStates['lose']
        continue
      # Get guess #2.
      showBoard(gameBoard)
      try:
        pickB = getSelection(gameBoard, cardCount)
        pickB['cardState'] = cardStates[1]
        play(pickSound)
      except:
        if pickB == gameStates['quit']:
          gameState = gameStates['lose']
        continue
      # Display current game.
      showBoard(gameBoard)
      time.sleep(1)
      if pickA['uniqueID'] == pickB['uniqueID']:
        pickA['cardState'] = cardStates[2]
        pickB['cardState'] = cardStates[2]
        matches += 1
        applyTint(pickA['image'])
        printNow("Match, way to go!")
        play(pickSound)
      else:
        pickA['cardState'] = cardStates[0]
        pickB['cardState'] = cardStates[0]
        incorrectMatches += 1
        printNow("No match.")
      # Let the user know when they've matched all of the cards.
      if matches == maxMatches:
        printNow("All cards matched!")
        gameState = gameStates['win']
        play(matchSound)
        time.sleep(5)
    printNow(
      str(matches) + " correct and " + str(incorrectMatches) + 
      " incorrect matches total.")
    if (matches/(matches+incorrectMatches) > gameStates['win']):
      gameStates['win'] = matches/(matches+incorrectMatches)
      printNow("Congratulations - new high score (" + str(gameStates['win']) + ")")
    isQuit = True 

def getNewGameBoard(boardSize):
  """
  Create a new game board with new cards.
  """
  global cardStates
  gameCard = {
      'uniqueID': -1,
      'x': -1,
      'y': -1,
      'cardState': cardStates[0],
      'image': makeEmptyPicture(100,100)
  }
  return [[copy.copy(gameCard) for x in range(boardSize)] for y in range(boardSize)]

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

def showBoard(gameBoard):
  """
  Show the game board based on the state of each card.
  """
  copyInto(backgroundPic, gameScreen, 0, 0) # nothing like a fresh start
  size = len(gameBoard)
  for y in range(size):
    line = "\n"
    for x in range(size):
      cardState = gameBoard[y][x]['cardState']
      if cardState == cardStates[2]:
        # --Matched card--
        # Highlight this tile.
        cardImage = gameBoard[y][x]['image']
        copyInto(cardImage, gameScreen, 100 * x, 100 * y)
      if cardState == cardStates[1]:
        # --Selected card--
        # Draw the regular card face on this tile.
        cardImage = gameBoard[y][x]['image']
        copyInto(cardImage, gameScreen, 100 * x, 100 * y)
  repaint(gameScreen)
  
def getSelection(gameBoard, cardCount):
  """
  Let the user select a valid game tile.
  Parameters: gameBoard -> The game board (array).
              cardCount -> The total number of cards that can be selected
                           from (int).
  Returns: Selected card if the user selects something valid, or a game state
           if they use a command to quit.
  Throws: Use exception handling to catch the quit case when they don't select
          a card.
  """
  global gameStates
  while True:
    # Reset the user's card selection to -1, which is an invlid card entry.
    value = -1
    input = raw_input("Please select a card (1, 2, 3, etc...): ")
    # Exit case.
    if input == "q" or input == "quit":
      return gameStates['quit']
    # User must redo their card selection if their entered value can't be cast
    # to an integer.
    try:
      value = int(input) - 1
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
  # Find all images in the /cardImages directory.
  images = []
  for file in os.listdir(getMediaPath()):
    if file.endswith("-bsmg.jpg") and file is not "background.jpg":
      images.append(makePicture(file))
  return images # list of card images to use for the game

def applyTint(image):
  """
  Apply tint to show which images are already matched.
  """
  pixels = getPixels(image)
  for p in pixels:
    g = getGreen(p)
    r = getRed(p)
    b = getBlue(p)
    setGreen(p,(g+r+b)/3)
    setRed(p,(g+r+b)/3)
    setBlue(p,(g+r+b)/3)
    makeDarker(getColor(p))

def printHelpMsg():
  """
  Display the welcome and help message.
  Parameters: (none)
  Returns: N/A
  """
  printNow(
    "Welcome to Memory Cards!\n" +
    "Cards are numbered 1 - 16. Type the number of the card you would like\n" +
    "to select. When you find a matching pair they will remain on the\n" +
    "board. Type 'help' to repeat this message and 'quit' to exit the game.\n" +
    "To start the game again once you have finished type 'playGame()'\n")

playGame()
