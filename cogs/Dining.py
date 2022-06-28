import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Dining(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_url = "https://www.mangoplate.com"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dining Cog is Ready")

    @commands.command(name="맛집")
    async def restaurant(self, ctx, *args):
        keyword = ' '.join(args)
        url = f"https://www.mangoplate.com/search/{keyword}"

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select(
            "li.server_render_search_result_item > div.list-restaurant-item")
        if len(data) > 5:
            limit = 5
        else:
            limit = len(data)
        for item in data[:limit]:
            thumbnail = item.select_one('img').get('data-original')
            link = item.select_one('a').get('href')
            title = item.select_one('h2.title').text.replace('\n', '')
            rating = item.select_one('strong.search_point').text
            category = item.select_one('p.etc').text
            view = item.select_one('span.view_count').text
            review = item.select_one('span.review_count').text
            if rating == '':
                rating = '0'
            embed = discord.Embed(
                title=title, description=category, color=discord.Color.blue())
            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name='평점', value=rating)
            embed.add_field(name='조회수', value=view)
            embed.add_field(name='리뷰수', value=review)
            embed.add_field(
                name='링크', value="https://www.mangoplate.com"+link, inline=False)

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Dining(client))
