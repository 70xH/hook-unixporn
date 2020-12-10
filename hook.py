import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

while True:
    try:
        with open('db.json') as json_file:
            db = json.load(json_file)
    except:
        db = []

    webhook_url = "WEBHOOK_URL"
    subreddit = 'unixporn'

    req = requests.get(f"https://www.reddit.com/r/{subreddit}/new/.json", headers={
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "discord-feed-bot"})

    try:
        posts = req.json()['data']['children']
    except:
        continue

    for post in posts:
        if post['data']['name'] not in db:
            db.append(post['data']['name'])
            webhook = DiscordWebhook(url=webhook_url)
            permalink = f"https://www.reddit.com{post['data']['permalink']}"

            if post['data']['thumbnail'] == 'self':
                i = 1
            elif post['data']['is_video']:
                embed = DiscordEmbed(title=post['data']['title'], url=permalink)
                embed.set_image(url=post['data']['thumbnail'])
                embed.set_footer(text=f"Video posted by {post['data']['author']}")
            else:
                embed = DiscordEmbed(title=post['data']['title'], url=permalink)
                embed.set_author(name=post['data']['author'])
                embed.set_image(url=post['data']['url'])
                embed.set_footer(text=f"{post['data']['ups']}", icon_url="https://pngimg.com/uploads/like/like_PNG64.png")

                webhook.add_embed(embed)
                webhook.execute()
                time.sleep(3)


    with open('db.json', 'w') as outfile:
        json.dump(db,outfile)
