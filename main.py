# -*- coding: utf-8 -*-
import io
import urllib.request
import discord
import asyncio
import random
import time
from discord import VerificationLevel
from discord.ext import commands
import pytz
import asyncio
from discord import File
from zipfile import ZipFile
import re
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext import commands, tasks
from itertools import cycle
import requests
import json
import datetime
from datetime import datetime

from discord.ext.commands import BadArgument

comandos = "https://cdn.discordapp.com/attachments/771470980324524043/778708215026286652/comandos.png"

lista_spam = []

TOKEN = 'SUA TOKEN'
time_zone = pytz.timezone("Brazil/East")
date_time = datetime.now(time_zone)
date = date_time.strftime("%d/%m as %H:%M")

def get_prefix(client, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except Exception as e:
        var = str(e)
        var = var.replace("'", '')
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(var)] = '!'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

async def apenas_RD(ctx):
    return ctx.message.author.id == 742592151875223658

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

bots_status = cycle(['💎 Equipe Alliance - https://discord.gg/eyHv6wR', '⚠️ Prefix "!"', '‍🔒 Alliance Security', '👑 Server Alliance - https://discord.gg/eyHv6wR', 'Criado por [ALC]RD#8566', '📌 Caso tenha algum erro para reportar referente ao Alliance Security... Entre em nosso servidor'])

@client.event
async def on_ready():
    print('-------------------------')
    print('BOT - online')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('---------STATUS----------')
    change_status.start()
    diaria.start()

@tasks.loop(seconds=60)
async def diaria():
    time_zone = pytz.timezone("Brazil/East")
    date_time = datetime.now(time_zone)
    date = date_time.strftime("%H%M")
    date = int(date)
    date_date = date_time.strftime("%d/%m as %H:%M")
    if date == 0000:
        cc = client.get_channel(806661316281761873)
        await cc.send(f"Backup do dia {date_date}")
        await cc.send('', file=discord.File('main.py', 'main.py'))
        await cc.send('', file=discord.File('prefixes.json', 'prefixes.json'))
        await cc.send('', file=discord.File('anti_spam.json', 'anti_spam.json'))
        await cc.send('', file=discord.File('bloqueador_links.json', 'bloqueador_links.json'))
        await cc.send('', file=discord.File('canal_log.json', 'canal_log.json'))
        await cc.send('', file=discord.File('canal_report.json', 'canal_report.json'))
        await cc.send('', file=discord.File('status_bot.json', 'status_bot.json'))

    if date == 1200:
        cc = client.get_channel(806661316281761873)
        await cc.send(f"Backup do dia {date_date}")
        await cc.send('', file=discord.File('main.py', 'main.py'))
        await cc.send('', file=discord.File('prefixes.json', 'prefixes.json'))
        await cc.send('', file=discord.File('anti_spam.json', 'anti_spam.json'))
        await cc.send('', file=discord.File('bloqueador_links.json', 'bloqueador_links.json'))
        await cc.send('', file=discord.File('canal_log.json', 'canal_log.json'))
        await cc.send('', file=discord.File('canal_report.json', 'canal_report.json'))
        await cc.send('', file=discord.File('status_bot.json', 'status_bot.json'))


@tasks.loop(seconds=120)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bots_status)))

@client.event
async def on_guild_join(guild):
    await guild.create_role(name="ModSecurity[ALC]")
    perms = discord.Permissions(send_messages=False, read_messages=True)
    await guild.create_role(name="Mute[ALC]", permissions=perms)

    #prefix

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    #anti link

    with open('bloqueador_links.json', 'r') as f:
        bloqueador_links = json.load(f)

    bloqueador_links[str(guild.id)] = 'True'

    with open('bloqueador_links.json', 'w') as f:
        json.dump(bloqueador_links, f, indent=4)

    #antispam

    with open('anti_spam.json', 'r') as f:
        anti_spam = json.load(f)

    anti_spam[str(guild.id)] = 'True'

    with open('anti_spam.json', 'w') as f:
        json.dump(anti_spam, f, indent=4)


@client.event
async def on_guild_remove(guild):
    #prefix

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    del prefixes[str(guild.id)]

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    #canal report

    with open('canal_report.json', 'r') as f:
        canal_report = json.load(f)

    del canal_report[str(guild.id)]

    with open('canal_report.json', 'w') as f:
        json.dump(canal_report, f, indent=4)

    #anti link

    with open('bloqueador_links.json', 'r') as f:
        bloqueador_links = json.load(f)

    del bloqueador_links[str(guild.id)]

    with open('bloqueador_links.json', 'w') as f:
        json.dump(bloqueador_links, f, indent=4)

    #anti spam

    with open('anti_spam.json', 'r') as f:
        anti_spam = json.load(f)

    del anti_spam[str(guild.id)]

    with open('anti_spam.json', 'w') as f:
        json.dump(anti_spam, f, indent=4)

@client.event
async def on_message(message):
    def _check(m):
        return (m.author == message.author and (datetime.utcnow() - m.created_at).seconds < 15)

    if not message.author.bot:
        try:
            with open('anti_spam.json', 'r') as f:
                anti_spam = json.load(f)

            antispam = anti_spam[str(message.guild.id)]

            if len(list(filter(lambda m: _check(m), client.cached_messages))) >= 9 and antispam == 'True' and message.author.id not in lista_spam:
                lista_spam.append(message.author.id)
                try:
                    guild_local = message.guild
                    user = message.author
                    mutado = discord.utils.get(guild_local.roles, name='Mute[ALC]')
                    if mutado not in user.roles:
                        embed000 = discord.Embed(title="",
                                                 description="🤐 {} foi mutado no servidor por 10 minutos".format(user.mention),
                                                 color=0xffff00)
                        embed000.set_footer(text=f"AntiSpam Alliance - {date}")
                        await message.channel.send(embed=embed000)
                        await user.add_roles(mutado)
                    await asyncio.sleep(10 * 60)
                    await user.remove_roles(mutado)
                    lista_spam.remove(user.id)
                    if mutado not in user.roles:
                        embed000 = discord.Embed(title="",
                                                 description="😁 {} foi desmutado do servidor".format(user.mention),
                                                 color=0xffff00)
                        embed000.set_footer(text=f"AntiSpam Alliance - {date}")
                        await message.channel.send(embed=embed000)
                    for guild_local_channel in guild_local.channels:
                        channel = guild_local_channel
                        overwrite = channel.overwrites_for(mutado)
                        overwrite.send_messages = False
                        await channel.set_permissions(mutado, overwrite=overwrite)
                except:
                    pass
        except:
            pass
    urls = re.findall('http[s]?://discord.',
                      message.content.lower())
    urls2 = message.content.lower().startswith('discord.')
    url3 = re.findall('http[s]?://discord.com/oauth2/authorize?', message.content.lower())
    user = message.author
    guild = message.guild


    try:
        with open('bloqueador_links.json', 'r') as f:
            bloqueador_links = json.load(f)

        block = bloqueador_links[str(message.guild.id)]

        if url3:
            pass
        elif urls and block == "False" and message:
            pass
        elif urls and block == "True" and not message.author.guild_permissions.administrator and message.channel.id != 788874151498088488 and message.channel.id != 798615489013481492:
            await message.delete()
            channel = message.channel
            embed = discord.Embed(title="", description=f"Link bloqueado de {user.mention} ... Proibido links de servidores", color=0xffff00)
            embed.set_footer(text='Para desativar o bloqueador de link digite "!antilink_off"')
            await channel.send(embed=embed)
        elif urls2 and block == "False":
            pass
        elif urls2 and block == "True" and not message.author.guild_permissions.administrator and message.channel.id != 788874151498088488 and message.channel.id != 798615489013481492:
            await message.delete()
            channel = message.channel
            embed = discord.Embed(title="", description=f"Link bloqueado de {user.mention} ... Proibido links de servidores", color=0xffff00)
            embed.set_footer(text='Para desativar o bloqueador de link digite "!antilink_off"')
            await channel.send(embed=embed)
    except Exception as e:
        try:
            var = str(e)
            var = var.replace("'", '')
            var = int(var)

            with open('bloqueador_links.json', 'r') as f:
                bloqueador_links = json.load(f)

            bloqueador_links[str(var)] = 'True'

            with open('bloqueador_links.json', 'w') as f:
                json.dump(bloqueador_links, f, indent=4)
        except:
            pass

    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    mensagem = message.content
    autor = message.author
    canal = message.channel

    try:
        with open('canal_log.json', 'r') as f:
            canal_log = json.load(f)

        canal_log_json = canal_log[str(message.guild.id)]['canal']
        guild_log_json = canal_log[str(message.guild.id)]['guild']
        LOG_CHANNEL = client.get_channel(int(canal_log_json))

        if message.guild.id == int(guild_log_json):
            embed = discord.Embed(title=f'{autor}',
                                  description=f'📝 **Mensagem de texto deletada**\n\n**Canal de texto:** {canal.mention}\n\n**Mensagem:**\n```{mensagem}```',
                                  color=0xff0000)
            embed.set_footer(text=f'ID do usuário: {autor.id} • {date}')
            await LOG_CHANNEL.send(embed=embed)
    except:
        pass


@client.event
async def on_message_edit(before, after):
    try:
        if before.message.author.id == 735316407322935317:
            pass
        #Alliance Security
        elif before.message.author.id == 742814840825053235:
            pass
        #Lorrita
        elif before.message.author.id == 762807113575432262:
            pass
        #Loritta
        elif before.message.author.id == 297153970613387264:
            pass
        #roovy
        elif before.message.author.id == 234395307759108106:
            pass
        else:
            guild = before.channel.guild

            with open('canal_log.json', 'r') as f:
                canal_log = json.load(f)

            canal_log_json = canal_log[str(guild.id)]['canal']
            guild_log_json = canal_log[str(guild.id)]['guild']
            LOG_CHANNEL = client.get_channel(int(canal_log_json))

            embed = discord.Embed(title=f'{before.author.name}',
                                  description=f'📝 {before.author.mention} **editou uma mensagem de texto**\n\n**Canal de texto:** {before.channel.mention}\n\n**Antiga mensagem:**\n```{before.content}```\n**Nova mensagem:**\n```{after.content}```',
                                  color=0xffff00)
            embed.set_footer(text=f'ID do usuário: {before.author.id} • {date}')
            await LOG_CHANNEL.send(embed=embed)
    except:
        pass

@client.event
async def on_member_ban(guild, user):
    try:
        with open('canal_log.json', 'r') as f:
            canal_log = json.load(f)

        canal_log_json = canal_log[str(guild.id)]['canal']
        guild_log_json = canal_log[str(guild.id)]['guild']
        LOG_CHANNEL = client.get_channel(int(canal_log_json))

        if guild.id == int(guild_log_json):
            embed = discord.Embed(title=f'{user.name}#{user.discriminator}',
                                  description=f'🚫 **{user.name}** **foi banido!**',
                                  color=0x23d160)
            embed.set_footer(text=f'ID do usuário: {user.id} • {date}')
            await LOG_CHANNEL.send(embed=embed)
    except:
        pass


@client.event
async def on_member_unban(guild, user):
    try:
        with open('canal_log.json', 'r') as f:
            canal_log = json.load(f)

        canal_log_json = canal_log[str(guild.id)]['canal']
        guild_log_json = canal_log[str(guild.id)]['guild']
        LOG_CHANNEL = client.get_channel(int(canal_log_json))

        if guild.id == int(guild_log_json):
            embed = discord.Embed(title=f'{user.name}#{user.discriminator}',
                                  description=f'🤝 **{user.name}** **foi desbanido!**',
                                  color=0x23d160)
            embed.set_footer(text=f'ID do usuário: {user.id} • {date}')
            await LOG_CHANNEL.send(embed=embed)
    except:
        pass

@client.event
async def on_voice_state_update(member, before, after):
    try:
        guild = member.guild

        with open('canal_log.json', 'r') as f:
            canal_log = json.load(f)

        canal_log_json = canal_log[str(guild.id)]['canal']
        guild_log_json = canal_log[str(guild.id)]['guild']
        LOG_CHANNEL = client.get_channel(int(canal_log_json))

        if guild.id == int(guild_log_json):
            vc_before = before.channel
            vc_after = after.channel
            if vc_before == vc_after:
                return
            if vc_before is None:
                embed = discord.Embed(title=f'{member.name}#{member.discriminator}',
                                      description=f'👉🎤{member.mention} **entrou no canal de voz** `{vc_after.name}`',
                                      color=0x23d160)
                embed.set_footer(text=f'ID do usuário: {member.id} • {date}')
                await LOG_CHANNEL.send(embed=embed)

            elif vc_after is None:
                embed = discord.Embed(title=f'{member.name}#{member.discriminator}',
                                      description=f'👈🎤{member.mention} **saiu do canal de voz** `{vc_before.name}`',
                                      color=0x23d160)
                embed.set_footer(text=f'ID do usuário: {member.id} • {date}')
                await LOG_CHANNEL.send(embed=embed)
            else:
                embed = discord.Embed(title=f'{member.name}#{member.discriminator}',
                                      description=f'🏃‍♂️🎤{member.mention} **foi movido de** `{vc_before.name}` **para** `{vc_after.name}`',
                                      color=0x23d160)
                embed.set_footer(text=f'ID do usuário: {member.id} • {date}')
                await LOG_CHANNEL.send(embed=embed)
    except:
        pass

@client.command(pass_context=True)
@commands.check(apenas_RD)
async def reset(ctx):
    await ctx.send('start')
    for guild in client.guilds:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '!'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        # anti link

        with open('bloqueador_links.json', 'r') as f:
            bloqueador_links = json.load(f)

        bloqueador_links[str(guild.id)] = 'True'

        with open('bloqueador_links.json', 'w') as f:
            json.dump(bloqueador_links, f, indent=4)

        # antispam

        with open('anti_spam.json', 'r') as f:
            anti_spam = json.load(f)

        anti_spam[str(guild.id)] = 'True'

        with open('anti_spam.json', 'w') as f:
            json.dump(anti_spam, f, indent=4)

    await ctx.send('pronto')

@client.command(pass_context=True)
@commands.check(apenas_RD)
async def backup(ctx):
    await ctx.send('', file=discord.File('prefixes.json', 'prefixes.json'))
    await ctx.send('', file=discord.File('anti_spam.json', 'anti_spam.json'))
    await ctx.send('', file=discord.File('bloqueador_links.json', 'bloqueador_links.json'))
    await ctx.send('', file=discord.File('canal_log.json', 'canal_log.json'))
    await ctx.send('', file=discord.File('canal_report.json', 'canal_report.json'))
    await ctx.send('', file=discord.File('status_bot.json', 'status_bot.json'))

@client.command(pass_context=True)
async def desativar_log(ctx):
    errado = client.get_emoji(id=754710506559766530)
    atencao = client.get_emoji(id=754710505821831228)
    seta = client.get_emoji(id=754710505695871077)
    loading = client.get_emoji(id=754710506652303480)
    verf = client.get_emoji(id=754710506631331972)
    user = ctx.message.author
    guild = ctx.message.guild
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        msg = await ctx.send("{}".format(loading))
        time.sleep(1)
        try:
            with open('canal_log.json', 'r', encoding='utf8') as f:
                canal_log = json.load(f)

            del canal_log[str(guild.id)]

            with open('canal_log.json', 'w', encoding='utf8') as f:
                json.dump(canal_log, f, indent=4, sort_keys=True, ensure_ascii=False)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O canal para receber os **logs** foi removido",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            embed000 = discord.Embed(title="",
                                     description=f"{errado} O canal para receber os **logs** não foi configurado, assim não temos como remover",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')

@client.command(pass_context=True)
async def canal_log(ctx, *, arg: int):
    errado = client.get_emoji(id=754710506559766530)
    atencao = client.get_emoji(id=754710505821831228)
    seta = client.get_emoji(id=754710505695871077)
    loading = client.get_emoji(id=754710506652303480)
    verf = client.get_emoji(id=754710506631331972)
    user = ctx.message.author
    guild = ctx.message.guild
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            msg = await ctx.send("{}".format(loading))
            time.sleep(1)

            id_canal = client.get_channel(arg)

            with open('canal_log.json', 'r', encoding='utf8') as f:
                canal_log = json.load(f)

            with open('canal_log.json', 'w', encoding='utf8') as f:
                canal_log[str(ctx.message.guild.id)] = {}
                canal_log[str(ctx.message.guild.id)]['guild'] = f'{ctx.message.guild.id}'
                canal_log[str(ctx.message.guild.id)]['canal'] = f'{arg}'
                json.dump(canal_log, f, indent=4, sort_keys=True, ensure_ascii=False)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O canal para receber os **logs** foi definido com sucesso\n{seta} **Nome:** {id_canal}\n{seta} **ID:** {arg}",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def antilink_off(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        seta = client.get_emoji(id=754710505695871077)
        loading = client.get_emoji(id=754710506652303480)
        verf = client.get_emoji(id=754710506631331972)
        try:
            msg = await ctx.send("{}".format(loading))
            time.sleep(1)
            guild = ctx.message.guild

            with open('bloqueador_links.json', 'r') as f:
                bloqueador_links = json.load(f)

            bloqueador_links[str(guild.id)] = 'False'

            with open('bloqueador_links.json', 'w') as f:
                json.dump(bloqueador_links, f, indent=4)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O Bloqueador de Links foi **DESATIVADO**",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def antilink_on(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        seta = client.get_emoji(id=754710505695871077)
        loading = client.get_emoji(id=754710506652303480)
        verf = client.get_emoji(id=754710506631331972)
        try:
            msg = await ctx.send("{}".format(loading))
            time.sleep(1)
            guild = ctx.message.guild
            with open('bloqueador_links.json', 'r') as f:
                bloqueador_links = json.load(f)

            bloqueador_links[str(guild.id)] = 'True'

            with open('bloqueador_links.json', 'w') as f:
                json.dump(bloqueador_links, f, indent=4)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O Bloqueador de Links foi **ATIVADO**",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def antispam_on(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        seta = client.get_emoji(id=754710505695871077)
        loading = client.get_emoji(id=754710506652303480)
        verf = client.get_emoji(id=754710506631331972)
        try:
            msg = await ctx.send("{}".format(loading))
            time.sleep(1)
            guild = ctx.message.guild
            with open('anti_spam.json', 'r') as f:
                anti_spam = json.load(f)

            anti_spam[str(guild.id)] = 'True'

            with open('anti_spam.json', 'w') as f:
                json.dump(anti_spam, f, indent=4)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O AntiSpam foi **ATIVADO**",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def antispam_off(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        seta = client.get_emoji(id=754710505695871077)
        loading = client.get_emoji(id=754710506652303480)
        verf = client.get_emoji(id=754710506631331972)
        try:
            msg = await ctx.send("{}".format(loading))
            time.sleep(1)
            guild = ctx.message.guild
            with open('anti_spam.json', 'r') as f:
                anti_spam = json.load(f)

            anti_spam[str(guild.id)] = 'False'

            with open('anti_spam.json', 'w') as f:
                json.dump(anti_spam, f, indent=4)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O AntiSpam foi **DESATIVADO**",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def canal_report(ctx, *, arg: int):
    errado = client.get_emoji(id=754710506559766530)
    atencao = client.get_emoji(id=754710505821831228)
    seta = client.get_emoji(id=754710505695871077)
    loading = client.get_emoji(id=754710506652303480)
    verf = client.get_emoji(id=754710506631331972)
    user = ctx.message.author
    guild = ctx.message.guild
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            msg = await ctx.send("{}".format(loading))
            time.sleep(1)
            id_canal = client.get_channel(arg)
            with open('canal_report.json', 'r') as f:
                canal_report = json.load(f)

            canal_report[str(guild.id)] = f'{arg}'

            with open('canal_report.json', 'w') as f:
                json.dump(canal_report, f, indent=4)

            embed000 = discord.Embed(title="",
                                     description=f"{verf} O canal para receber os **reports** foi definido com sucesso\n{seta} **Nome:** {id_canal}\n{seta} **ID:** {arg}",
                                     color=0xffff00)
            embed000.set_footer(text=f"Aplicação do {user.name}")
            await msg.edit(content=None, embed=embed000)
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def prefix(ctx, *, arg):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = arg

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Prefix mudou para = {arg}")
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def mod(ctx):
    errado = client.get_emoji(id=754710506559766530)
    atencao = client.get_emoji(id=754710505821831228)
    verf = client.get_emoji(id=754710506631331972)
    manutencao = client.get_emoji(id=754710505867706409)
    certo = client.get_emoji(id=754710505855123466)
    seta = client.get_emoji(id=754710505695871077)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            mm = ctx.message.mentions[0]
            embed = discord.Embed(title="",
                                  description=f'{manutencao} **Painel de Moderação** {manutencao}\n\n**Você realmente quer dar MOD para:**\n{mm.mention}\n\n**Verificação Valida Por:**\n*40 segundos*',
                                  color=0xffff00)
            embed.set_footer(text=f"Aplicação do {user.name}")
            msg = await ctx.send(embed=embed)
            for emoji in ('✅', '❌'):
                await msg.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

            reaction, user = await client.wait_for('reaction_add', check=check, timeout=40.0)
            if reaction.emoji == '✅':
                perms = discord.Permissions(administrator=False)
                role = "ModSecurity[ALC]"
                role = discord.utils.get(user.guild.roles, name=role)
                await role.edit(permissions=perms)
                await mm.add_roles(role)
                embed = discord.Embed(title="",
                                      description="{} {} Recebeu permissão para utilizar os comandos de moderação".format(
                                          certo, mm.mention),
                                      color=0xffff00)
                embed.set_footer(text=f"Aplicação do {user.name}")
                await msg.edit(embed=embed)
            elif reaction.emoji == '❌':
                embed = discord.Embed(title="",
                                      description="{} {} não vai receber permissão para utilizar os comandos de moderação".format(
                                          errado, mm.mention),
                                      color=0xffff00)
                await msg.edit(embed=embed)
            else:
                await ctx.send("Emoji invalido")
        except IndexError:
            await ctx.send("É necessário inserir uma pessoa Ex: ( `!mod @membro` )  ")
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def unmod(ctx):
    errado = client.get_emoji(id=754710506559766530)
    atencao = client.get_emoji(id=754710505821831228)
    guild_local = ctx.message.guild
    manutencao = client.get_emoji(id=754710505867706409)
    certo = client.get_emoji(id=754710505855123466)
    seta = client.get_emoji(id=754710505695871077)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            mm = ctx.message.mentions[0]
            embed = discord.Embed(title="",
                                  description=f'{manutencao} **Painel de Moderação** {manutencao}\n\n**Você realmente remover o MOD:**\n{mm.mention}\n\n**Verificação Valida Por:**\n*40 segundos*',
                                  color=0xffff00)
            embed.set_footer(text=f"Aplicação do {user.name}")
            msg = await ctx.send(embed=embed)
            for emoji in ('✅', '❌'):
                await msg.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

            reaction, user = await client.wait_for('reaction_add', check=check, timeout=40.0)

            if reaction.emoji == '✅':
                mutado = discord.utils.get(guild_local.roles, name='ModSecurity[ALC]')
                await mm.remove_roles(mutado)
                embed = discord.Embed(title="",
                                      description="{} {} Perdeu a permissão para utilizar os comandos de moderação".format(
                                          certo, mm.mention),
                                      color=0xffff00)
                embed.set_footer(text=f"Aplicação do {user.name}")
                await msg.edit(embed=embed)
            elif reaction.emoji == '❌':
                embed = discord.Embed(title="", description="{} Ação cancelada {}".format(errado, user.mention),
                                      color=0xffff00)
                await msg.edit(embed=embed)
            else:
                await ctx.send("Emoji invalido")
        except IndexError:
            await ctx.send("É necessário inserir uma pessoa Ex: ( `!unmod @membro` )  ")
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def reportar(ctx):
    user = ctx.message.author
    seta = client.get_emoji(id=754710505695871077)
    atencao = client.get_emoji(id=754710505821831228)
    sirene = client.get_emoji(id=754710507222728715)
    date_time = datetime.now()
    date = date_time.strftime("%d/%m/%Y")
    hora = date_time.strftime("%H:%M:%S")
    guild = ctx.message.guild

    def check(m):
        return m.channel == ctx.message.channel and m.author == user

    try:
        member = ctx.message.mentions[0]
        embed = discord.Embed(title='{} Você solicitou uma reclamação'.format(sirene),
                              description='**Acusado =** {}\n**Data =** {}\n**Hora =** {}\n\n**Digite sua reclamação e explique:**'.format(
                                  member.mention, date, hora), color=0xff0000)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/707920032667271228/744794901509701632/report.png")
        await ctx.send(embed=embed)
        r00 = await client.wait_for('message', check=check)
        text = r00.content

        with open('canal_report.json', 'r') as f:
            canal_report = json.load(f)

        pp = int(canal_report["{}".format(guild.id)])

        channel1 = client.get_channel(id=pp)

        embed1 = discord.Embed(title="", description=f'{sirene} {user.mention} **sua reclamação foi enviada**\n\n{seta} *Os ADMs vão analisar sua reclamação*\n\n❤️ *Obrigado por fazer do nosso servidor melhor*', color=0xff0000)
        await ctx.send(embed=embed1)
        embed0 = discord.Embed(title=f'{sirene} Painel de Reclamações {sirene}',
                               description='**Enviado por =** {}\n**Acusado =** {}\n**Data =** *{}*\n**Hora =** *{}*\n\n**Motivo da reclamação:**\n*{}*'.format(
                                   user.mention, member.mention, date, hora, text), color=0xff0000)
        embed0.set_thumbnail(url="https://cdn.discordapp.com/attachments/707920032667271228/744794901509701632/report.png")
        await channel1.send(embed=embed0)
    except IndexError:
        await ctx.send(f"{atencao} É necessário mencionar uma pessoa Ex: ( `!reportar @membro` )")
    except:
        await ctx.send(f"{atencao} O administrador deste servidor precisa configurar o canal para receber os reports ( `!canal_report` )")
    finally:
        pass

@client.command()
async def avatar(ctx):
    try:
        user = ctx.message.mentions[0]
        embed = discord.Embed(title="", description=f"**Clique** [**aqui**]({user.avatar_url}) **para baixar a imagem!**", color=0x2f3136)
        embed.set_image(url=f"{user.avatar_url}")
        embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar_url}")
        await ctx.send(embed=embed)
    except IndexError:
        await ctx.send("É necessário mencionar uma pessoa Ex: ( `!avatar @membro` )  ")
    except:
        await ctx.send("COMANDO ERROR ")
    finally:
        pass

@client.command(pass_context=True)
async def ajuda(ctx):
    manutencao = client.get_emoji(id=754710505867706409)
    config = client.get_emoji(id=754710506505371658)
    sino = client.get_emoji(id=754710506048192543)
    verf = client.get_emoji(id=754710506631331972)
    loading = client.get_emoji(id=754710506652303480)
    pessoa = client.get_emoji(id=754710506190667796)
    member = ctx.message.author
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    guild = ctx.message.guild
    pp = str(prefixes["{}".format(guild.id)])

    loading = client.get_emoji(id=754710506652303480)
    embed = discord.Embed(description=f"{loading}")
    env = await ctx.send(embed=embed)

    index = -1
    while index < 0:
        menu = '🔒'
        embed000 = discord.Embed(title="",
                                 description=f"**Seja bem-vindo ao painel de ajuda da Alliance**\n\n{sino} **Invite-me:** [**clique aqui**](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)\n{manutencao} **Servidor de Suporte:** [**clique aqui**](https://discord.gg/eyHv6wR)\n\n🔒 **➜ Voltar para Início\n**{pessoa} **➜ Comandos de Utilidades**\n{config} **➜ Comandos de Moderação/Administração**",
                                 color=0xffff00)
        embed000.set_author(name=f"Olá {member.name}", icon_url=member.avatar_url)
        embed000.set_thumbnail(url=client.user.avatar_url)
        embed000.set_image(
            url=comandos)
        await env.edit(embed=embed000)
        for emoji in ('🔒', f'{pessoa}', f'{config}'):
            await env.add_reaction(emoji)

        def check(reaction, user):
            return user.id == ctx.message.author.id and str(reaction.emoji) in [f'{pessoa}', f'{config}', '🔒'] and reaction.message.id == env.id

        reaction, user = await client.wait_for('reaction_add', check=check)
        if reaction.emoji == pessoa:
            embed = discord.Embed(title=f"{pessoa} Comandos de Utilidades",
                                  description=f"**{pp}info [@user]** - *Ver informações de membros*\n**{pp}serverinfo** - *Ver informações do Server*\n**{pp}avatar [@user]** - *Monstra o avatar do membro*\n**{pp}config** - *Ver configurações do server*\n**{pp}security** - *Entender sobre a Alliance Security*\n**{pp}status** - *Ver status do bot*\n**{pp}reportar [@user]** - *Reporta um membro para os adms*\n**{pp}limpar_dm** - *Limpa todas conversas do BOT em sua DM*\n**{pp}convite** - *Link para adicionar o Alliance Security*",
                                  color=0xffff00)
            embed.set_image(
                url=comandos)
            await env.edit(embed=embed)
            await env.remove_reaction(pessoa, member)
            reaction, user = await client.wait_for('reaction_add', check=check)

        if reaction.emoji == '🔒':
            await env.remove_reaction(menu, member)
            index = 0 - 1

        if reaction.emoji == config:
            embed = discord.Embed(title=f"{config} Comandos de Moderação/Administração",
                                  description=f"**{pp}kick [@user]** - *Expulsar membro*\n**{pp}ban [@user]** - *Banir membro*\n**{pp}unban [@user]** - *Desbanir membro*\n**{pp}mute [@user]** - *Mutar membro*\n**{pp}unmute [@user]** - *Tirar mute do membro*\n**{pp}limpar** - *Limpa o chat*\n**{pp}scan** - *Scanear cargos e verificar suas permissões*\n**{pp}bloquear** - *Bloquear canal*\n**{pp}liberar** - *Liberar canal*\n**{pp}btodos** - *Bloquear todos canais*\n**{pp}ltodos** - *Liberar todos canais*\n**{pp}mod [@user]** - *Da acesso aos comandos de moderação*\n**{pp}unmod [@user]** - *Remove o acesso aos comandos de moderação*\n\n**{pp}prefix [seu_prefixo]** - *Definir um prefix personalizado*\n**{pp}canal_report [id_canal]** - *Definir o canal para receber os !reportar*\n**{pp}canal_log [id_canal]** - *Definir o canal para receber os logs*\n**{pp}desativar_log** - *Remover o canal para receber os logs*\n**{pp}antilink_on** - *Bloquea todos os links de servidores*\n**{pp}antilink_off** - *Permite os links de servidores*\n**{pp}antispam_on** - *Liga o sistema de anti-spam*\n**{pp}antispam_on** - *Desliga o sistema de anti-spam*",
                                  color=0xffff00)
            embed.set_image(
                url=comandos)
            await env.edit(embed=embed)
            await env.remove_reaction(config, member)
            reaction, user = await client.wait_for('reaction_add', check=check)

        if reaction.emoji == '🔒':
            await env.remove_reaction(menu, member)
            index = 0 - 1

        if reaction.emoji == pessoa:
            embed = discord.Embed(title=f"{pessoa} Comandos de Utilidades",
                                  description=f"**{pp}info [@user]** - *Ver informações de membros*\n**{pp}serverinfo** - *Ver informações do Server*\n**{pp}avatar [@user]** - *Monstra o avatar do membro*\n**{pp}config** - *Ver configurações do server*\n**{pp}security** - *Entender sobre a Alliance Security*\n**{pp}status** - *Ver status do bot*\n**{pp}reportar [@user]** - *Reporta um membro para os adms*\n**{pp}limpar_dm** - *Limpa todas conversas do BOT em sua DM*\n**{pp}convite** - *Link para adicionar o Alliance Security*",
                                  color=0xffff00)
            embed.set_image(
                url=comandos)
            await env.edit(embed=embed)
            await env.remove_reaction(pessoa, member)
            reaction, user = await client.wait_for('reaction_add', check=check)

@client.command(pass_context=True)
async def help(ctx):
    manutencao = client.get_emoji(id=754710505867706409)
    config = client.get_emoji(id=754710506505371658)
    sino = client.get_emoji(id=754710506048192543)
    verf = client.get_emoji(id=754710506631331972)
    loading = client.get_emoji(id=754710506652303480)
    pessoa = client.get_emoji(id=754710506190667796)
    member = ctx.message.author
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    guild = ctx.message.guild
    pp = str(prefixes["{}".format(guild.id)])

    loading = client.get_emoji(id=754710506652303480)
    embed = discord.Embed(description=f"{loading}")
    env = await ctx.send(embed=embed)

    index = -1
    while index < 0:
        menu = '🔒'
        embed000 = discord.Embed(title="",
                                 description=f"**Seja bem-vindo ao painel de ajuda da Alliance**\n\n{sino} **Invite-me:** [**clique aqui**](https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)\n{manutencao} **Servidor de Suporte:** [**clique aqui**](https://discord.gg/eyHv6wR)\n\n🔒 **➜ Voltar para Início\n**{pessoa} **➜ Comandos de Utilidades**\n{config} **➜ Comandos de Moderação/Administração**",
                                 color=0xffff00)
        embed000.set_author(name=f"Olá {member.name}", icon_url=member.avatar_url)
        embed000.set_thumbnail(url=client.user.avatar_url)
        embed000.set_image(
            url=comandos)
        await env.edit(embed=embed000)
        for emoji in ('🔒', f'{pessoa}', f'{config}'):
            await env.add_reaction(emoji)

        def check(reaction, user):
            return user.id == ctx.message.author.id and str(reaction.emoji) in [f'{pessoa}', f'{config}', '🔒'] and reaction.message.id == env.id

        reaction, user = await client.wait_for('reaction_add', check=check)
        if reaction.emoji == pessoa:
            embed = discord.Embed(title=f"{pessoa} Comandos de Utilidades",
                                  description=f"**{pp}kick [@user]** - *Expulsar membro*\n**{pp}ban [@user]** - *Banir membro*\n**{pp}unban [@user]** - *Desbanir membro*\n**{pp}mute [@user]** - *Mutar membro*\n**{pp}unmute [@user]** - *Tirar mute do membro*\n**{pp}limpar** - *Limpa o chat*\n**{pp}scan** - *Scanear cargos e verificar suas permissões*\n**{pp}bloquear** - *Bloquear canal*\n**{pp}liberar** - *Liberar canal*\n**{pp}btodos** - *Bloquear todos canais*\n**{pp}ltodos** - *Liberar todos canais*\n**{pp}mod [@user]** - *Da acesso aos comandos de moderação*\n**{pp}unmod [@user]** - *Remove o acesso aos comandos de moderação*\n\n**{pp}prefix [seu_prefixo]** - *Definir um prefix personalizado*\n**{pp}canal_report [id_canal]** - *Definir o canal para receber os !reportar*\n**{pp}canal_log [id_canal]** - *Definir o canal para receber os logs*\n**{pp}desativar_log** - *Remover o canal para receber os logs*\n**{pp}antilink_on** - *Bloquea todos os links de servidores*\n**{pp}antilink_off** - *Permite os links de servidores*\n**{pp}antispam_on** - *Liga o sistema de anti-spam*\n**{pp}antispam_on** - *Desliga o sistema de anti-spam*",
                                  color=0xffff00)
            embed.set_image(
                url=comandos)
            await env.edit(embed=embed)
            await env.remove_reaction(pessoa, member)
            reaction, user = await client.wait_for('reaction_add', check=check)

        if reaction.emoji == '🔒':
            await env.remove_reaction(menu, member)
            index = 0 - 1

        if reaction.emoji == config:
            embed = discord.Embed(title=f"{config} Comandos de Moderação/Administração",
                                  description=f"**{pp}kick [@user]** - *Expulsar membro*\n**{pp}ban [@user]** - *Banir membro*\n**{pp}unban [@user]** - *Desbanir membro*\n**{pp}mute [@user]** - *Mutar membro*\n**{pp}unmute [@user]** - *Tirar mute do membro*\n**{pp}limpar** - *Limpa o chat*\n**{pp}scan** - *Scanear cargos e verificar suas permissões*\n**{pp}bloquear** - *Bloquear canal*\n**{pp}liberar** - *Liberar canal*\n**{pp}btodos** - *Bloquear todos canais*\n**{pp}ltodos** - *Liberar todos canais*\n**{pp}mod [@user]** - *Da acesso aos comandos de moderação*\n**{pp}unmod [@user]** - *Remove o acesso aos comandos de moderação*\n\n**{pp}prefix [seu_prefixo]** - *Definir um prefix personalizado*\n**{pp}canal_report [id_canal]** - *Definir o canal para receber os !reportar*\n**{pp}canal_log [id_canal]** - *Definir o canal para receber os logs*\n**{pp}desativar_log** - *Remover o canal para receber os logs*\n**{pp}antilink_on** - *Bloquea todos os links de servidores*\n**{pp}antilink_off** - *Permite os links de servidores*\n**{pp}antispam_on** - *Liga o sistema de anti-spam*\n**{pp}antispam_on** - *Desliga o sistema de anti-spam*",
                                  color=0xffff00)
            embed.set_image(
                url=comandos)
            await env.edit(embed=embed)
            await env.remove_reaction(config, member)
            reaction, user = await client.wait_for('reaction_add', check=check)

        if reaction.emoji == '🔒':
            await env.remove_reaction(menu, member)
            index = 0 - 1

        if reaction.emoji == pessoa:
            embed = discord.Embed(title=f"{pessoa} Comandos de Utilidades",
                                  description=f"**{pp}info [@user]** - *Ver informações de membros*\n**{pp}serverinfo** - *Ver informações do Server*\n**{pp}avatar [@user]** - *Monstra o avatar do membro*\n**{pp}config** - *Ver configurações do server*\n**{pp}security** - *Entender sobre a Alliance Security*\n**{pp}status** - *Ver status do bot*\n**{pp}reportar [@user]** - *Reporta um membro para os adms*\n**limpar_dm** - *Limpa todas conversas do BOT em sua DM*\n**{pp}convite** - *Link para adicionar o Alliance Security*",
                                  color=0xffff00)
            embed.set_image(
                url=comandos)
            await env.edit(embed=embed)
            await env.remove_reaction(pessoa, member)
            reaction, user = await client.wait_for('reaction_add', check=check)

@client.command()
async def limpar_dm(ctx):
    messages_to_remove = 10
    guild = ctx.message.guild
    member = ctx.message.author
    verf = client.get_emoji(id=754710506631331972)
    loading = client.get_emoji(id=754710506652303480)
    msg = await ctx.send(f"{loading}")
    try:
        async for message in client.get_user(member.id).history(limit=messages_to_remove):
            if message.author.id == client.user.id:
                await message.delete()
                await asyncio.sleep(0.5)
    except:
        pass
    embed000 = discord.Embed(title='', description=f'{verf} Acabei de limpar todas nossas mensagens {member.mention}', color=0xffff00)
    await msg.edit(content=None, embed=embed000)

@client.command(pass_context=True)
async def links(ctx):
    embed000 = discord.Embed(title="",
                             description="**Aqui está o link para adicionar o Alliance Security**\n•──────────────────────────────────•\n[Clique aqui para adicionar o Alliance Security em seu server](https://discord.com/oauth2/authorize?client_id=742814840825053235&permissions=8&scope=bot)\n•──────────────────────────────────•",
                             color=0x2f3136)
    await ctx.send(embed=embed000)

@client.command(pass_context=True)
async def convite(ctx):
    embed000 = discord.Embed(title="",
                             description="**Aqui está o link para adicionar o Alliance Security**\n•──────────────────────────────────•\n[Clique aqui para adicionar o Alliance Security em seu server](https://discord.com/oauth2/authorize?client_id=742814840825053235&permissions=8&scope=bot)\n•──────────────────────────────────•",
                             color=0x2f3136)
    await ctx.send(embed=embed000)

@client.command(pass_context=True)
async def security(ctx):
    verf = client.get_emoji(id=754710506631331972)
    user = ctx.message.author
    await ctx.send("{} Enviamos nossos dados em sua DM".format(verf))
    embed001 = discord.Embed(color=0xffff00)
    embed001.set_image(
        url="https://cdn.discordapp.com/attachments/742870320074981428/742928798789533778/quem_somos.png")
    await user.send(embed=embed001)
    await user.send(
        "**Equipe Alliance**\n*Somos uma empresa indie, desenvolvemos diversos tipos de BOTS, tanto para servidores grandes como pequenos*\n*Nossa equipe atualmente conta com 5 desenvolvedores*\n*Estamos a mais de 3 anos no mercado e com um servidor com mais de 1200 membros*\n*Mesmos sem muitos recursos prezamos pela qualidade dos produtos desenvolvidos para nossos clientes*")
    embed001 = discord.Embed(title="", description="", color=0xffff00)
    embed001.set_image(
        url="https://cdn.discordapp.com/attachments/742870320074981428/742929351334559775/propositos.png")
    await user.send(embed=embed001)
    await user.send(
        "**Propósitos do Alliance Security**\n- *Trazer segurança aos servidores (flood/spam com contas ou com bots)*\n- *Divulgar dicas para ajudar na moderação dos servidores*\n- *Tirar duvidas em relação de como o discord funciona*\n- *Ter um suporte rapido e eficiente*\n- *Fornecer Backup do seu servidor(cargos, canais e permissões)*")

@client.command(pass_context=True)
async def serverinfo(ctx):
    guild_local = ctx.message.guild
    gg = client.get_guild(guild_local.id)
    guild = ctx.message.guild
    total_text_channels = len(guild.text_channels)
    total_voice_channels = len(guild.voice_channels)
    total_channels = total_text_channels + total_voice_channels
    embed = discord.Embed(title="", description="", color=0xffff00)
    embed.set_author(name=guild_local.name, icon_url=guild_local.icon_url)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="📌 Nome Server", value="{}".format(guild_local.name), inline=True)
    embed.add_field(name="💻 ID Server", value="{}".format(guild_local.id), inline=True)
    embed.add_field(name="👑 Dono", value="{}".format(guild_local.owner), inline=True)
    embed.add_field(name="🌎 Região", value="{}".format(guild_local.region), inline=True)
    embed.add_field(name="👥 Membros", value="{}".format(guild_local.member_count), inline=True)
    embed.add_field(name="⌨️ Canais texto", value=total_text_channels, inline=True)
    embed.add_field(name="🔊 Canais voz", value = total_voice_channels, inline=True)
    embed.add_field(name="📣 Total canais", value=total_channels, inline=True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def definir_status(ctx):
    user = ctx.message.author
    if user.id == 742592151875223658:
        with open('status_bot.json', 'r') as f:
            prefixes = json.load(f)
        user = ctx.message.author
        await ctx.message.delete()
        embed = discord.Embed(title='', description='Bot: ', color=0xffff00)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == user

        r00 = await client.wait_for('message', check=check)
        r00 = r00.content

        prefixes["status_bot"] = str(r00)
        with open("status_bot.json", 'w') as f:
            json.dump(prefixes, f)

        embed = discord.Embed(title='', description='Atualizações: ', color=0xffff00)
        await ctx.send(embed=embed)

        r01 = await client.wait_for('message', check=check)
        r01 = r01.content

        prefixes["status_atualizacoes"] = str(r01)
        with open("status_bot.json", 'w') as f:
            json.dump(prefixes, f)

        embed = discord.Embed(title='', description='**FINALIZADO**', color=0xffff00)
        await ctx.send(embed=embed)


@client.command(pass_context=True)
async def status(ctx):
    with open('status_bot.json', 'r') as f:
        prefixes = json.load(f)

    status_bot = str(prefixes["status_bot"])
    status_atualizacoes = str(prefixes["status_atualizacoes"])

    verf = client.get_emoji(id=754710506631331972)
    stat = client.get_emoji(id=754710506236936212)
    manutencao = client.get_emoji(id=754710505867706409)
    try:
        embed = discord.Embed(title="{} - Status".format(client.user.name),
                              description=f"{verf} **Bot:** {status_bot}\n{manutencao} **Atualizações:** {status_atualizacoes}\n{stat} **Servers:** {str(len(client.guilds))}\n\n*Fique ligado nas atualizações do BOT*\nhttps://discord.gg/eyHv6wR", color=0xffff00)
        embed.set_thumbnail(url=client.user.avatar_url)
        await ctx.send(embed=embed)
    except:
        await ctx.send("ERROR FATAL")
    finally:
        pass

@client.command(pass_context=True)
async def info(ctx):
    atencao = client.get_emoji(id=754710505821831228)
    try:
        user = ctx.message.mentions[0]
        userentrou = str(user.joined_at).split('.', 1)[0]
        usercriou = str(user.created_at).split('.', 1)[0]

        userembed = discord.Embed(
            description=user.name,
            color=0xffff00
        )
        userembed.set_thumbnail(
            url=user.avatar_url,

        )
        userembed.add_field(
            name="ID:",
            inline=True,
            value=user.id
        )
        userembed.add_field(
            name="Série:",
            inline=False,
            value=user.discriminator
        )
        userembed.add_field(
            name="Usuário criado",
            inline=False,
            value=usercriou
        )
        userembed.add_field(
            name="Juntou-se ao servidor",
            inline=False,
            value=userentrou
        )

        await ctx.send(embed=userembed)
    except IndexError:
        await ctx.send("É necessário mencionar uma pessoa Ex: ( `!info @membro` )  ")
    except:
        await ctx.send("Desculpa, ERROR")
    finally:
        pass

@client.command(pass_context=True)
async def config(ctx):
    guild_local = ctx.message.guild
    verification_level = {
        discord.VerificationLevel.none: "Sem restrições (Não recomendado)",
        discord.VerificationLevel.low: "Baixo (Precisa ter um e-mail verificado na conta do Discord)",
        discord.VerificationLevel.medium: "Médio (Também precisa ter uma conta no Discord há mais de 5 minutos)",
        discord.VerificationLevel.high: "Alta (Também precisa ser membro deste servidor há mais de 10 minutos)",
        discord.VerificationLevel.table_flip: 'Mais Alta (Precisa ter um telefone verificado na conta do Discord)'
    }.get(guild_local.verification_level, '*Desconhecido*')

    with open('bloqueador_links.json', 'r') as f:
        bloqueador_links = json.load(f)

    with open('anti_spam.json', 'r') as f:
        anti_spam = json.load(f)


    if bloqueador_links[str(ctx.guild.id)] == 'True':
        var_antilink = '*Ligado*'
    else:
        var_antilink = '*Desligado*'
    if anti_spam[str(ctx.guild.id)] == 'True':
        var_antispam = '*Ligado*'
    else:
        var_antispam = '*Desligado*'

    with open('bloqueador_links.json', 'w') as f:
        json.dump(bloqueador_links, f, indent=4)

    embed = discord.Embed(color=0xffff00)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.add_field(name="\u200b",
                    value="**Nivel de Verificação:** " + verification_level + f"\n**AntiSpam:** {var_antispam}\n**AntiLink:** {var_antilink}\n**Membros:** *{guild_local.member_count}*\n**Bots Confiáveis:** [Consultar Bots Confiáveis](https://cdn.discordapp.com/attachments/742870320074981428/742924240214425691/bots_confiaveis.png)\n**Dicas:** [Ver Dicas](https://cdn.discordapp.com/attachments/660313898385145856/743174988722602135/recomendacoes.png)", inline=True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def scan(ctx):
    def pingable_roles(guild):
        mentionable_report = "```Scan Cargos mencionáveis```"
        for role in ctx.message.guild.roles:
            if role.mentionable:
                mentionable_report += f'**Atenção**: `{role.name}` é mencionável\n'
        return mentionable_report


    pingable_roles(ctx.message.guild)
    await ctx.send(pingable_roles(ctx.message.guild))
    pass

    guild = ctx.message.guild

    def split(s):
        half, rem = divmod(len(s), 2)
        return s[:half + rem], s[half + rem:]

    def role_permissions(guild):
        permission_report = "```Scan Permissões de Cargos```"
        for role in guild.roles:
            if role.permissions.administrator == True:
                permission_report += f"**Aviso Crítico:** `{role.name}`. Permissão `administrador` detectada.\n"
            else:
                if role.permissions.kick_members == True:
                    permission_report += f"**Atenção**: `{role.name}`. Permissão `expulsar membros` detectada.\n"
                    pass
                elif role.permissions.ban_members == True:
                    permission_report += f"**Atenção**: `{role.name}`. Permissão `banir membros` detectada.\n"
                    pass
                elif role.permissions.manage_channels == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar canais` detectada.\n"
                    pass
                elif role.permissions.manage_guild == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar servidor` detectada.\n"
                    pass
                elif role.permissions.view_audit_log == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `ver audit_log` detectada.\n"
                    pass
                elif role.permissions.manage_messages == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar mensagens` detectada.\n"
                    pass
                elif role.permissions.mention_everyone == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `mencionar everyone` detectada.\n"
                    pass
                elif role.permissions.mute_members == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `silenciar membros` detectada.\n"
                    pass
                elif role.permissions.deafen_members == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `surdar membros` detectada.\n"
                    pass
                elif role.permissions.move_members == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `mover membros` detectada.\n"
                    pass
                elif role.permissions.manage_nicknames == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar apelidos` detectada.\n"
                    pass
                elif role.permissions.manage_roles == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar cargos` detectada.\n"
                    pass
                elif role.permissions.manage_webhooks == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar webhooks` detectada.\n"
                    pass
                elif role.permissions.manage_emojis == True:
                    permission_report += f"**Atenção:** `{role.name}`. Permissão `gerenciar emojis` detectada.\n"
                    pass
        return permission_report

    permission_report = role_permissions(guild)
    permission_report2 = """"""
    permission_report3 = """"""
    permission_report4 = """"""
    permission_report5 = """"""
    permission_report6 = """"""
    permission_report7 = """"""
    rep_len = len(permission_report)
    if rep_len >= 2000:
        permission_report2, permission_report3 = split(permission_report)
        if len(permission_report2) >= 2000:
            perission_report4, permission_report5 = split(permission_report2)
            permission_report6, permission_report7 = split(permission_report3)
    if permission_report2 == """""":
        await ctx.send(permission_report)
        pass
    else:
        if permission_report4 == """""":
            await ctx.send(permission_report2)
            pass
            await ctx.send(permission_report3)
            pass
        else:
            await ctx.send(permission_report4)
            pass
            await ctx.send(permission_report5)
            pass
            await ctx.send(permission_report6)
            pass
            await ctx.send(permission_report7)
            pass

@client.command(pass_context=True)
async def limpar(ctx):
    verf = client.get_emoji(id=754710506631331972)
    errado = client.get_emoji(id=754710506559766530)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        await ctx.message.delete()
        embed = discord.Embed(title='', description='Quantas mensagens quer excluir ?', color=0xffff00)
        await ctx.send(embed=embed)

        def check(m):
            return m.author == user

        r00 = await client.wait_for('message', check=check)
        await ctx.channel.purge(limit=2)
        uu = ctx.message.author
        text = int(r00.content)
        if text >= 101:
            await ctx.send(f'{errado} O limite é de 100 mensagem')
        else:
            await ctx.channel.purge(limit=text)
            embed = discord.Embed(title='', description='{} {} mensagens foram excluidas por {}'.format(verf, text,
                                                                                                        uu.mention),
                                  color=0xffff00)
            await ctx.send(embed=embed)
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def mute(ctx):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    guild_local = ctx.message.guild
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            user = ctx.message.mentions[0]
            mutado = discord.utils.get(guild_local.roles, name='Mute[ALC]')
            loading = client.get_emoji(id=754710506652303480)
            msg = await ctx.send("{}".format(loading))

            mutado = discord.utils.get(guild_local.roles, name='Mute[ALC]')
            for guild_local_channel in guild_local.channels:
                channel = guild_local_channel
                overwrite = channel.overwrites_for(mutado)
                overwrite.send_messages = False
                await channel.set_permissions(mutado, overwrite=overwrite)

            await user.add_roles(mutado)
            embed000 = discord.Embed(title="",
                                     description="🤐 {} foi mutado no servidor".format(user.mention),
                                     color=0xffff00)
            user = ctx.message.author
            embed000.set_footer(text="Aplicação do {} - {}".format(user.name, date))
            await msg.edit(content=None, embed=embed000)
        except IndexError:
            await ctx.send("É necessário mencionar uma pessoa Ex: ( `!mute @membro` )  ")
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def unmute(ctx):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    guild_local = ctx.message.guild
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            user = ctx.message.mentions[0]
            loading = client.get_emoji(id=754710506652303480)
            msg = await ctx.send("{}".format(loading))
            mutado = discord.utils.get(guild_local.roles, name='Mute[ALC]')
            await user.remove_roles(mutado)
            embed000 = discord.Embed(title="",
                                     description="😁 {} foi desmutado do servidor".format(user.mention),
                                     color=0xffff00)
            user = ctx.message.author
            embed000.set_footer(text="Aplicação do {} - {}".format(user.name, date))
            await msg.edit(content=None, embed=embed000)
        except IndexError:
            await ctx.send("É necessário mencionar uma pessoa Ex: ( `!unmute @membro` )  ")
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando', color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def kick(ctx):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    certo = client.get_emoji(id=754710505855123466)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            mm = ctx.message.mentions[0]
            embed = discord.Embed(title="",
                                  description=f'{atencao} **Painel de Expulsão** {atencao}\n\n**Você realmente quer expulsar:**\n{mm.mention}\n\n**Verificação Valida Por:**\n*40 segundos*',
                                  color=0xffff00)
            embed.set_footer(text=f"Aplicação do {user.name}")
            msg = await ctx.send(embed=embed)
            for emoji in ('✅', '❌'):
                await msg.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

            reaction, user = await client.wait_for('reaction_add', check=check, timeout=40.0)

            if reaction.emoji == '✅':
                embed = discord.Embed(title="", description="{} {} foi expulso do servidor por {}".format(certo, mm.mention,
                                                                                                          user.mention),
                                      color=0xffff00)
                await msg.edit(embed=embed)
                await ctx.message.guild.kick(discord.Object(id=mm.id))
            elif reaction.emoji == '❌':
                embed = discord.Embed(title="", description="{} Expulsão {} foi cancelado".format(errado, mm.mention),
                                      color=0xffff00)
                await msg.edit(embed=embed)
            else:
                await ctx.send("Emoji invalido")
        except IndexError:
            await ctx.send("É necessário mencionar uma pessoa Ex: ( `!kick @membro` )  ")
        except asyncio.TimeoutError:
            mm = ctx.message.mentions[0]
            await ctx.send(f"Validação de expulsão do {mm.mention} por {user.mention} encerrada")
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def ban(ctx):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    certo = client.get_emoji(id=754710505855123466)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        try:
            mm = ctx.message.mentions[0]
            embed = discord.Embed(title="",
                                  description=f'{atencao} **Painel de Banimento** {atencao}\n\n**Você realmente quer banir:**\n{mm.mention}\n\n**Verificação Valida Por:**\n*40 segundos*',
                                  color=0xffff00)
            embed.set_footer(text=f"Aplicação do {user.name}")
            msg = await ctx.send(embed=embed)
            for emoji in ('✅', '❌'):
                await msg.add_reaction(emoji)

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

            reaction, user = await client.wait_for('reaction_add', check=check, timeout=40.0)

            if reaction.emoji == '✅':
                embed = discord.Embed(title="", description="{} {} foi banido do servidor por {}".format(certo, mm.mention,
                                                                                                         user.mention),
                                      color=0xffff00)
                await msg.edit(embed=embed)
                await ctx.message.guild.ban(discord.Object(id=mm.id))
            elif reaction.emoji == '❌':
                embed = discord.Embed(title="", description="{} Banimento {} foi cancelado".format(errado, mm.mention),
                                      color=0xffff00)
                await msg.edit(embed=embed)
            else:
                await ctx.send("Emoji invalido")
        except IndexError:
            await ctx.send("É necessário mencionar uma pessoa Ex: ( `!ban @membro` )  ")
        except asyncio.TimeoutError:
            mm = ctx.message.mentions[0]
            await ctx.send(f"Validação de banimento do {mm.mention} por {user.mention} encerrada")
        except:
            await ctx.send("COMANDO ERROR ")
        finally:
            pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command()
async def unban(ctx, *, member=None):
    atencao = client.get_emoji(id=754710505821831228)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        if not member:
            await ctx.send("É necessário inserir uma pessoa Ex: ( `!unban Membros#1368` )  ")
        else:
            atencao = client.get_emoji(id=754710505821831228)
            certo = client.get_emoji(id=754710505855123466)
            errado = client.get_emoji(id=754710506559766530)
            user = ctx.message.author
            try:
                banned_users = await ctx.guild.bans()
                member_name, member_discriminator = member.split('#')

                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        user2 = ctx.message.author
                        await ctx.guild.unban(user)
                        await ctx.send(f'{certo} {user.mention} foi desbanido por {user2.mention}')
                        return
            except IndexError:
                await ctx.send("É necessário inserir uma pessoa Ex: ( `!unban MembroTeste#0001` )  ")
            except:
                await ctx.send("COMANDO ERROR ")
            finally:
                pass
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def bloquear(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        manutencao = client.get_emoji(id=754710505867706409)
        loading = client.get_emoji(id=754710506652303480)
        errado = client.get_emoji(id=754710506559766530)
        user = ctx.message.author
        guild_local = ctx.message.guild
        msg = await ctx.send("{}".format(loading))
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed000 = discord.Embed(title="{}".format(client.user.name),
                                 description="{} *Esse chat foi* __***bloqueado***__".format(manutencao),
                                 color=0xffff00)
        embed000.set_footer(text="Aplicação do {} - {}".format(user.name, date))
        embed000.set_thumbnail(url=client.user.avatar_url)
        await msg.edit(content=None, embed=embed000)
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def liberar(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        verf = client.get_emoji(id=754710506631331972)
        loading = client.get_emoji(id=754710506652303480)
        errado = client.get_emoji(id=754710506559766530)
        user = ctx.message.author
        guild_local = ctx.message.guild
        role = "ModSecurity[ALC]"
        role = discord.utils.get(user.guild.roles, name=role)
        msg = await ctx.send("{}".format(loading))
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed000 = discord.Embed(title="{}".format(client.user.name),
                                 description="{} *Esse chat foi* __***liberado***__".format(verf),
                                 color=0xffff00)
        embed000.set_footer(text="Aplicação do {} - {}".format(user.name, date))
        embed000.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/742870320074981428/742904580807065720/open.png")
        await msg.edit(content=None, embed=embed000)
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def btodos(ctx):
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        manutencao = client.get_emoji(id=754710505867706409)
        loading = client.get_emoji(id=754710506652303480)
        errado = client.get_emoji(id=754710506559766530)
        user = ctx.message.author
        guild_local = ctx.message.guild
        role = "ModSecurity[ALC]"
        role = discord.utils.get(user.guild.roles, name=role)
        await ctx.message.delete()
        msg = await ctx.send("{}".format(loading))
        for gg in client.guilds:
            if gg == guild_local:
                for guild_local_channel in guild_local.channels:
                    channel = guild_local_channel
                    overwrite = channel.overwrites_for(ctx.guild.default_role)
                    overwrite.send_messages = False
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                embed000 = discord.Embed(title="{}".format(client.user.name),
                                         description="{} *Todos os chats foram* __***bloqueados***__".format(
                                             manutencao), color=0xffff00)
                embed000.set_footer(text="Aplicação do {} - {}".format(user.name, date))
                embed000.set_thumbnail(url=client.user.avatar_url)
                await msg.edit(content=None, embed=embed000)
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def ltodos(ctx):
    verf = client.get_emoji(id=754710506631331972)
    loading = client.get_emoji(id=754710506652303480)
    errado = client.get_emoji(id=754710506559766530)
    user = ctx.message.author
    role = "ModSecurity[ALC]"
    role = discord.utils.get(user.guild.roles, name=role)
    if role in user.roles:
        user = ctx.message.author
        role = "ModSecurity[ALC]"
        role = discord.utils.get(user.guild.roles, name=role)
        await ctx.message.delete()
        msg = await ctx.send("{}".format(loading))
        guild_local = ctx.message.guild
        for gg in client.guilds:
            if gg == guild_local:
                for guild_local_channel in guild_local.channels:
                    channel = guild_local_channel
                    overwrite = channel.overwrites_for(ctx.guild.default_role)
                    overwrite.send_messages = True
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                embed000 = discord.Embed(title="{}".format(client.user.name),
                                         description="{} *Todos os chats foram* __***liberados***__".format(verf),
                                         color=0xffff00)
                embed000.set_footer(text="Aplicação do {} - {}".format(user.name, date))
                embed000.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/742870320074981428/742904580807065720/open.png")
                await msg.edit(content=None, embed=embed000)
    else:
        errado = client.get_emoji(id=754710506559766530)
        embed = discord.Embed(title='', description=f'{errado} Você não tem permissão para utilizar este comando',
                              color=0xffff00)
        embed.set_footer(text='Para utilizar os comandos adicione o cargo @ModSecurity[ALC]')
        await ctx.send(embed=embed)

@canal_log.error
async def canal_log_error(ctx, error):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("É necessário inserir ID de um canal Ex: ( `!canal_log 743914824454373417` )  ")

@canal_report.error
async def canal_report_error(ctx, error):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("É necessário inserir ID de um canal Ex: ( `!canal_report 743914824454373417` )  ")

@prefix.error
async def prefix_error(ctx, error):
    atencao = client.get_emoji(id=754710505821831228)
    errado = client.get_emoji(id=754710506559766530)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("É necessário inserir um prefixo Ex: ( `!prefix $` )  ")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

client.run(TOKEN)
