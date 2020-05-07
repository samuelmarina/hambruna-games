from db import retrieveData, removeUserByID, getUserByID, submitDeathDatabase, retrieveDeadData
from random import randint
from PIL import Image, ImageDraw
from igbot import uploadPost, logIn
import time

minutes = 59
times = 3

def getRandomNumber(range):
    """Get random number within a range
    Args:
        range: int of range's top limit
    """
    return randint(0, range)

def getTwoIndexes(users):
    """Select two different random objects within an array
    Args:
        users: array of strings of users ids
    Returns:
        array of two users ids as strings
    """
    indexPlayer1 = getRandomNumber(len(users)-1)    #first index
    indexPlayer2 = getRandomNumber(len(users)-1)    #second index
    while indexPlayer1 == indexPlayer2:             #loop in case the second index is the same as the first one
        indexPlayer2 = getRandomNumber(len(users)-1)

    return [indexPlayer1, indexPlayer2]

def selectLoser():
    """Binary random number
    Returns:
        integer (zero or one)
    """
    return randint(0, 1)

def battle():
    """Game simulator of the Hunger Games"""
    logIn() #ig log in
    players = retrieveData() #players alive
    indexes = getTwoIndexes(players) #select two players

    loser = selectLoser() #select loser
    loserIndex = indexes[loser]
    loserID = players[loserIndex]

    postCaption = battleNarrator(indexes[0], indexes[1], players, loser, len(players)-1, 2) #ig caption
    postPicturePath = generatePicture(indexes[0], indexes[1], players) #picture path

    uploadPost(postPicturePath, postCaption) #ig upload picture
    removeUserByID(loserID) #remove user of database


def battleNarrator(index1, index2, players, loser, survivorsCount, day):
    """Prints the battle course in console
    Args:
        index1: string of first player index
        index2: string of second player index
        players: array of players as strings
        loser: int of loser index
        survivorsCount: int of amount of current survivors
        day: current day of game
    Returns:
        string caption of the ig post
    """
    userID1 = players[index1]   #player1 id
    userID2 = players[index2]   #player2 id

    player1 = getUserByID(userID1)  #object player1
    player2 = getUserByID(userID2)  #object player2

    print("Esta batalla se disputa entre " + player1[0] + " y " + player2 [0] + "\n") #This battle is between player1 and player2

    killed = ""
    if loser == 0:
        powers = player2[1] #powers array
        randomPower = powers[getRandomNumber(len(powers)-1)] #select random power
        killed = player2[0] + " ha matado a " + player1[0] + " " + randomPower #player2 killed player1 with random power
        submitDeathDatabase(player2[0], player1[0], randomPower, day) #post request

    else:
        powers = player1[1] #powers array
        randomPower = powers[getRandomNumber(len(powers)-1)] #select random power
        killed = player1[0] + " ha matado a " + player2[0] + " " + randomPower #player1 killed player2 with random power
        submitDeathDatabase(player1[0], player2[0], randomPower, day)#post request

    return generatePostCaption(killed, survivorsCount)

def generatePostCaption(killed, survivors):
    """Generate ig post caption
    Args:
        killed: string of battle text
        survivors: int of amount of current survivors
    Returns:
        string caption of the ig post
    """
    caption = killed + " 📣.\n 🏳️ Quedan " + str(survivors) + " sobrevivientes 🏳️" #caption
    print(caption)
    return caption

def generatePicture(index1, index2, players):
    """Generate ig post picture
    Args:
        index1: int index player1
        index2: int index player2
        players: array of players
    Return:
        string of image path
    """
    userID1 = players[index1] #player1 id
    userID2 = players[index2] #player2 id

    player1 = getUserByID(userID1)[0]   #object player1
    player2 = getUserByID(userID2)[0]   #object player2

    imgPlayer1 = makeCircleImg(player1[1:]).resize((370, 370)) #image player1
    imgPlayer2 = makeCircleImg(player2[1:]).resize((370, 370)) #image player2
    imgPath = getPostImage(imgPlayer1, imgPlayer2, player1, player2) #image path
    return imgPath

def generateListPicture():
    """Generate a picture listing all players"""
    players = retrieveData()
    userNum = 0
    for x in range(0, 4):
        background = Image.open('images/JUGADORES.jpg')
        copy = background.copy()
        num = 0
        y = 500
        while userNum < len(players) and num < 10:
            username = getUserByID(players[userNum])[0]
            circleImg = makeCircleImg(username[1:]).resize((100, 100))
            copy.paste(circleImg, (150, y), circleImg)
            y += 120
            userNum += 1
            num += 1
        copy.save('images/list' + str(x) + '.jpg', quality=95)

def generateDeadsPicture():
    """Generte a picture listing all dead players"""
    deadPlayers = retrieveDeadData()
    background = Image.open('images/PERDIDOS.jpg')
    copy = background.copy()
    userNum = 6
    y = 800
    for row in range(0, 3):
        x = 150
        for col in range(0, 2):
            name = deadPlayers[userNum][1:]
            circleImg = makeCircleImg(name).resize((300, 300))
            copy.paste(circleImg, (x, y), circleImg)
            x += 500
            userNum += 1
        y += 350

    copy.save('images/lost.jpg', quality=95)

def makeCircleImg(user):
    """Crop picture in a circle
    Args:
        user: string of username
    """
    originalImg = Image.open('images/users/' + user + '.jpg')
    copyImg = originalImg.copy()
    size = originalImg.size
    ellipse = drawEllipse(size)
    copyImg.putalpha(ellipse)
    circleImg = copyImg.crop((0, 0, size[0], size[0]))
    circleImg.save('images/circle.png')
    return circleImg


def drawEllipse(size):
    """Draw ellipse
    Args:
        size: tuple of img size
    """
    ellipse = Image.new("L", size, 0)
    draw = ImageDraw.Draw(ellipse)
    draw.ellipse((0, 0, size[0], size[0]), fill=255)
    return ellipse

def getPostImage(player1, player2, name1, name2):
    """Generate ig pog image
    Args:
        player1: image player1
        player2: image player2
        name1: string username1
        name2: string username2
    Returns:
        string of img path
    """
    vsImage = str(getRandomNumber(2))
    background = Image.open('images/VS' + vsImage + '.jpg')
    backgroundCopy = background.copy()
    backgroundCopy.paste(player1, (45, 60), player1)
    backgroundCopy.paste(player2, (652, 662), player2)
    path =  'images/battles/' + name1 + 'VS' + name2 + '.jpg'
    backgroundCopy.save(path, quality=95)
    return path

def startGame():
    battle()
    for x in range(0, 5):
        for y in range(59, 0, -1):
            print("Faltan " + str(y) + " minutos para la siguiente batalla")
            time.sleep(60)
        battle()

startGame()
