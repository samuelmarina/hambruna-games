
![HG Logo](https://github.com/samuelmarina/hambruna-games/blob/master/images/logo.png)
# Hambruna Games
**Hambruna Games** is an Instagram bot that simulates a game similar to "Hunger Games", in which your Instagram followers select which
users participate in the game. The task of the bot is to recreate "battles" selecting two players, randomly choosing a winner and posting
a "VS" picture with a caption announcing the battle.

### Important
Running Instagram bots is not longer safe - you may get easily detected and banned by Instagram. Read why [here](https://likeup.me/bots-are-dead/?utm_source=instabot-github-readme)

---

## Quickstart
1. Replace all the important credentials in the defines.py, igdata.py and igbot.py files.
2. Populate your database with the following object format:
```
data = {
  "User": username,
  "Power": [powers]
 }
 ```
3. To start the simulation, simply run this script:
```
python3 gamesimulator.py
```

## Author

* **Samuel Mariña** - *Personal Project*

## Acknowledgments
I made use of two repositories to make this project possible:
* [**Instabot**](https://github.com/instagrambot/instabot)
* [**blog_code**](https://github.com/jstolpe/blog_code) by Justin Stolpe
