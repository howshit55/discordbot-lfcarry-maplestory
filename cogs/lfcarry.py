import os
import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from datetime import datetime, timedelta

LOG_FILE = "lfcarry_log.txt"

def get_week_dates():
    today = datetime.today()
    weekday = today.weekday()
    
    # 计算本周的星期四
    this_thursday = today - timedelta(days=weekday - 3)
    # 计算下周的星期四
    next_thursday = this_thursday + timedelta(days=7)
    
    return this_thursday, next_thursday

class lfcarry_main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name = "lfcarry", description = "找人帶王")
    @app_commands.describe(char = "哪隻角色", boss = "要甚麼王", week="選擇本周或下周")
    @app_commands.choices(
        boss = [
            Choice(name = "混三王", value = "混三王"),
            Choice(name = "混四王", value = "混四王"),
            Choice(name = "貝倫", value = "混貝"),
        ],
        week=[
            Choice(name="本周", value="本周"),
            Choice(name="下周", value="下周"),
        ]
    )
    async def lfcarry(self, interaction: discord.Interaction, char: str, boss: Choice[str], week: Choice[str]):
        # 獲取使用指令的使用者名稱
        customer = interaction.user.name
        # 使用者選擇的選項資料，可以使用name或value取值
        boss = boss.value
        
        # 计算日期
        current_date = datetime.today().strftime("%m/%d")
        
        # 计算日期
        if week.value == "本周":
            week_str = f"本周({current_date})"
        else:
            next_thursday, _ = get_week_dates()
            week_str = f"下周({(next_thursday).strftime('%m/%d')})"
        
        # 记录日志
        log_entry = f"{customer} 的 {char} 要 {week_str} 的 {boss}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
        await interaction.response.send_message(f"{customer} 的 {char} 要 {week_str} 的 {boss}")
    @commands.command(name="lfcarrylog", description="查看lfcarry的日志")    
    async def lfcarrylog(self, ctx: commands.Context):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as log_file:
                logs = log_file.readlines()
            if logs:
                # 使用多行代码块显示日志内容
                log_message = "```\n" + "".join(logs) + "```"
                await ctx.send(log_message)
            else:
                await ctx.send("沒人要王。")
        else:
            await ctx.send("你程式壞了。")
    @commands.command(name="clearlog", description="清除lfcarry的日志")
    async def clearlog(self, ctx: commands.Context):
        if os.path.exists(LOG_FILE):
            # 清除日志内容
            with open(LOG_FILE, "w", encoding="utf-8") as log_file:
                log_file.write("")
            await ctx.send("清除Log。")
        else:
            await ctx.send("你程式壞了。")

async def setup(bot: commands.Bot):
    await bot.add_cog(lfcarry_main(bot))