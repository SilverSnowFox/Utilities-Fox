import requests
import simplejson as json
from discord.ext import tasks, commands


class API(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(hours=1.0)
    async def ServerCount(self):
        count = len(self.client.guilds)

        with open("/data/API_keys.json", "r") as file:
            keys = json.load(file)

            # DisBotList.xyz
            response_1 = requests.post("https://disbotlist.xyz/api/bots/stats", headers={
                "Authorization": keys["disbotlist.xyz"],
                "ServerCount": str(count)
            })

            # DiscordBotList.com
            response_2 = requests.post(f"https://discordbotlist.com/api/v1/bots/{self.client.id}/stats",
                                       headers={
                                           "id": str(self.client.id),
                                           "Authorization": keys["discordbotlist.com"]},
                                       data={
                                           "guilds": str(count)
                                       })

            print(response_1.text)
            print(response_2.text)


def setup(client):
    client.add_cog(API(client))
