import asyncio
import json
import discord
from discord.ext import commands
import csv
import random


class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.quizDict = {}
        with open("./data/quiz.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.quizDict[row[0]] = row[1]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quiz Cog is Ready")

    @commands.command("퀴즈랭킹")
    async def ranking(self, ctx, arg=None):
        with open("data/score.json", 'r', encoding='utf-8') as f:
            self.score = json.load(f)
        rank = sorted(self.score.items(), key=lambda x: x[1], reverse=True)

        if arg in self.score.keys():
            embed = discord.Embed(
                title='개인 퀴즈 랭킹', description="개인 퀴즈 랭킹입니다.",
                color=discord.Color.blue()
            )
            user = arg
            score = str(self.score.get(arg))
            des = user+'님은 '+score+'점입니다.'
            embed.add_field(name=user, value=des, inline=False)
            await ctx.send(embed=embed)
        elif arg == None:
            embed = discord.Embed(
                title='퀴즈랭킹', description="전체퀴즈랭킹입니다.\n한문제를 맞힐때마다 1점씩 증가해요",
                color=discord.Color.blue()
            )
            i = 1
            for name, score in rank:
                user = str(i)+'.' + name
                ranking = "점수: " + str(score) + "점"
                embed.add_field(name=user, value=ranking, inline=False)
                i += 1
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='퀴즈랭킹', description="입력하신 정보가 없습니다.",
                color=discord.Color.blue()
            )

    @commands.command(name="퀴즈")
    async def quiz(self, ctx):
        problemList = list(self.quizDict.keys())
        problem = random.choice(problemList)
        answer = self.quizDict[problem]
        # await ctx.send(problem)

        embed = discord.Embed(
            title='퀴즈', description=problem, color=discord.Color.blue())
        await ctx.send(embed=embed)

        def checkAnswer(message):
            if message.channel == ctx.channel and answer in message.content:
                return True
            else:
                return False
        try:
            # await self.client.wait_for("message", timeout=10.0, check=checkAnswer)
            # await ctx.send("정답이에요!")

            message = await self.client.wait_for("message", timeout=10.0, check=checkAnswer)
            name = message.author.name
            embed = discord.Embed(
                title='', description=f'{name} 님, 정답이에요 !', color=discord.Color.blue())
            await ctx.send(embed=embed)

            with open("data/score.json", 'r', encoding='utf-8') as f:
                self.score = json.load(f)
            if ctx.author.name in self.score:
                self.score[ctx.author.name] += 1
            else:
                self.score[ctx.author.name] = 1

            with open("data/score.json", 'w', encoding='utf-8') as f:
                json.dump(self.score, f, ensure_ascii=False)

        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='', description=f'땡! 시간초과입니다~ 정답은 {answer}이에요!', color=discord.Color.red())
            await ctx.send(embed=embed)

        # except asyncio.TimeoutError:
            # await ctx.send(f"땡! 시간초과입니다~ 정답은 {answer}이에요!")


def setup(client):
    client.add_cog(Quiz(client))
