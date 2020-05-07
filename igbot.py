import instabot

bot = instabot.Bot() #instagram bot

def logIn():
    """Log in
    """
    username = "" #your username
    password = "" #your password
    bot.login(username=username, password=password)

def uploadPost(picturePath, caption):
    """Upload picture
    Args:
        picturePath: path of the picture
        caption: caption of the picture
    """
    bot.upload_photo(picturePath, caption=caption)
