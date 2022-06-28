import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Melon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = "https://www.melon.com/chart/index.htm"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Melon Cog is Ready")

    @commands.command(name="멜론차트")
    async def melon(self, ctx):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select(
            "div.wrap > div.wrap_song_info")
        main = ''
        for item in data[0:100:2]:
            title = item.select_one('a').text.replace('\n', '')
            main = main + '\n' + title
        # print(main)
        embed = discord.Embed(
            title="멜론차트 순위", description=main, color=discord.Color.blue())

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Melon(client))
