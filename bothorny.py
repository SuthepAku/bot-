import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# สร้าง dictionary เพื่อติดตามการแนะนำตัวของผู้ใช้
user_introductions = {}

@client.event
async def on_ready():
    print(f'บอทเปิดใช้งานแล้วในชื่อ {client.user}')
    try:
        synced = await client.tree.sync()
        print(f'ซิงค์ {len(synced)} คำสั่งแล้ว')
    except Exception as e:
        print(f'ไม่สามารถซิงค์คำสั่งได้: {e}')

@client.event
async def on_member_join(member):
    channel = client.get_channel(1256977666414874764)
    if channel is not None:
        tex = f"{member.mention} ยินดีต้อนรับ! กรุณาแนะนำตัวด้วยการใช้คำสั่ง `/แนะนำตัว` โดยใส่ชื่อเล่น อายุ และเพศของคุณใน {member.guild.name}!"
        await channel.send(tex)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1256977691715047424)
    if channel is not None:
        tex = f"{member.mention} ลาก่อนจาก {member.guild.name}!"
        await channel.send(tex)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    mes = message.content
    if mes == 'hello bot':
        await message.channel.send('Hello! I am bot')
    elif mes == 'hi bot':
        await message.channel.send(f'Hello! I am bot {message.author.name}')
    elif mes == 'ชื่อเล่น อายุ เพศ':
        await message.channel.send(f'ok {message.author.name}')
    await client.process_commands(message)

@client.command()
async def My(ctx):
    await ctx.send(f'โปรดพิมพ์ !am <ชื่อเล่น> <อายุ> <เพศ> {ctx.author.name}!')

@client.command()
async def am(ctx, *, arg):
    await ctx.send(arg)

@client.tree.command(name='hellobot', description='ตอบกลับด้วย Hello')
async def hellocommand(interaction):
    await interaction.response.send_message('Hello!')

@client.tree.command(name='แนะนำตัว', description='ชื่อเล่น อายุ เพศ')
@app_commands.describe(name="ชื่อ อายุ เพศ")
async def namecommand(interaction: discord.Interaction, name: str):
    # แจ้งว่ากำลังดำเนินการ
    await interaction.response.defer(thinking=True)

    # บันทึกว่าผู้ใช้ได้แนะนำตัวแล้ว
    user_introductions[interaction.user.id] = True

    # ส่งข้อความแนะนำตัวไปยังช่องที่กำหนด
    channel_id = 1079367503525974078  # แทนที่ด้วย ID ของช่องที่ต้องการส่งข้อความไป
    channel = client.get_channel(channel_id)
    if channel is not None:
        await channel.send(f'ผู้ใช้ {interaction.user.mention} ได้แนะนำตัวว่า: {name}')

    # ตอบกลับการอินเตอร์แอคชั่น
    await interaction.followup.send('ok!แนะนำตัวเสร็จแล้ว โปรพิมพ์*K ตัวพิมพ์ใหญ่นะ เพื่อเข้ามาEnjoy')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!H':
        # ตรวจสอบว่าผู้ใช้ได้แนะนำตัวแล้วหรือยัง
        if user_introductions.get(message.author.id, False):
            role_name = "1101"
            role = discord.utils.get(message.guild.roles, name=role_name)

            if role:
                try:
                    await message.author.add_roles(role)
                    await message.channel.send(f"คุณได้รับ {role.name} แล้ว!")
                except discord.Forbidden:
                    await message.channel.send("ไม่สามารถมอบบทบาทให้ผู้ใช้งานได้")
            else:
                await message.channel.send("ไม่พบบทบาทที่ต้องการในเซิร์ฟเวอร์")
        else:
            await message.channel.send("กรุณาแนะนำตัวด้วยคำสั่ง `/แนะนำตัว` ก่อน")

    await client.process_commands(message)

server_on()

client.run(os.getenv('TOKEN'))
