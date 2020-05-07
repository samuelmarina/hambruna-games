from igdata import getAllComments, obtainIgPageID, getUserProfilePic
from firebase import firebase
import json
import shutil
import requests

userDict = dict() #dictionary of users (username, [power])
realtimeDatabase = "YOUR-DATABASE-URL"
firebase = firebase.FirebaseApplication(realtimeDatabase, None)

def getCommentArray():
    """Get comments from a ig post
    Returns:
        array of comments as strings
    """
    commentsResponse = getAllComments() #API call
    responseArray = commentsResponse['json_data']['data'] #object of comments
    commentsArray = [] #comments array
    for x in range(0, len(responseArray)):
        commentsArray.append(responseArray[x]['text'])
    return commentsArray

def getUsers(comments):
    """Get users that are going to be part of the game
    and add them do the users dictionary
    Args:
        comments: array of comments as strings
    Comment format to add:
        @username : power
    """
    for comment in comments:
        if comment[0] != '@': #avoid comments that don't follow the format
            continue

        user = ""
        power = ""
        count = 0
        while comment[count] != " ": # add username
            user += comment[count]
            count += 1

        while comment[count] == " " or comment[count] == ":": #skip to power
            count += 1

        while count < len(comment): # add power
            power += comment[count]
            count += 1

        getProfilePicture(user[1:]) #get user's profile picture
        setUsers(user, power)   #set dictionary of users

def getProfilePicture(user):
    """Get user's profile picture
    Args:
        user: user to get the picture from
    """
    profilePicResponse = getUserProfilePic(user) #API call
    try:
        url = profilePicResponse['json_data']['business_discovery']['profile_picture_url'] #url endpoint

        resp = requests.get(url, stream=True) #get request
        local_file = open('images/users/' + user + '.jpg', 'wb') #location to save the picture in
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, local_file)
        del resp
    except:
        print("Error: " + user + "\n")


def setUsers(user, power):
    """Add user to dictionary (if exists, add power)
    """
    if user in userDict:
        powers = userDict.get(user)
        powers.append(power)
        userDict[user] = powers
        return
    userDict[user] = [power]

def submitToDatabase():
    """Submit the data to the database
    (users that are part of the game)
    """
    r = getUsers(getCommentArray()) #get users
    for keys in userDict: #add users to database
        data = {
            "User" : keys,
            "Power" : userDict[keys]
        }
        result = firebase.post("Users", data)

def submitDeathDatabase(killer, victim, power, day):
    """Submit data to the database
    (users that died in game)
    """
    data = {
        "Victim" : victim,
        "Killer" : killer,
        "Killed Power": power,
        "Day" : day
    }
    result = firebase.post("Dead", data)

def retrieveData():
    """Get all users currently alive in the game
    Returns:
        array of users ids as strings
    """
    result = firebase.get("Users", "") #get request
    usersID = []    #users id array
    for id in result:
        usersID.append(id)
    return usersID
#
def retrieveDeadData():
    """Get all users dead in the game
    Returns:
        array of users ids as strings
    """
    result = firebase.get("Dead", "") #get request
    deadUsers = []  #users id array
    for victims in result:
        deadUsers.append(getDeadUserByID(victims))
    return deadUsers

def removeUserByID(id):
    """Remove user by database id"""
    result = firebase.delete("Users", id) #delete request

def getUserByID(id):
    """Get user by database id
    Args:
        id: string of user's id
    Returns:
        array of username and its power(s)
    """
    result = firebase.get("Users/" + id, "") #get database request
    username = result["User"]
    power = result["Power"]
    return [username, power]
