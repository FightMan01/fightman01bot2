import datetime, time
import calendar as cal
import logging
import json
from discord import Game
import aiohttp
import requests
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
global last_played
last_played = ""
client = commands.Bot(command_prefix='?!')
Client = discord.Client()
vc_clients = {}
players = {}
client.remove_command('help')
from discord.voice_client import VoiceClient
import asyncio
import youtube_dl
global chat_filter
global bypass_list
chat_filter = ["a"]
bypass_list = []
global playing
playing = "Most nem megy semmi :("
queues = {}
#                                                                                             A bot készült: 2018.09.19.
def check_queue(id):
    if queues[id] != []:
        players = queues[id].pop(0)
        players[id] = players
        players.start()

@client.event
async def on_ready():
    print ("A bot keszen all!")
    print ("Nev: " + client.user.name)
    print ("ID: " + client.user.id)
    counter = 0
    while not counter > 0:
        statuses = ["{} szerver | ?!help".format(str(len(client.servers))) , "{} szerver | ?!dc".format(str(len(client.servers))), "{} szerver | ?!zenehelp".format(str(len(client.servers))), "{} szerver | ?!tudnivalók".format(str(len(client.servers)))]
       # await client.change_presence(game=discord.Game(name="{} szerver | ?!help".format(str(len(client.servers)))))
        await client.change_presence(game=discord.Game(name=random.choice(statuses)))
        await asyncio.sleep(15)
        

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id='414422696802385923')
    while not counter > 15:
        counter += 1
        await client.send_message(channel, counter)
        await asyncio.sleep(1) 
        

async def wc():
    await client.wait_until_ready()
    channel = discord.Object(id='414407064014553100')
    await client.send_message(channel, "@everyone A FightMan01bot készen áll a használatra! :thumbsup:")
    await client.send_message(channel, "Parancsokért írd be, hogy ?!parancsok")
    await client.send_message(channel, "Szép napot! :sun_with_face: ")

@client.command(pass_context=True)
async def link(ctx):
    await client.say("Ha szeretnéd a botomat behívni a szerveredre, akkor itt egy link hozzá: \nhttps://discordapp.com/api/oauth2/authorize?client_id=492023626527277077&permissions=8&scope=bot \nParancsokért: **?!help** \n:thumbsup:")

@client.command(aliases=['user-info', 'ui'], pass_context=True, invoke_without_command=True)
async def info(ctx, user: discord.Member):
    '''Használat: ?!info [említés]'''
    if not message.author.bot:
        try:
            embed = discord.Embed(title="Információk a következőről: {}".format(user.name), description="Ezeket találtam:", color=0x00ff00)
            embed.add_field(name="Neve", value=user.name, inline=True)
            embed.add_field(name='Beceneve', value=user.nick, inline=True)
            embed.add_field(name="ID-ja", value=user.id, inline=True)
            embed.add_field(name="Állapota", value=user.status, inline=True)
            embed.add_field(name='Játékban', value=user.game, inline=True)
            embed.add_field(name="Legmagasabb rangja", value=user.top_role)
            #embed.add_field(name="Csatlakozott", value=user.joined_at)
            embed.add_field(name='Csatlakozott', value=user.joined_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'))
            embed.set_author(name=user, icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text="FightMan01 bot 6.3")
            await client.say(embed=embed)
        except:
            await client.say("Hoppá! Valószínűleg nem említetted meg a felhasználót! :x:\nHelyes használat: ?!info [említés]")
    else:
        return False

@info.error
async def info_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg nem említetted meg a felhasználót! :x:\nHelyes használat: ?!info [említés]")

@client.command(aliases=['kirúgás'], pass_context=True, no_pm=True)
async def kick(ctx, user: discord.Member, * ,reason : str = None):
    if not message.author.bot:
        if ctx.message.author.server_permissions.administrator:
            '''Használat: ?!kick [említés] [indok]'''
            if reason == "None":
                reason = "(Nem csatoltak üzenetet ehhez a figyelmeztetéshez!)"
            await client.send_message(user, "Kickelve lettél a **{}** szerverről a következő indokkal: **".format(ctx.message.server.name) + reason + "**")
            await client.say(":boot: Csá, {}. Ki lettél kickelve :D".format(user.name))
            await client.kick(user)
            if ctx.message.server.name == "#FightMan01":
                channel = discord.Object(id="522489336197808133")
                embed = discord.Embed(title="Kirúgás", description="Részletek: ", color=0x00ffed)
                embed.add_field(name="Moderátor", value=ctx.message.author.mention, inline=True)
                embed.add_field(name="Kirúgott", value=user.mention, inline=True)
                embed.add_field(name="Oka", value=reason, inline=True)
                await client.send_message(channel, embed=embed)
            if ctx.message.server.name == "HunTrans Kft.":
                channel2 = discord.Object(id="493754977181892609")
                embed2 = discord.Embed(title="Kirúgás", description="Részletek: ", color=0x00ffed)
                embed2.add_field(name="Moderátor", value=ctx.message.author.mention, inline=True)
                embed2.add_field(name="Kirúgott", value=user.mention, inline=True)
                embed2.add_field(name="Oka", value=reason, inline=True)
                await client.send_message(channel2, embed=embed2) 
            if ctx.message.server.name == "Bot Support Szerver (HU)":
                channel3 = discord.Object(id="527173456496689183")
                embed3 = discord.Embed(title="Kirúgás", description="Részletek: ", color=0x00ffed)
                embed3.add_field(name="Moderátor", value=ctx.message.author.mention, inline=True)
                embed3.add_field(name="Kirúgott", value=user.mention, inline=True)
                embed3.add_field(name="Oka", value=reason, inline=True)
                await client.send_message(channel3, embed=embed3)   
        else:
            await client.say("Ezt csak Adminisztrátor joggal lehet használni! :x:")
    else:
        return False

@kick.error
async def kick_error(error, ctx): 
    await client.say("Oopss! Valami hiányzik! :x:\nHelyes használat: ?!kick [említés] [indok]")

@client.command(pass_context=True)
async def kecske(ctx, user: discord.Member):
    await client.say("Kedves {} ! Kérsz egy kis kecske sajtot?".format(user.name))
    
@client.command(pass_context=True)
async def kristály(ctx):
    await client.say("NE emlegesd ezt a nevet!!! SOHAAA!")

@client.command(pass_context=True)
async def dolycs(ctx):
    await client.say("Dolycsestundé jáh!")
    
@client.command(pass_context=True)
async def szaktanári(ctx, user: discord.Member):
    '''Használat: ?!szaktanári [említés]'''
    await client.say("Üzenet {}-nak/nek Dálymond Erikától: 'SZAKTANÁRÍÍÍÍÍ!!!' ".format(user.name))

@client.command(pass_context=True)
async def sláfen(ctx):
    await client.say("Mingyá' kapsz egy sláfent a krákenvágenedbe!!")

@client.command(pass_context=True)
async def meghívó(ctx):
    await client.say("Anyád a meghívó CSÍRA :D")

@client.command(pass_context=True)
async def ELKÁBÍTÓISTENNYILA(ctx):
    await client.say("Yeahhhh boiiiiii! BOIIIIIIIII")

@client.command(pass_context=True)
async def szponzoráció(ctx):
    await client.say("Ssssss! :D Rejtett szponzoráció jön: https://www.sourceforge.net/p/speedeula Ne szólj róla senkinek!!!")

@client.command(pass_context=True)
async def parancsok278444325(ctx):
    await client.say(":x:-----------------------------------------------------------------------------------------------------------------:x:")
    await client.say("Figyelem! A discord nem tudja az összes üzenetet egyszerre feldolgozni! Kérlek várj míg meg nem jelenik a vége felirat!")
    await client.say("Parancsok: ")
    await client.say("?!meghívó")
    await client.say("?!sláfen")
    await client.say("?!kristály")
    await client.say("?!dolycs")
    await client.say("?!szaktanári [említés]")
    await client.say("?!kecske [említés]")
    await client.say("?!info [említés]")
    await client.say("?!ping")
    await client.say("?!ELKÁBÍTÓISTENNYILA")
    await client.say("?!szponzoráció")
    await client.say("?!parancsok")
    await client.say("?!dc")
    await client.say("?!szerverinfo")
    await client.say("Hogy megtudd mit csinálnak a parancsok írd be :D")
    await client.say("Állandó prefix: ?!")
    await client.say("Készítő: FightMan01")
    await client.say("Parancslista vége!")
    await client.say(":x:-----------------------------------------------------------------------------------------------------------------:x:")
    
@client.command(aliases=['discord'], pass_context=True)
async def dc(ctx):
    if not message.author.bot:
        await client.say("Discord szerverem: https://discord.gg/VUw6DkZ Csatlakozz be!!")
    else:
        return False

@client.command(pass_context=True)
async def embed(ctx):
    embed = discord.Embed(title="FightMan01 client", description="Készítő: FightMan01", color=0x00ff00)
    embed.set_author(name="FightMan01")
    await client.say(embed=embed)

@client.command(aliases=['server', 'sinfo', 'si', 'serverinfo'], pass_context=True)
async def szerverinfo(ctx):
    if not message.author.bot:
        online = 0
        for i in ctx.message.server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        role_count = len(ctx.message.server.roles)
        emoji_count = len(ctx.message.server.emojis)
        embed = discord.Embed(title="Információk a következő szerverről: {}".format(ctx.message.server.name), description="Ezeket találtam:", color=0x00ff00)
        embed.add_field(name="Név: ", value=ctx.message.server.name, inline=True)
        embed.add_field(name="ID: ", value=ctx.message.server.id, inline=True)
        embed.add_field(name="Rangok: ", value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name="Tagok: ", value=len(ctx.message.server.members))
        embed.add_field(name='Jelenleg elérhető', value=online)
        embed.add_field(name="Szerver létrehozási dátuma: ", value=ctx.message.server.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'), inline=True)
        embed.add_field(name="Szoba létrehozási dátuma: ",value=ctx.message.channel.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'), inline=True)
        embed.add_field(name="Jelenlegi szoba: ",value=ctx.message.channel, inline=True)
        embed.add_field(name="Szerver tulajdonosa: ",value=ctx.message.server.owner.mention, inline=True)
        embed.add_field(name="Szerver tulajdonosának az állapota: ",value=ctx.message.server.owner.status, inline=True)
        embed.add_field(name="Szerver régiója: ",value=ctx.message.server.region, inline=True)
        embed.add_field(name='Ellenőrzési szint', value=str(ctx.message.server.verification_level))
        embed.add_field(name='Emoteok száma', value=str(emoji_count))
        embed.add_field(name='Szerver legmagasabb rangja', value=ctx.message.server.role_hierarchy[0])
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.set_author(name=ctx.message.server.name, icon_url=ctx.message.server.icon_url)
        embed.set_footer(text="FightMan01 bot 6.3")
        await client.say(embed=embed)
    else:
        return False

#@client.command(pass_context=True)
#async def parancsok12345678(ctx):
   # await client.say(".")
    #channel = ctx.message.channel
   # messages = []
  #  async for message in client.logs_from(channel, 2):
 #       messages.append(message)
#    await client.delete_messages(messages)
    #embed = discord.Embed(title="Parancslista", description="FightMan01 bot v6.3 ", color=0x00ff00)
   # embed.add_field(name="?!meghívó",value=".", inline=False)
  #  embed.add_field(name="?!sláfen", value=".", inline=False)
 #   embed.add_field(name="?!kristály",value=".", inline=False)
#    embed.add_field(name="?!dolycs",value=".", inline=False)
    #embed.add_field(name="?!szaktanári [említés]",value=".", inline=False)
   # embed.add_field(name="?!kecske [említés]",value=".", inline=False)
  #  embed.add_field(name="?!info [említés]",value=".", inline=False)
 #   embed.add_field(name="?!ping", value=".", inline=False)
#    embed.add_field(name="?!ELKÁBÍTÓISTENNYILA", value=".", inline=False)
    #embed.add_field(name="?!szponzoráció", value=".", inline=False)
   # embed.add_field(name="?!parancsok", value=".", inline=False)
  #  embed.add_field(name="?!dc", value=".", inline=False)
  #  embed.add_field(name="?!szerverinfo", value=".", inline=False)
  #  embed.add_field(name="?!tess", value=".", inline=False)
    #embed.add_field(name="?!zene", value=".", inline=False)
  #  embed.add_field(name="?!zenehelp",value=".", inline=False)
  #  embed.add_field(name="?!törlés [szám 1 és 300 között]",value=".", inline=False)
   # embed.add_field(name="?!üdv [említés]",value=".", inline=False)
   # embed.add_field(name="?!mute [említés]",value="Csak admin funkció!", inline=False)
  #  embed.add_field(name="?!unmute [említés]",value="Csak admin funkció!", inline=False)
  #  embed.add_field(name="Hogy megtudd mit csinálnak a parancsok, írd be :D", value=".")
  #  embed.add_field(name="Állandó prefix: ?!", value=".", inline=False)
  #  embed.add_field(name="Készítő: FightMan01", value=".", inline=False)
    #embed.add_field(name="Parancslista vége!", value=".", inline=False)
  #  embed.add_field(name="Discord szerverem: https://discord.gg/VUw6DkZ",value=".", inline=False)  
   # embed.set_thumbnail(url=ctx.message.author.avatar_url)
    #await client.send_message(ctx.message.author, embed=embed)
   # await client.say(":white_check_mark: {} küldtem neked privátot :thumbsup:".format(ctx.message.author.mention))

#@client.command(pass_context=True)
#async def parancsok(ctx):
    #await client.send_message(ctx.message.author, "Üdv kedves érdeklődő! Köszi, hogy érdeklődtél a botom iránt! Alább találod botom parancsait: \n *?!mute [említés]* \n *?!unmute [említés]* \n *?!kick [említés] [indok]* \n *?!ping* \n *?!dc* \n *?!parancsok* - Megnyitja ezt a listát \n *?!help* - Megnyitja ezt a listát \n *?!szerverinfo* \n *?!matek* \n *?!info [említés]* \n *?!üdv [említés]* \n *?!újdonságok* \n *?!tudnivalók* \n *?!segítség [szöveg]* \n *?!warn [említés]* \n *?!ban [említés] [nap] [indok]* \n A bot zenei parancsaiért kérlek írd be, hogy **?!zenehelp** \n Botom állandó prefixe: **?!** \n Hivatalos support szerver: https://discord.gg/VUw6DkZ \n Egyes parancsokat csak ***Adminisztrátor*** joggal lehet használni! \n Köszönöm mégegyszer is, hogy érdeklődtél a botom iránt! \n Szép napot! :sun_with_face: ")
    #await client.say(":white_check_mark: {} küldtem neked privátot :thumbsup:".format(ctx.message.author.mention))

@client.command(aliases=['parancsok', 'commands'], pass_context=True)
async def help(ctx):
    if not message.author.bot:
        await client.send_message(ctx.message.author, "Üdv kedves érdeklődő! Köszi, hogy érdeklődtél a botom iránt! Alább találod botom parancsait kategóriákba sorolva: " 
        "\n"
        "\n :information_source: __**Általános**__ :information_source: "
        "\n"
        "\n *?!ping* - **Megmutatja a kliens pingedet!**"
        "\n *?!dc* **Küld egy meghívót a hivatalos support szerverre!**"
        "\n *?!help* - **Megnyitja ezt a listát!** "
        "\n *?!szerverinfo* - **Megmutatja az adott szerver információit!**"
        "\n *?!matek* - **Megmutatja a bot matematikai képességeit!**"
        "\n *?!info [említés]* - **Megmutatja az adott ember információit!**"
        "\n *?!újdonságok* - **Megmutatja a bot újdonságait!**"
        "\n *?!tudnivalók* - **Kiír pár tudnivalót a botról!**"
        "\n *?!kérdés [kérdés]* - **A bot válaszol a kérdésedre! (Csak eldöntendő kérdésre tud válaszolni!)**"
        "\n *?!zenehelp* - **Kilistázza a bot zenei parancsait!**"
        "\n *?!link* - **Kiír egy linket, mellyel a botot tudod behívni a szerveredre!**" 
        "\n"
        "\n :tools: __**Moderáció**__ :tools:"
        "\n"
        "\n *?!mute [említés]* - **Némít egy adott felhasználót! (Adminisztrátor jog szükséges!)**"
        "\n *?!unmute [említés]* - **Feloldja a felhasználó némítását! (Adminisztrátor jog szükséges!)**"
        "\n *?!kick [említés] [indok]* - **Kickeli a felhasználót az adott szerverről! (Adminisztrátor jog szükséges)!**"
        "\n *?!warn [említés]* - **Figyelmezteti privát üzenetben az adott embert! (Adminisztrátor jog szükséges)**"
        "\n *?!ban [említés] [nap] [indok]* - **Kitiltja az adott embert a megadott időtartamra az adott szerverről! (Adminisztrátor jog szükséges!)**"
        "\n"
        "\n :mailbox_with_mail: __**Tudnvalók**__ :mailbox_with_mail: "
        "\n"
        "\n Botom állandó prefixe: **?!** \n Hivatalos support szerver: https://discord.gg/VUw6DkZ "
        "\n Köszönöm mégegyszer is, hogy érdeklődtél a botom iránt! "
        "\n Szép napot! :sun_with_face: "
        "\n"
        "\n UI.: Támogasd a botom fejlesztését! Ha összegyűlik megfelelő mennyiségű pénz, akkor a bot 0-24-ben tud futni! "
        "\n https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=S4AB6KJJ3ESU6&source=url")


        await client.say(":white_check_mark: {} küldtem neked privátot :thumbsup:".format(ctx.message.author.mention))
    else:
        return False

@client.command(pass_context = True, aliases=['zhelp', 'zeneh'])
async def zenehelp(ctx):
    if not message.author.bot:
        await client.send_message(ctx.message.author, "Üdv! Látom a botom zenei parancsai után érdeklődsz! Alább találod meg őket: "
        "\n"
        "\n :musical_note: __**Zenei parancsok**__ :musical_note:"
        "\n"
        "\n *?!play [zene]* - **Lejátssza az adott zenét!**"
        "\n *?!folytatás* - **Folytatja a zenét!**"
        "\n *?!szünet* - **Szünetelteti a zenét!**"
        "\n *?!stop* - **Megállítja a zenét!**"
        "\n *?!skip* - **Átugorja a zenét! (Ez csak a ?!playlist1 illetve ?!bassboost listáknál működik)**"
        "\n *?!most* - **Megmutatja a most játszódó zenét!**"
        "\n *?!újrakezdés* - **Újrakezdi az adott zenét! (Csak az ?!play parancs után működik!)**"
        "\n *?!lecsatl* - **Lecsatlakoztatja a botot!**"
        "\n *?!kérés [zene]* - **Zenét lehet kérni a ?!playlist1 listába!**"
        "\n"
        "\n :musical_note: __**Lejátszási listák**__ :musical_note: "
        "\n"
        "\n *?!best2017* - **2017 legjobb zenéi! Összesen 25 zenét tartalmaz!**"
        "\n *?!best2018* - **2018 legjobb zenéi! Összesen 25 zenét tartalmaz!**"
        "\n *?!best2019* - **2019 legjobb zenéi! Összesen 25 zenét tartalmaz!**"
        "\n *?!bassboost* - **Elindít 3 darab bass boosted zenét!**"
        "\n *?!uktop40* - **Anglia top 40-es listája! Összesen 40 darab zenét tartalmaz!**"
        "\n *?!summerhits2018* - **2018 nyarának legforróbb slágerei! Összesen 25 zenét tartalmaz!**"
        "\n *?!radio1top50* - **Rádió1 top 50-es listája! Összesen 50 zenét tartalmaz!**"
        "\n *?!ncsgaming* - **Elindít egy 2 órás NCS gaming lejátszási listát!**"
        "\n *?!playlist1* - **Egy, általatok összeálított lista!**"
        "\n"
        "\n"
        "\n :radio: __**Rádiók**__ :radio:"
        "\n"
        "\n *?!radio1* - **Rádió1 élő adás indítása!**"
        "\n *?!musicfm* - **MusicFM élő adás indítása!**"
        "\n *?!retro* - **Retró rádió élő adás indítása!**"
        "\n *?!petofi* - **Petőfi rádió élő adás indítása!**"
        "\n"
        "\n A bot az egyes parancsok után automatikusan becsatlakozik a csatornába, a végén pedig elhagyja azt!"
        "\n Szép napot :sun_with_face:")

        await client.say(":white_check_mark: {} küldtem neked privátot :thumbsup:".format(ctx.message.author.mention))
    else:
        return False

@client.command(pass_context=True, aliases=['join', 'belépés', 'csatlakozás'])
async def csatl(ctx):
    if not message.author.bot:
        await client.say("A bot a zene indításakor automatikusan becsatlakozik, a végén pedig ki!")
   # channel = ctx.message.author.voice.voice_channel
   # await client.join_voice_channel(channel)
    else:
       return False

@client.command(aliases=['kilépés', 'fuckoff', 'kurva'], pass_context=True)
async def lecsatl(ctx):
    if not message.author.bot:
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("Lecsatlakozva! :thumbsup:")
        except:
            await client.say("Nem vagyok hangcsatornában :x:")
    else:
        return False
@client.command(aliases=['p', 'start', 'zene'], pass_context=True)
async def play(ctx, * ,url, ytdl_options=None, **kwarg):

    '''Használat: ?!play [url]'''
    if not message.author.bot:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        if voice_client == None:
            await client.say("Kérlek várj! :musical_note:")
            try:
                channel = ctx.message.author.voice.voice_channel
                await client.join_voice_channel(channel)
            except:
                return False
            try:
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp4',
                        'preferredquality': '192',
                    }],
                }
                player = await voice_client.create_ytdl_player("ytsearch: {}".format(url), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                player.start()
                players[server.id] = player 
                player.volume = 0.2
                global playing 
                playing = "Most megy: **{}**".format(player.title)
                global last_played
                last_played = player.url
                embed = discord.Embed(title="Zenelejátszó", description="Zene információi: ", color=0x00ff00)
                embed.add_field(name="Zene címe",value=player.title, inline=True)
                embed.add_field(name="Zene feltöltési dátuma",value=player.upload_date, inline=True)
                embed.add_field(name="Zene feltöltője",value=player.uploader, inline=True)
                embed.add_field(name="A zenét kérte",value=ctx.message.author,inline=True)
                embed.set_footer(text="FightMan01 bot 6.3")
                await client.say(embed=embed)
            
            except:
                print(Exception)
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            while not player.is_done():
                await asyncio.sleep(1) 
            try:
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                await voice_client.disconnect()
                await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
            except:
                return False
        else:
             await client.say("Hmm...Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")
    else:
        return False
@play.error
async def play_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg elfelejtettél zenét beírni! :x:\nHelyes használat: ?!play [zene]")

@client.command(aliases=['rádió1', 'rádió'], pass_context=True)
async def radio1(ctx):
    if not message.author.bot:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        if voice_client == None:
            await client.say("Kérlek várj! :musical_note: ")
            try:
                channel = ctx.message.author.voice.voice_channel
                await client.join_voice_channel(channel)
            except:
                await client.say("Már megy a zene! :thumbsup:")
            try:
                url = "http://213.181.210.106:80/high.mp3"
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                player = await voice_client.create_stream_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                player.volume = 0.2
                players[server.id] = player  
                player.start()
                global playing 
                playing = "Most megy: **Rádió1 élő adás**"
                await client.say("Azonnal indul! :thumbsup:")
            except:
                await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            while not player.is_done():
                await asyncio.sleep(1)
            try:
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                await voice_client.disconnect()
                await client.say("Az élő adást megállították! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
            except:
                return False
        else:
            await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")
    else:
        return False
@client.command(aliases=['pause'], pass_context=True)
async def szünet(ctx):
    if not message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].pause()
            await client.say("A zene szünetel! :thumbsup:")
        except:
            await client.say("A zene már szünetel! :x:")
    else:
        return False
@client.command(aliases=['resume'], pass_context=True)
async def folytatás(ctx):
    if not message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].resume()
            await client.say("A zene folytatódik! :thumbsup:")
        except:
            await client.say("A zene már megy! :x:")
    else:
        return False
@client.command(aliases=['megállít'], pass_context=True)
async def stop(ctx):
    if not message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].stop()
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene megállt! :white_check_mark:")
        except:
            await client.say("A zene már áll! :x:")
    else:
        return False
@client.command(aliases=['átugrás'], pass_context=True)
async def skip(ctx):
    if not message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].stop()
        except:
            return False
    else:
        return False

@client.command(aliases=['restart'], pass_context=True)
async def újrakezdés(ctx):
    '''Használat: ?!play [url]'''
    if not message.author.bot:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)

        if voice_client == None:
            try:
                channel = ctx.message.author.voice.voice_channel
                await client.join_voice_channel(channel)
            except:
                return False
            await client.say("Kérlek várj! :musical_note:")
            try:
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                global last_played
                url = last_played
                player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                players[server.id] = player  
                player.start()
                player.volume = 0.2
                global playing 
                playing = "Most megy: **{}**".format(url)
                await client.say("Azonnal indul! :thumbsup:")
            except:
                await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            while not player.is_done():
                await asyncio.sleep(1)
            try:
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                await voice_client.disconnect()
                await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
            except:
                return False
        else:
            await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

#@client.command(aliases=['zhelp', 'zeneh'], pass_context=True)
#async def zenehelp(ctx):
   # await client.say(":white_check_mark: {} küldtem neked privátot! :thumbsup: ".format(ctx.message.author.mention))
   # embed = discord.Embed(title="Zenelejátszó", description="FightMan01 bot zenei parancsai: ", color=0x00ffed)
   # embed.add_field(name="?!csatl",value="Ezt a parancsot ***NEM*** kell használni!!!", inline=False)
   # embed.add_field(name="?!play [zene url-je]",value="Fontos, hogy ide URL címet írjál!", inline=False)
   # embed.add_field(name="?!best2017",value="2017 legjobb zenéi! Összesen **25** zenét tartalmaz!", inline=False)
    #embed.add_field(name="?!best2018",value="2018 legjobb zenéi! Összesen **25** zenét tartalmaz!", inline=False)
  #  embed.add_field(name="?!best2019",value="2019 legjobb zenéi! Összesen **25** zenét tartalmaz!", inline=False)
    #embed.add_field(name="?!bassboost",value="Elindít **3** darab bass boosted zenét!", inline=False)
   # embed.add_field(name="?!uktop40",value="Anglia **top 40-es** listája! Összesen **40** darab zenét tartalmaz!", inline=False)
  # embed.add_field(name="?!summerhits2018",value="2018 nyarának **legforróbb** slágerei! Összesen **25** zenét tartalmaz!", inline=False)
  #  embed.add_field(name="?!radio1top50",value="Rádió1 **top 50-es** listája! Összesen **50** zenét tartalmaz!", inline=False)
  #  KÉSZ EDDIG embed.add_field(name="?!ncsgaming",value="Elindít egy **2 órás** NCS gaming lejátszási listát!", inline=False)
   # embed.add_field(name="?!szünet",value="Ezzel tudod szüneteltetni a zenét!", inline=False)
   # embed.add_field(name="?!folytatás",value="Ezzel tudod folytatni a zenét!", inline=False)
    #embed.add_field(name="?!stop",value="Ezzel tudod megállítani a zenét!", inline=False)
   # embed.add_field(name="?!skip",value="Ezzel zenét lehet ugrani a **?!playlist1** illetve a **?!bassboost** playlistekben!", inline=False)
   # embed.add_field(name="?!most",value="Kiírja a most játszódó zenét!", inline=False)
  #  embed.add_field(name="?!újrakezdés",value="Ezzel újra tudod kezdeni a zenét! FIGYELEM! Csak a ?!play [url] parancs után megy!", inline=False)
   # embed.add_field(name="?!radio1",value="Rádió 1 élő adás indítása!", inline=False)
    #embed.add_field(name="?!lecsatl",value="Ezzel tudod lecsatlakoztatni a botot!", inline=False)
   # embed.add_field(name="?!kérés [zene címe]",value="Zenét lehet kéni egy playlistbe!", inline=False)
   # embed.set_footer(text="FightMan01 bot 6.3")
    #await client.send_message(ctx.message.author, embed=embed)

@client.command(aliases=['purge', 'töröl', 'delete'], pass_context=True)
async def törlés(ctx, amount=301):
    '''Használat: ?!törlés [szám 1 és 300 között]'''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '416226732966936577':
        try:
            channel = ctx.message.channel
            messages = []
            async for message in client.logs_from(channel, limit=int(amount) + 1):
                messages.append(message)
            await client.delete_messages(messages)
            if ctx.message.server.name == "#FightMan01":
                channel = discord.Object(id="522489336197808133")
                embed = discord.Embed(title="Törlés", description="Részletek: ", color=0x00ffed)
                embed.add_field(name="Törlő", value=ctx.message.author.mention, inline=True)
                embed.add_field(name="Csatorna", value=ctx.message.channel.mention, inline=True)
                embed.add_field(name="Törölt üzenetek száma", value=int(amount), inline=True)
                await client.send_message(channel, embed=embed)   
            if ctx.message.server.name == "HunTrans Kft.":
                channel2 = discord.Object(id="493754977181892609")
                embed2 = discord.Embed(title="Törlés", description="Részletek: ", color=0x00ffed)
                embed2.add_field(name="Törlő", value=ctx.message.author.mention, inline=True)
                embed2.add_field(name="Csatorna", value=ctx.message.channel.mention, inline=True)
                embed2.add_field(name="Törölt üzenetek száma", value=int(amount), inline=True)
                await client.send_message(channel2, embed=embed2)   
            await client.say("Üzenetek törölve! :white_check_mark: ")  
            if ctx.message.server.name == "Bot Support Szerver (HU)":
                channel3 = discord.Object(id="527173403468103710")
                embed3 =  discord.Embed(title="Törlés", description="Részletek: ", color=0x00ffed)
                embed3.add_field(name="Törlő", value=ctx.message.author.mention, inline=True)
                embed3.add_field(name="Csatorna", value=ctx.message.channel.mention, inline=True)
                embed3.add_field(name="Törölt üzenetek száma", value=int(amount), inline=True)
                await client.send_message(channel3, embed=embed3)   
        except:
            print (Exception)
            await client.say("A számnak 1 és 300 között kell lennie, és az üzenet legfeljebb 14 napos lehet! :x:")
    else:
        await client.say("Nincs jogod a parancs használatához! :x:")

@törlés.error
async def törlés_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg nem adtad meg, hogy mennyit töröljek! :x:\nHelyes használat: ?!törlés [szám]")

@client.event
async def on_member_join(member):
    if member.server.name == "#FightMan01":
        channel = discord.Object("522489336197808133")
        embed = discord.Embed(title="Felhasználó belépett", description="Részletek: ", color=0x00ffed)
        embed.add_field(name="Felhasználó", value=member.name)
        embed.add_field(name='ID', value=member.id)
        embed.set_author(name=member, icon_url=member.avatar_url)
        await client.send_message(channel, embed=embed)

@client.command(pass_context=True)
async def üdv(ctx, user: discord.Member):
    '''Használat: ?!üdv [említés]'''
    if not message.author.bot:
        await client.delete_message(ctx.message)
        if ctx.message.server.name == "#FightMan01":
            await client.say("Üdv " + user.mention + " a **" + ctx.message.server.name + "** szerveren! \n Én a **" + ctx.message.server.name + "** szerver saját készítésű botja vagyok! Hogy megtudd a parancsaimat kérlek írd be, hogy **?!parancsok**! A zenei parancsaimért a **?!zenehelp** parancsot írd be! Először 2 db kérdést szeretnék feltenni neked! Kérlek chatben válaszolj rájuk: \n :question: Első kérdésem: Ki hívott meg a szerverre (@-cal említsd meg) \n :question: Második kérdésem: Szoktál-e botokat készíteni? \n Ennyit szerettem volna kérdezni! Az egész **" + ctx.message.server.name + "** szerver nevében mégegyszer is üdvözöllek! :wave: \n Szerverünk hivatalos szövegszerkesztője: https://sourceforge.net/projects/speedeula/ \n Ha úgy tartja kedved, akkor nézz rá! :wink: \n UI.: Támogasd a botom fejlesztését! Ha összegyűlik megfelelő mennyiségű pénz, akkor a bot 0-24-ben tud futni! \n https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=S4AB6KJJ3ESU6&source=url")
        else:
            await client.say("Üdv " + user.mention + " a **" + ctx.message.server.name + "** szerveren! \n Én a **" + ctx.message.server.name + "** szerver saját készítésű botja vagyok! Hogy megtudd a parancsaimat kérlek írd be, hogy **?!parancsok**! A zenei parancsaimért a **?!zenehelp** parancsot írd be! Először 2 db kérdést szeretnék feltenni neked! Kérlek chatben válaszolj rájuk: \n :question: Első kérdésem: Ki hívott meg a szerverre (@-cal említsd meg) \n :question: Második kérdésem: Milyen játékokkal szoktál játszani? \n Ennyit szerettem volna kérdezni! Az egész **" + ctx.message.server.name + "** szerver nevében mégegyszer is üdvözöllek! :wave: ")
    else:
        return False
@üdv.error
async def üdv_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg nem említetted meg a felhasználót! :x:\nHelyes használat: ?!üdv [említés]")

@client.command(pass_context = True)
async def mute(ctx, member: discord.Member):
    '''Használat: ?!mute [említés]'''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '416226732966936577' or ctx.message.author.id == '497797334684401664':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.add_roles(member, role)
        embed=discord.Embed(title="Felhasználó némítva!", description="**{0}** némítva lett **{1}** által! :white_check_mark: ".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Hozzáférés megtagadva!", description="Nincs jogot ennek a parancsnak a használatára! :x:", color=0xff00f6)
        await client.say(embed=embed)

@mute.error
async def mute_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg nem említetted meg a felhasználót! :x:\nHelyes használat: ?!mute [említés]")

@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
    '''Használat: ?!unmute [említés]'''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '416226732966936577' or ctx.message.author.id == '497797334684401664':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.remove_roles(member, role)
        embed=discord.Embed(title="Felhasználó némítása feloldva!", description="**{0}** némításának a feloldása **{1}** által megtörtént!! :white_check_mark: ".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Hozzáférés megtagadva!", description="Nincs jogot ennek a parancsnak a használatára! :x:", color=0xff00f6)
        await client.say(embed=embed)

@unmute.error
async def unmute_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg nem említetted meg a felhasználót! :x:\nHelyes használat: ?!mute [említés]")

@client.command(pass_context=True)
async def ping(ctx):
    if not message.author.bot:
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        embed=discord.Embed(title="Pong!", description='A pinged {}ms!'.format(round((t2-t1)*1000)), color=0xffff00)
        await client.say(embed=embed)
    else:
        return False

@client.command(pass_context=True)
async def tudnivalók(ctx):
    if not message.author.bot:
        await client.delete_message(ctx.message)
        embed = discord.Embed(title="Tudnivalók", description="FightMan01 bot v6.3 ", color=0x00ff00)
        embed.add_field(name="Verzió",value="6.3", inline=True)
        embed.add_field(name="Parancslista", value="?!parancsok", inline=True)
        embed.add_field(name="Készítő", value="FightMan01", inline=True)
        embed.add_field(name="Eredeti név", value="FightMan01 bot", inline=True)
        embed.add_field(name="Újdonságokért", value="?!újdonságok", inline=True)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await client.say(embed=embed)
    else:
        return False

@client.command(pass_context=True)
async def újdonságok(ctx):
    if not message.author.bot:
        await client.say("Jelenlegi verzió: **6.3**\n**FightMan01bot** újdonságai: Hibajavítások :tools: \nA ?!help és a ?!zenehelp parancs átdolgozva :tools: \nA ?!play parancs már kulcsszó alapján is tud zenét lejátszani :tools:")
    else:
        return False
@client.command(pass_context=True)
async def összead(ctx, a: float, b: float):
    try:
        await client.say("Az összeg: {}".format(a + b))
    except:
        await client.say("Csak számokat írj be! :x:")

@összead.error
async def összead_error(error, ctx): 
    await client.say("Oops! Valami hiba van a parancsban! :x:\nHelyes használat: ?!összead [szám] [szám]\nPélda: ?!összead 2 2")

@client.command(pass_context=True)
async def kivon(ctx, a: float, b: float):
    try:
        await client.say("A különbség: {}".format(a - b))
    except:
        await client.say("Csak számokat írj be! :x:")

@kivon.error
async def kivon_error(error, ctx): 
    await client.say("Oops! Valami hiba van a parancsban! :x:\nHelyes használat: ?!kivon [szám] [szám]\nPélda: ?!kivon 2 2")

@client.command(pass_context=True)
async def szoroz(ctx, a: float, b: float):
    try:
        await client.say("A szorzat: {}".format(a * b))
    except:
        await client.say("Csak számokat írj be! :x:")

@szoroz.error
async def szoroz_error(error, ctx): 
    await client.say("Oops! Valami hiba van a parancsban! :x:\nHelyes használat: ?!szoroz [szám] [szám]\nPélda: ?!szoroz 2 2")

@client.command(pass_context=True)
async def oszt(ctx, a: float, b: float):
    try:
        await client.say("A hányados: {}".format(a / b))
    except:
        await client.say("Csak számokat írj be! :x:\nHa számot írtál be, akkor szólok, hogy a 0-val való osztást nem értelmezzük, a bot sem!!!")

@oszt.error
async def oszt_error(error, ctx): 
    await client.say("Oops! Valami hiba van a parancsban! :x:\nHelyes használat: ?!oszt [szám] [szám]\nPélda: ?!oszt 2 2")

@client.command(pass_context=True)
async def matek(ctx):
    embed = discord.Embed(title="Matematika", description="FightMan01 bot képességei ", color=0x00ff00)
    embed.add_field(name="?!összead [szám] [szám]",value="Összead két számot.", inline=True)
    embed.add_field(name="?!kivon [szám] [szám]", value="Kivon két számot.", inline=True)
    embed.add_field(name="?!szoroz [szám] [szám]", value="Összeszoroz két számot.", inline=True)
    embed.add_field(name="?!oszt [szám] [szám]", value="Eloszt két számot.", inline=True)
    await client.say(embed=embed)    

@client.command(pass_context=True)
async def bassboost(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        await client.say("Kérlek várj! :musical_note: ")
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            url = "https://youtu.be/7SGekmlVt5c"
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing
            playing = "Most megy: **Bass boosted zenék**"
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            bassboost.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        await client.say("Kérlek várj! A második zene azonnal megborít! :musical_note: ")
        try:
            server = ctx.message.server
            url = "https://youtu.be/IF4GEuzeGZ0"
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            bassboost.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        await client.say("Kérlek várj! A harmadik zene azonnal megborít! :musical_note: ")
        try:
            server = ctx.message.server
            url = "https://youtu.be/_t-u1QFoQsk"
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            bassboost.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except: 
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")



@client.command(pass_context=True)
async def kérés(ctx, *, reason: str):
    await client.say(".")
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, 2):
        messages.append(message)
    await client.delete_messages(messages)
    await client.send_message(ctx.message.server.get_member_named("FightMan01#1680"), "{} kérése a következő: ".format(ctx.message.author) + "**" + reason + "**" + "\n" + "@here")
    await client.say(":white_check_mark: A kérésedet továbbítottam! :thumbsup:")

@kérés.error
async def kérés_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg nem írtál semmilyen kérést! :x:\nHelyes használat: ?!kérés [szöveg]")

@client.command(pass_context=True)
async def segítség(ctx, *, reason: str):
    await client.say(".")
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, 2):
        messages.append(message)
    await client.delete_messages(messages)
    if ctx.message.server.name == "HunTrans Kft.":
        channel = discord.Object(id="507589115567538182")
        await client.send_message(channel, " FIGYELEM! {} segítséget kért! A következőt kéri:  ".format(ctx.message.author) + "\n" + "\n" +"**" + reason + "**")
        await client.say(":white_check_mark: A segítségkérésedet továbbítottam! :thumbsup:")
    if ctx.message.server.name == "LOL magyar közösség":
        channel1 = discord.Object(id="516166980437540864")
        await client.send_message(channel1, " FIGYELEM! {} segítséget kért! A következőt kéri:  ".format(ctx.message.author) + "\n" + "\n" +"**" + reason + "**")
        await client.say(":white_check_mark: A segítségkérésedet továbbítottam! :thumbsup:")

@client.command(pass_context=True)
async def best2018(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('l.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **2018 legjobb zenéi**"
            await client.say("**2018 legjobb zenéi** azonnal indulnak! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def best2017(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('l16.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **2017 legjobb zenéi**"
            await client.say("**2017 legjobb zenéi** azonnal indulnak! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def best2019(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('l19.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **2019 legjobb zenéi**"
            await client.say("**2019 legjobb zenéi** azonnal indulnak! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def most(ctx):
    if not message.author.bot:
        global playing
        await client.say(playing)
    else:
        return False

@client.command(pass_context=True)
async def summerhits2018(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('s18.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **2018 nyarának legforróbb slágerei**"
            await client.say("**2018 nyarának legjobb zenéi** azonnal indulnak! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def uktop40(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('uktop40.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **Anglia top 40-es listája**"
            await client.say("**Anglia top 40-es listája** azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(aliases=['r1top50'], pass_context=True)
async def radio1top50(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('r1top50.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **Rádió1 top 50-es listája**"
            await client.say("**Rádió1 top 50-es listája** azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def ncsgaming(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('ncsg.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **NCS gaming 2 órás lista**"
            await client.say("**NCS 2 órás gaming zenéi** azonnal indulnak! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def warn(ctx, member: discord.Member, *, reason : str = None):
    #await client.say(".")
    #channel = ctx.message.channel
  #  messages = []
  #  async for message in client.logs_from(channel, 2):
    #    messages.append(message)
 #   await client.delete_messages(messages)
    if not message.author.bot:
        await client.delete_message(ctx.message)
        await client.send_message(member, "Figyelmeztetést kaptál **{}** által a **{}** szerveren! Oka: **{}**".format(ctx.message.author , ctx.message.server.name , reason))
        await client.say(":white_check_mark: A figyelmeztetést sikeresen elküldtem! :thumbsup:")
        if ctx.message.server.name == "#FightMan01":
            channel = discord.Object(id="522489336197808133")
            embed = discord.Embed(title="Figyelmeztetés", description="Részletek: ", color=0x00ffed)
            embed.add_field(name="Küldő", value=ctx.message.author.mention, inline=True)
            embed.add_field(name="Figyelmeztetett", value=member.mention, inline=True)
            embed.add_field(name="Oka", value=reason, inline=True)
            await client.send_message(channel, embed=embed)
        if ctx.message.server.name == "HunTrans Kft.":
            channel2 = discord.Object(id="493754977181892609")
            embed2 = discord.Embed(title="Figyelmeztetés", description="Részletek: ", color=0x00ffed)
            embed2.add_field(name="Küldő", value=ctx.message.author.mention, inline=True)
            embed2.add_field(name="Figyelmeztetett", value=member.mention, inline=True)
            embed2.add_field(name="Oka", value=reason, inline=True)
            await client.send_message(channel2, embed=embed2)  
        if ctx.message.server.name == "Bot Support Szerver (HU)":
            channel3 = discord.Object(id="527173403468103710")
            embed3 = discord.Embed(title="Figyelmeztetés", description="Részletek: ", color=0x00ffed)
            embed3.add_field(name="Küldő", value=ctx.message.author.mention, inline=True)
            embed3.add_field(name="Figyelmeztetett", value=member.mention, inline=True)
            embed3.add_field(name="Oka", value=reason, inline=True)
            await client.send_message(channel3, embed=embed3)  
    else:
        return False

@warn.error
async def warn_error(error, ctx): 
    await client.say("Hoppá! Valószínűleg elfelejtettél valamit! :x:\nHelyes használat: ?!warn [említés] [indok]")

@client.command(aliases=['playlist'], pass_context=True)
async def playlist1(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        await client.say("Az első zene : **DJ Snake - Taki Taki ft. Cardi B, Selena Gomez, Ozuna** \nA zenét kérte: *YoooGerii08#8933*")
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            url = "https://www.youtube.com/watch?v=vZPOiMzUBCE"
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing
            playing = "Most megy: **Ti kértétek playlist**"
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            playlist1.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        await client.say("A második zene : **Majka X Curtis X Király Viktor - Füttyös** \nA zenét kérte: *YoooGerii08#8933*")
        try:
            server = ctx.message.server
            url = "https://www.youtube.com/watch?v=3MGqYCjP73A"
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            playlist1.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        await client.say("A harmadik zene : **Sukár Petro - A legnagyobb nyári sláger (Polgár Peti bemutatja)** \nA zenét kérte: *YoooGerii08#8933*")
        try:
            server = ctx.message.server
            url = "https://www.youtube.com/watch?v=awiZUMtKBTA"
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            await client.say("Azonnal indul! :thumbsup: \nMegjegyzés: Ez a zene kb 20 másodperc után indul! Sajnálom, de ez nem rajtam múlott :(")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            playlist1.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        await client.say("A negyedik zene : **Rácz Gergő x Ív - Bolondod Voltam (Newik Remix)** \nA zenét kérte: *FightMan01#1680*")
        try:
            server = ctx.message.server
            url = "https://www.youtube.com/watch?v=tXkKiDFNHkA"
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            playlist1.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        await client.say("Az ötödik zene : **Burak Yeter & Cecilia Krull - My Life Is Going On (Burak Yeter Remix) (Lyric Video)** \nA zenét kérte: *FightMan01#1680*")
        try:
            server = ctx.message.server
            url = "https://www.youtube.com/watch?v=qBDyiZ8ZXWI"
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            await client.say("Azonnal indul! :thumbsup:")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
            playlist1.cancel()
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A playlist véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def musicfm(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        await client.say("Kérlek várj! :musical_note:")
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            url = "http://79.172.241.238:8000/musicfm.mp3"
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            players[server.id] = player  
            player.start()
            player.volume = 0.2
            global playing 
            playing = "Most megy: **MusicFM élő adás**"
            global last_played
            last_played = url
            await client.say("Azonnal indul! :thumbsup:")
        except:
            print(Exception)
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("Az élő adást megállították! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm...Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True)
async def szilveszterimix(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            server = ctx.message.server
            #url = "http://77.221.39.23:8000/;stream"
            voice_client = client.voice_client_in(server)
            player = voice_client.create_ffmpeg_player('szilveszter.mp3')
            player.volume = 0.2
            players[server.id] = player  
            player.start()
            global playing 
            playing = "Most megy: **Szilveszteri mix** :tada: "
            await client.say(" A **szilveszteri mix** azonnal indul! :tada: \nHossza: **26** perc\nBoldog új évet! :beers: \nA mix készítője: **DJ Csatornafedél**")
        except:
            await client.say("Hiba történt! Kérlek próbáld meg a **?!lecsatl** parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("A zene véget ért! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(aliases=['kitiltás'], pass_context = True)
async def ban(ctx, member: discord.Member, days: int, *, reason : str = None):
    if ctx.message.author.server_permissions.administrator:
        if reason == "None":
            reason = "(Nem csatoltak üzenetet ehhez a figyelmeztetéshez!)"
        await client.send_message(member, "Ki lettél tiltva a {} szerverről {} napra a következő indokkal: **{}**".format(ctx.message.server.name, days ,reason))
        if ctx.message.server.name == "#FightMan01":
            channel = discord.Object(id="522489336197808133")
            embed = discord.Embed(title="Kitiltás", description="Részletek: ", color=0x00ffed)
            embed.add_field(name="Moderátor", value=ctx.message.author.mention, inline=True)
            embed.add_field(name="Kitiltott", value=member.mention, inline=True)
            embed.add_field(name="Oka", value=reason, inline=True)
            embed.add_field(name="Időtartam (nap)", value=days, inline=True)
            await client.send_message(channel, embed=embed)
        if ctx.message.server.name == "HunTrans Kft.":
            channel2 = discord.Object(id="493754977181892609")
            embed2 = discord.Embed(title="Kitiltás", description="Részletek: ", color=0x00ffed)
            embed2.add_field(name="Moderátor", value=ctx.message.author.mention, inline=True)
            embed2.add_field(name="Kitiltott", value=member.mention, inline=True)
            embed2.add_field(name="Oka", value=reason, inline=True)
            embed2.add_field(name="Időtartam (nap)", value=days, inline=True)
            await client.send_message(channel2, embed=embed2) 
        if ctx.message.server.name == "Bot Support Szerver (HU)":
            channel3 = discord.Object(id="527173456496689183")
            embed3 = discord.Embed(title="Kitiltás", description="Részletek: ", color=0x00ffed)
            embed3.add_field(name="Moderátor", value=ctx.message.author.mention, inline=True)
            embed3.add_field(name="Kitiltott", value=member.mention, inline=True)
            embed3.add_field(name="Oka", value=reason, inline=True)
            embed3.add_field(name="Időtartam (nap)", value=days, inline=True)
            await client.send_message(channel3, embed=embed3)   
        await client.ban(member, days)
    else:
        await client.say("Nincs jogod a parancs használatához! :x:")

@ban.error
async def ban_error(error, ctx): 
    await client.say("Oopss! Valami hiányzik! :x:\nHelyes használat: ?!ban [említés] [időtartam (napban)] [indok]")

@client.event
async def on_member_remove(member):
    if member.server.name == "#FightMan01":
        channel = discord.Object("522489336197808133")
        embed = discord.Embed(title="Felhasználó kilépett", description="Részletek: ", color=0x00ffed)
        embed.add_field(name="Felhasználó", value=member.name)
        embed.add_field(name='Csatlakozott', value=member.joined_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'))
        embed.set_author(name=member, icon_url=member.avatar_url)
        await client.send_message(channel, embed=embed)
    
@client.command(aliases=['bc'], pass_context=True)
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("A bitcoin árfolyama: $" + response['bpi']['USD']['rate'])  

@client.command(aliases=['8ball'],pass_context=True)
async def kérdés(ctx, *, msg:str):
    if not message.author.bot:
        possible_responses = [
            'Igen',
            'Talán...',
            'Nem',
            'Most nem tudok válaszolni :(',
            'Határozottan!',
            'Talán... nem',
            'Talán... igen'
        ]
        embed3 = discord.Embed(title="Kérdés", description="Válaszom: ", color=0x00ff00)
        embed3.add_field(name="Kérdező", value=ctx.message.author.mention, inline=False)
        embed3.add_field(name="Kérdés", value=msg, inline=False)
        embed3.add_field(name="Válaszom", value=random.choice(possible_responses), inline=False)
        await client.say(embed=embed3)
    else:
        return False
@kérdés.error
async def kérdés_error(error, ctx): 
    await client.say("Oopss! Valószínűleg nem kérdeztél semmit! :x:\nHelyes használat: ?!kérdés [kérdés]")

@client.command(pass_context=True, aliases=['retroradio', 'retró'])
async def retro(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        await client.say("Kérlek várj! :musical_note:")
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            url = "http://stream.retroradio.hu/high.mp3"
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            players[server.id] = player  
            player.start()
            player.volume = 0.2
            global playing 
            playing = "Most megy: **Retró rádió élő adás**"
            playing = player.title
            global last_played
            last_played = url
            await client.say("Azonnal indul! :thumbsup:")
        except:
            print(Exception)
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("Az élő adást megállították! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

@client.command(pass_context=True, aliases=['petofi', 'petofiradio'])
async def petőfi(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    if voice_client == None:
        await client.say("Kérlek várj! :musical_note:")
        try:
            channel = ctx.message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except:
            return False
        try:
            url = "http://mr-stream.mediaconnect.hu:80/4738/mr2.mp3"
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
            players[server.id] = player
            player.start()
            player.volume = 0.2
            global playing 
            playing = "Most megy: **Petőfi rádió élő adás**"
            global last_played
            last_played = url
            await client.say("Azonnal indul! :thumbsup:")
        except:
            print(Exception)
            await client.say("Hiba történt! Kérlek próbáld meg a ?!lecsatl parancsot, majd próbáld újra! :x:")
        while not player.is_done():
            await asyncio.sleep(1)
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("Az élő adást megállították! A bot most **automatikusan** lecsatlakozik! :white_check_mark: ")
        except:
            return False
    else:
        await client.say("Hmm... Azt észleltem, hogy jelenleg szól egy zene. Mielőtt ezt elkezdenéd hallgatni, kérlek írd be, hogy **?!lecsatl** ! :x:")

#client.loop.create_task(wc())
client.run(os.environ.get("TOKEN"))
