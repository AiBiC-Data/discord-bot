# cogs/example.py
from discord.ext import commands
import discord


class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("example Cog is Ready")

    @commands.command(name="임베드")
    async def embed(self, ctx):
        embed = discord.Embed(
            title="Embed의 제목입니다.",
            description="임베드 설명입니다.",
            color=discord.Color.blue())

        embed.add_field(
            name="Field 1 Title",
            value="This is the value for field 1. This is NOT an inline field.",
            inline=False)

        embed.add_field(name="Field 2 Title",
                        value="It is inline with Field 3", inline=True)
        embed.add_field(name="Field 3 Title",
                        value="It is inline with Field 2", inline=True)

        embed.set_author(
            name="작성자 이름",
            url="https://cafe.naver.com/codeuniv",
            icon_url="https://source.unsplash.com/random")

        embed.set_thumbnail(url="https://source.unsplash.com/random")
        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def _ping(self, ctx):
        await ctx.send('pong!')

    @commands.command(name="이름")
    async def _ping(self, ctx):
        await ctx.send(ctx.author.name)


def setup(client):
    client.add_cog(Example(client))
