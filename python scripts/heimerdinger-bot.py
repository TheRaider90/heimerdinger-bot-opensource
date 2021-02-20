# Modules
from riotwatcher import LolWatcher
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import discord
import pickle

# initializing api key, lolwatcher and bot
load_dotenv()
discordToken = os.getenv("DISCORD_TOKEN")
discordGuild = os.getenv("DISCORD_GUILD")
LiveFeedTimer = os.getenv("TIME_IN_SECONDS")
riotApiKey = os.getenv("RIOT_API_KEY")
riotApiRegion = os.getenv("RIOT_API_REGION")
liveFeedChannelID = os.getenv("LIVE_FEED_CHANNEL_ID")

watcher = LolWatcher(riotApiKey)
bot = commands.Bot(command_prefix='!')
version = "1.0 beta_release_opensource"



# bot startup
@bot.event
async def on_ready():

    # update database at start
    data = loadIdData()
    for key, value in data.items():
        data[key] = getId(key)
    writeIdData(data)
    
    #print out startup messages
    print("The Heimerdinger-Bot  has joined " + discordGuild)
    print("Version: " + version)


    #start 60s task
    await my_task.start()

    





#task for updating
@tasks.loop(seconds=int(LiveFeedTimer))
async def my_task():
    await update()
    
    print("Heimerdinger recently updated your live-feed list! [this happens every " + LiveFeedTimer + " seconds]")


#!stats [name] command
@bot.command(name="stats")
async def stats(ctx,*,summonerName):  
    
    embed = discord.Embed(title=summonerName, color=discord.Colour.red())

    try:
        me = watcher.summoner.by_name(str(riotApiRegion), summonerName)
        stats = watcher.league.by_summoner(str(riotApiRegion), me['id'])

        winrate = int(stats[0]['wins']) / (int(stats[0]['wins']) + int(stats[0]['losses']))

        embed.add_field(name="Current rank", value=stats[0]['tier'] + " with " + str(stats[0]['leaguePoints']) + " LP", inline=False)
        embed.add_field(name="Winrate", value=str(int(winrate * 100)) + " %", inline=False)
    except Exception:
        embed.add_field(name="Current rank", value="No ranked stats available")
    await ctx.send(embed=embed)



#!game [name] command
@bot.command(name="game")
async def game(ctx, *, summonerName):
    await ctx.send(embed=printInfo(summonerName))



#returns message with details (riot api) for discord text
def printInfo(summonerName):
    #setup for riot api
    me = watcher.summoner.by_name(str(riotApiRegion), summonerName)
    my_matches = watcher.match.matchlist_by_account(str(riotApiRegion), me['accountId'])
    last_match = my_matches['matches'][0]
    match_detail = watcher.match.by_id(str(riotApiRegion), last_match['gameId'])
    latest = watcher.data_dragon.versions_for_region(str(riotApiRegion))['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'de_DE')

    #champion id to champion name translation
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']

    #finding out the id of the wanted summoner
    dic = {
        (match_detail['participantIdentities'][0]['player']['summonerName']).lower().replace(" ", ""): 0,
        (match_detail['participantIdentities'][1]['player']['summonerName']).lower().replace(" ", ""): 1,
        (match_detail['participantIdentities'][2]['player']['summonerName']).lower().replace(" ", ""): 2,
        (match_detail['participantIdentities'][3]['player']['summonerName']).lower().replace(" ", ""): 3,
        (match_detail['participantIdentities'][4]['player']['summonerName']).lower().replace(" ", ""): 4,
        (match_detail['participantIdentities'][5]['player']['summonerName']).lower().replace(" ", ""): 5,
        (match_detail['participantIdentities'][6]['player']['summonerName']).lower().replace(" ", ""): 6,
        (match_detail['participantIdentities'][7]['player']['summonerName']).lower().replace(" ", ""): 7,
        (match_detail['participantIdentities'][8]['player']['summonerName']).lower().replace(" ", ""): 8,
        (match_detail['participantIdentities'][9]['player']['summonerName']).lower().replace(" ", ""): 9
    }
    
    
    #stats
    thisId = dic[summonerName.lower().replace(" ", "")]
    thisQId = match_detail['queueId']
    thisQ = ' '
    thisChamp = match_detail['participants'][thisId]['championId']
    thisChampName = champ_dict[str(thisChamp)]
    thisKills = match_detail['participants'][thisId]['stats']['kills']
    thisDeaths = match_detail['participants'][thisId]['stats']['deaths']
    thisAssists = match_detail['participants'][thisId]['stats']['assists']
    thisWinId = match_detail['participants'][thisId]['stats']['win']
    thisWin = ' '
    thisTime = round((int(match_detail['gameDuration']) / 60), 2)
    thisMultiKill = match_detail['participants'][thisId]['stats']['largestMultiKill']
    thisDamage = match_detail['participants'][thisId]['stats']['totalDamageDealtToChampions']
    thisVision = match_detail['participants'][thisId]['stats']['visionScore']
    thisMinion = match_detail['participants'][thisId]['stats']['totalMinionsKilled']
    thisPink = match_detail['participants'][thisId]['stats']['visionWardsBoughtInGame']
    thisGold = int(match_detail['participants'][thisId]['stats']['goldEarned'])
    thisMinionPerMin = round((thisMinion / thisTime), 2)
    thisVisionPerMin = round((thisVision / thisTime), 2)
    thisGoldPerMinute = round((thisGold / thisTime), 2)
    thisStats = watcher.league.by_summoner(str(riotApiRegion), me['id'])
    thisWinrateStat = ' '
    thisWinrate = ' '
    thisRank = ' '
    thisLP = ' '


    if thisQId == 420:
        thisQ = "RANKED"
    elif thisQId == 400:
        thisQ = "NORMAL"
    else:
        thisQ = "OTHER"

    
    if str(thisWinId) == 'True':
        thisWin = "won"
    else:
        thisWin = "lost"


    if thisId > 4:
        thisDamage1 = match_detail['participants'][5]['stats']['totalDamageDealtToChampions']
        thisDamage2 = match_detail['participants'][6]['stats']['totalDamageDealtToChampions']
        thisDamage3 = match_detail['participants'][7]['stats']['totalDamageDealtToChampions']
        thisDamage4 = match_detail['participants'][8]['stats']['totalDamageDealtToChampions']
        thisDamage5 = match_detail['participants'][9]['stats']['totalDamageDealtToChampions']
    else:
        thisDamage1 = match_detail['participants'][0]['stats']['totalDamageDealtToChampions']
        thisDamage2 = match_detail['participants'][1]['stats']['totalDamageDealtToChampions']
        thisDamage3 = match_detail['participants'][2]['stats']['totalDamageDealtToChampions']
        thisDamage4 = match_detail['participants'][3]['stats']['totalDamageDealtToChampions']
        thisDamage5 = match_detail['participants'][4]['stats']['totalDamageDealtToChampions']

    thisTeamDamage = thisDamage1 + thisDamage2 + thisDamage3 + thisDamage4 + thisDamage5
    thisDamageRatio = round((float(thisDamage) / float(thisTeamDamage)) * 100, 2)


    try:
        thisWinrate = int(thisStats[0]['wins']) / (int(thisStats[0]['wins']) + int(thisStats[0]['losses']))
        thisWinrateStat = str(int(thisWinrate * 100))
        thisRank = str(thisStats[0]['rank'])
        thisTier = str(thisStats[0]['tier'])
        thisLP = str(thisStats[0]['leaguePoints'])
    except IndexError:
        print("no ranked stats available for " + str(summonerName))
    
    #constructing the message

    

    if thisQ == "OTHER":
        embed = discord.Embed(title = "**" + str(summonerName).upper() + "** has recently **" + thisWin + "** a game on **" + str(thisChampName) + "**", color = discord.Colour.blue())
    else:
        embed = discord.Embed(title = "**" + str(summonerName).upper() + "** has recently **" + thisWin + "** a **" + str(thisQ) + "** game on **" + str(thisChampName) + "**", color = discord.Colour.blue())
    
    embed.add_field(name="Game length", value=str(int(thisTime)) + " minutes")
    
    try:
        embed.add_field(name="Stats", value= str(thisKills) + " | " + str(thisDeaths) + " | " + str(thisAssists) + " | KDA: " + str(round((int(thisKills) + int(thisAssists)) / int(thisDeaths), 2)), inline=False)
    except Exception:
        embed.add_field(name="Stats", value= str(thisKills) + " | " + str(thisDeaths) + " | " + str(thisAssists), inline=False)
    
    embed.add_field(name="Minions", value=str(thisMinion) + " | minions per minute: " + str(thisMinionPerMin) + " | delta perfect farm: " + str(round((float(10.0) - float(thisMinionPerMin)),2)) + "", inline=False)
    embed.add_field(name="Vision score", value=str(thisVision) + " | vision per minute: " + str(thisVisionPerMin) + " | control wards purchased: " + str(thisPink), inline=False)
    embed.add_field(name="Gold earned", value=str(thisGold) + " | gold per minute: " + str(thisGoldPerMinute), inline=False)
    embed.add_field(name="Damage dealt", value=str(thisDamage) + " | player/team damage ratio: " + str(thisDamageRatio) + "% | largest multikill: " + str(thisMultiKill), inline=False)

    if thisWinrate == ' ':
        embed.add_field(name="Current rank", value="no ranked data available", inline=False)
    else:
        embed.add_field(name="Current rank", value=thisTier + " " + thisRank + " with " + thisLP + " LP | winrate: " + thisWinrateStat + "%", inline=False)

    #returning the message for discord
    return embed



#returns last match id of [summonerName]
def getId(summonerName):
    me = watcher.summoner.by_name(str(riotApiRegion), summonerName)
    my_matches = watcher.match.matchlist_by_account(str(riotApiRegion), me['accountId'])
    last_match = my_matches['matches'][0]

    return str(last_match['gameId'])
    


#printInfo in live-feed discord channel
async def printLive(summonerName):
    channel = bot.get_channel(int(liveFeedChannelID))
    await channel.send(embed=printInfo(summonerName))



#writes new file in obj folder
def writeIdData(obj):
    name = "id_data"
    with open('obj/'+ name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, protocol=0)



#loads current file in obj folder
def loadIdData():
    try:
        name = "id_data"
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception:
        return {}
    


#updates current file in obj folder
async def update():
    data = loadIdData()

    for key, value in data.items():
        if str(value) != getId(key):
            await printLive(key)
            data[key] = getId(key)

    writeIdData(data)

    

#!add command for adding summoners to live-feed
@bot.command(name="add")
async def add(ctx, *, summonerName): 
    try:
        data = loadIdData()
        data[summonerName.lower().replace(" ", "")] = getId(summonerName)
        writeIdData(data)

        await ctx.send(summonerName + " was successfully added to live-feed!")
    except Exception:
        await ctx.send("Oops! There is no summoner with that name!") 



#!remove command for removing summoners of live-feed
@bot.command(name="remove")
async def remove(ctx, *, summonerName):
    data = loadIdData()
    if summonerName.lower().replace(" ", "") in data: del data[summonerName.lower().replace(" ", "")]
    writeIdData(data)

    await ctx.send(summonerName + " was successfully removed from live-feed!")

    

#!list command to show all summoner on live-feed
@bot.command(name="list")
async def showData(ctx):

    response = ""

    for key, value in loadIdData().items():
        response += key.upper() + ", "

    response = response[:-2]
    embed = discord.Embed(title="Live feed list", description=response, colour=discord.Colour.blurple())

    await ctx.send(embed=embed)



#!tutorial for live-feed tutorial
@bot.command(name="tutorial")
async def tutorial(ctx):
    
    embed = discord.Embed(title = "Live-Feed Tutorial", desciription="You can now add accounts to the live-feed. Matches of accounts on the list get tracked in the channel 'live-feed'",colour = discord.Colour.blurple())
    embed.add_field(name="!add [summonerName]", value="Use this command to add accounts to the live feed", inline=False)
    embed.add_field(name="!remove [summonerName]", value="Use this command to remove accounts to the live feed", inline=False)
    embed.add_field(name="!list", value="Shows all accounts currently on live feed", inline=False)

    await ctx.send(embed=embed)


#starts the bot
bot.run(discordToken)
