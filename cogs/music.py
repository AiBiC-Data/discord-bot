import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from .module.youtube import getUrl


class Music(commands.Cog):
    def __init__(self, client):
        option = {
            'format': 'bestaudio/best',
            'noplaylist': True,
        }
        self.client = client
        self.DL = YoutubeDL(option)

    @commands.command(name="음악재생")
    async def play_music(self, ctx, *keywords):
        # 봇의 음성 채널 연결이 없으면
        if ctx.voice_client is None:
            # 명령어(ctx) 작성자(author)의 음성 채널에 연결 상태(voice)
            if ctx.author.voice:
                # 봇을 명령어 작성자가 연결되어 있는 음성 채널에 연결
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(
                    title='오류 발생', description="음성 채널에 들어간 후 명령어를 사용 해 주세요!", color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        # 봇이 음성채널에 연결되어 있고, 재생중이라면
        elif ctx.voice_client.is_playing():
            # 현재 재생중인 음원을 종료
            ctx.voice_client.stop()

        keyword = ' '.join(keywords)
        url = getUrl(keyword)
        await ctx.send(url)

        embed = discord.Embed(
            title='음악 재생', description='음악 재생을 준비하고있어요. 잠시만 기다려 주세요!', color=discord.Color.red())
        await ctx.send(embed=embed)

        data = self.DL.extract_info(url, download=False)
        link = data['url']
        title = data['title']
        uploader = data['uploader']
        uploader_url = data['uploader_url']
        view_count = data['view_count']
        average_rating = data['average_rating']
        like_count = data['like_count']
        thumbnail = data['thumbnail']

        ffmpeg_options = {
            'options': '-vn',  # 비디오를 사용하지 않는다.
            # ffmpeg에서 연결이 끊기는 경우 재연결을 시도한다.
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        }
        player = discord.FFmpegPCMAudio(
            link, **ffmpeg_options, executable="C:/Users/whrnj/Documents/디스코드봇/ffmpeg/bin/ffmpeg")
        ctx.voice_client.play(player)

        embed = discord.Embed(
            title=f'{title}', url=url, color=discord.Color.red()
        )
        embed.set_author(name=uploader, url=uploader_url)
        embed.add_field(name='조회수', value=view_count, inline=True)
        embed.add_field(name='평점', value=average_rating, inline=True)
        embed.add_field(name='좋아요 수', value=like_count, inline=True)
        embed.set_image(url=thumbnail)
        await ctx.send(embed=embed)

    @commands.command(name="음악종료")
    async def quit_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(
                title='', description='음악 재생을 종료합니다.', color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name="일시정지")
    async def pause_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()
            embed = discord.Embed(
                title='', description='음악을 일시정지 합니다.', color=discord.Color.red())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title='', description='노래가 정지 중 입니다.', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="다시시작")
    async def resume_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_paused():
            voice.resume()
            embed = discord.Embed(
                title='', description='음악을 다시재생 합니다.', color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='', description='노래가 재생중입니다.', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is Ready")


def setup(client):
    client.add_cog(Music(client))
