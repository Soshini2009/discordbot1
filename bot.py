import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COUNT_FILE = os.path.join(os.path.dirname(__file__), "achievement_count.txt")

# ===== 実績番号読み込み =====
def load_count():
    if not os.path.exists(COUNT_FILE):
        return 0
    with open(COUNT_FILE, "r") as f:
        return int(f.read())


# ===== 実績番号保存 =====
def save_count(count):
    with open(COUNT_FILE, "w") as f:
        f.write(str(count))


# ===== 実績入力モーダル =====
class AchievementModal(discord.ui.Modal, title="実績記入フォーム"):

    product = discord.ui.TextInput(label="購入商品")
    amount = discord.ui.TextInput(label="購入数")
    rating = discord.ui.TextInput(label="評価（★5など）")
    comment = discord.ui.TextInput(label="感想", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):

        count = load_count() + 1
        save_count(count)

        embed = discord.Embed(
            title=f"🏆 No.{count}｜実績",
            color=discord.Color.green()
        )

        embed.add_field(name="実績ユーザー", value=interaction.user.mention, inline=False)
        embed.add_field(name="購入商品", value=self.product.value, inline=False)
        embed.add_field(name="購入数", value=self.amount.value, inline=False)
        embed.add_field(name="評価", value=self.rating.value, inline=False)
        embed.add_field(name="感想", value=self.comment.value, inline=False)

        channel = discord.utils.get(interaction.guild.text_channels, name="実績")

        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("✅ 実績を投稿しました！", ephemeral=True)
        else:
            await interaction.response.send_message("⚠ 実績チャンネルが見つかりません。", ephemeral=True)


# ===== ボタン =====
class AchievementButton(discord.ui.View):
    @discord.ui.button(label="実績を記入", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AchievementModal())


# ===== パネル設置 =====
@bot.command()
async def panel(ctx):
    embed = discord.Embed(
        title="📋 実績記入パネル",
        description="ボタンを押して実績を記入してください。",
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=AchievementButton())


@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    auto_replies = {
        "@@@": "ここに定型文を書く",
        "営業時間": "🕒 営業時間は\n平日 18:00〜24:00\n土日 12:00〜24:00 です。",
        "依頼方法": "📩 チケットを作成してご依頼ください。"
    }

    if message.content in auto_replies:
        await message.channel.send(auto_replies[message.content])

    await bot.process_commands(message)


bot.run(TOKEN)



