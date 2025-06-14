import asyncio

import discord
from discord.ext import commands
from discord import app_commands
import db.data_base as db
import db.upd_data_base as upd
from Discord.api_token import TOKEN

intents=discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None,
                   activity=discord.Activity(type=discord.ActivityType.listening, name="пользователей"))

GUILD_ID = 1259803762290069575
logging_channel_id = 1264613639277514774
allowed_channel_ids = 1376950823359086725, 1260461655112814643
admins_roles = { 'Administrator': 1260463377344364584, 'Moderator': 1266377743503986718, 'DD Bot Admin': 1376951791236677764, 'Verifer': 1376951874670039140, 'Verified': 1379025036995985550 }

log_ch = None

async def main():
    async with bot:
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    global log_ch
    log_ch = bot.get_channel(logging_channel_id)
    print(f'LOGING CHANNEL: {log_ch}')
    await log_ch.send(f"Бот запущен (test)")
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Синхронизировано {len(synced)} команд.")
    except Exception as e:
        print(f"Ошибка при синхронизации: {e}")

# @bot.tree.command(name="loggingtest", description="test", guild=discord.Object(id=GUILD_ID))
# async def loggingtest(interaction: discord.Interaction):
#     await log_ch.send("test")

@bot.tree.command(name="admr", description="Регистрация в боте (для админов)", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(text="@tt_username", id="discord id")
@commands.has_permissions(manage_roles=True)
async def register(interaction: discord.Interaction, text: str, id: str):
    try:
        id_int = int(id)
    except:
        await interaction.response.send_message("Неправильно указан айди", ephemeral=True)
        return
    roles = interaction.user.roles
    if any(role.id in (admins_roles['Verifer'], admins_roles['DD Bot Admin']) for role in roles):
        if not await db.get_user_by_dc_id(id_int):
            user = await db.get_user_by_tt_username(text)
            try:
                if user:
                    await db.set_in_dc_group_by_local_id(user[0], 1)
                    await db.set_dc_id_by_local_id(user[0], id_int)
                    await db.set_dc_lastname_by_local_id(user[0], interaction.guild.get_member(id_int).name)
                    await interaction.response.send_message(f"Пользователь <@{id_int}> Подключён к базе данных, tg_id: {user[1]}, tg_lastname: {user[3]}, tg_username: {user[6]}")
                    await log_ch.send(f"Connect <@{id_int}> tg_id: {user[1]}, tg_lastname: {user[3]}, tg_username: {user[6]} \nadmin: {interaction.user.name}")

                    member = interaction.guild.get_member(id_int)
                    if member:
                        verified_role = interaction.guild.get_role(admins_roles['Verified'])  # добавь ID роли в словарь
                        if verified_role:
                            await member.add_roles(verified_role)
                    await upd.update_db(user[0], dc_bot=bot)
                else:
                    new_local_id = await db.user_count() + 1
                    await db.insert_user(
                        local_id= new_local_id,
                        dc_id=id_int,
                        dc_lastname=interaction.guild.get_member(id_int).name,
                        tt_username=text,
                        in_dc_group=1)
                    await upd.update_db(new_local_id, dc_bot=bot)
                    member = interaction.guild.get_member(id_int)
                    if member:
                        verified_role = interaction.guild.get_role(admins_roles['Verified'])  # добавь ID роли в словарь
                        if verified_role:
                            await member.add_roles(verified_role)
                    await interaction.response.send_message(f"Пользователь {text} был занёсен в базу данных <@{id_int}>")
                    await log_ch.send(f"Register <@{id_int}> tg_username: {text} \nadmin: {interaction.user.name}")
            except Exception as e:
                await interaction.response.send_message(f"Произошла ошибка: {e}")
        else:
            await interaction.response.send_message(f"Пользователь уже зарегистрирован <@{id_int}>")
    else:
        await interaction.response.send_message("Вам не позволено использовать эту команду")

@bot.tree.command(name="del", description="Удалить пользователя", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(id="discord id")
async def del_user(interaction: discord.Interaction, id: str):
    id_int = int(id)
    roles = interaction.user.roles
    if any(role.id in (admins_roles['Verifer'], admins_roles['DD Bot Admin']) for role in roles):
        if await db.get_user_by_dc_id(id_int):
            await db.del_user_by_dc_id(id_int)
            await interaction.response.send_message(f"Пользователь <@{id_int}> был удалён из базы данных")
            try:
                member = interaction.guild.get_member(id_int)
                if member:
                    verified_role = interaction.guild.get_role(admins_roles['Verified'])  # добавь ID роли в словарь
                    if verified_role:
                        await member.remove_roles(verified_role)
            except Exception as e:
                await interaction.response.send_message(f"Произошла ошибка: {e}")
            await log_ch.send(f"Delete <@{id_int}> \nadmin: {interaction.user.name}")
        else:
            await interaction.response.send_message(f"Пользователь <@{id_int}> не зарегистрирован")
    else:
        await interaction.response.send_message("Вам не позволено использовать эту команду")

@bot.tree.command(name="userlist", description="Список пользователей", guild=discord.Object(id=GUILD_ID))
async def user_list(interaction: discord.Interaction):
    await interaction.response.send_message(f"ссылка на наш сайт с пользователями {await db.get_users_link()}", ephemeral=True)

@bot.tree.command(name="connect", description="Привязать телеграмм аккаунт", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(id="telegram id or username")
async def connect_tg(interaction: discord.Interaction, id: str):
    if not (interaction.channel.id in allowed_channel_ids):
        await interaction.response.send_message(f"Команды пишем в канале <#{allowed_channel_ids[0]}>, <#{allowed_channel_ids[1]}>", ephemeral=True)
        return

    user = await db.get_user_by_dc_id(interaction.user.id)
    if user:
        try:
            tg_id = int(id)
            await db.set_tg_id_by_local_id(user[0], tg_id)
            await interaction.response.send_message("ваш айди был занёсен в базу данных, после поступления вашей заявки на вступления в нашу телеграмм группу, вы будете приняты автоматически ( https://t.me/+uTsIVaKBlHoxYWNi )")
        except:
            tg_username = id.replace('@', '')
            await db.set_tg_username_by_local_id(user[0], tg_username)
            await interaction.response.send_message(
        "ваш юзернейм был занёсен в базу данных, после поступления вашей заявки на вступления в нашу телеграмм группу, вы будете приняты автоматически ( https://t.me/+uTsIVaKBlHoxYWNi )")
    else:
        await interaction.response.send_message("Вы не зарегестрированы в базе данных", ephemeral=True)


if __name__ == "__main__":
    asyncio.run(main())