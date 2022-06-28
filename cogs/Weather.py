import discord
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import requests


class Recommandation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = "https://weather.naver.com/today"
        with open("./data/weather.json", 'r', encoding='utf-8') as f:
            self.weatherDict = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather Cog is Ready")

    @commands.command(name="날씨")
    async def restaurant(self, ctx):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("div.weather_area > div.weather_now")

        for item in data:
            des = item.select_one('span.weather').text.replace('\n', '')
        wea_des = self.weatherDict[des]

        embed = discord.Embed(
            title="오늘의 날씨: " + des, description=wea_des, color=discord.Color.blue())

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Recommandation(client))
