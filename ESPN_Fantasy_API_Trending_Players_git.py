import requests
import pandas as pd

# URL to get the current scoring period for the day
scoringPeriodUrl = " https://fantasy.espn.com/apis/v3/games/fba/seasons/2023?view=kona_game_state"

# Tells ESPN that it is you that wants to retrieve their data by authenticating your personal cookies
# One of the parameters used for requests.get()
espn_cookies = {
    'swid': '',     # Fill in --> Found in "Cookies"
    'espn_s2': ''   # Fill in  --> Found in "Cookies"
}

# Option to use a user input for the 'swid' and 'espn_s2'
#espn_cookies['swid'] = input("Enter 'swid': ")
#espn_cookies['espn_s2'] = input("Enter 'espn_s2': ")

# Same as cookies: used to authenticate to ESPN that it is you when requesting data
headerz = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': ''    # Fill in --> Search "What is my User-Agent" on google
}

# Retrieves the raw data
scoringPeriod = requests.get(scoringPeriodUrl, 
                 headers=headerz,
                 cookies=espn_cookies)

# Stores the raw data into a .json file 
scoringPeriodData = scoringPeriod.json()

# Indexes through the data to only get the current Scoring Period ID
currentScoringPeriod = scoringPeriodData['currentScoringPeriod']['id']

# This header section has additional fields that filter the data that is retrieved. In this case, I only want to 
# get the data of the available players who are the most TRENDING. If we use the 
# previous headerz, the data returned will be data for the first 50 players in alphabetical order
headerz = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': '',   # Fill in --> Search "What is my User-Agent" on google
    'Referer': '',  # Fill in --> The URL for the website found in your browser. "Players" tab --> "Add Players" --> "Trending" tab
    'X-Fantasy-Source': 'kona',
    # Filter uses the current Scoring Period
    'X-Fantasy-Filter': '{"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS"]},"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11]},"filterRanksForScoringPeriodIds":{"value":['+str(currentScoringPeriod)+']},"sortRating":{"value":1,"sortPriority":1,"sortAsc":false},"limit":12,"filterStatsForTopScoringPeriodIds":{"value":5,"additionalValue":["002023","102023","002022","012023","022023","032023","042023"]}}}',
    'X-Fantasy-Platform': 'kona-PROD-329ab810189bc3c7f613e890143a5dfa53071abf'
}

# League ID for your league can be found in the URL of your fantasy league home page
leagueID = ""   # Fill in --> found in URL in your browser

# Option to use a user input to get the League ID
#leagueID = input("Enter your League ID: ")

# URL get the data of players based on the League ID
url = 'https://fantasy.espn.com/apis/v3/games/fba/seasons/2023/segments/0/leagues/'+leagueID+'?view=kona_player_info'
r = requests.get(url, 
                 headers=headerz,
                 cookies=espn_cookies)

# Stores the raw data into a .json file
espn_data = r.json()

# Only want the data of the players
espn_data = espn_data['players']

playerStats = {}    # Stores the Fantasy Points for each player's last 5 games, the Last 7 Day Average Stats, and Position
playerPosition = {} # Stores the position slot number(s) that represents the position of each player 

for i in range(0, 12): 
    # For each player, only want to look at the 'player' information that holds name, stats, and injury status
    espn_data[i] = espn_data[i]['player']

# This section get the player's stats

    #Creates a nested dictionary by creating a dictionary at index i to store all each player's stats
    playerStats[i] = {}
    
    for n in range(0, 5):
        # Only care about the "appliedTotal" which is the total Fantasy Points scored for that game
        # Stores the last 5 game Fantasy Points for player at index i
        playerStats[i][n] = round(espn_data[i]['stats'][n]['appliedTotal']) # Rounds to nearest whole number
        
        # Rename the Keys to be appropriate for the columns of the dataframe
        match n:
            case 0:
                playerStats[i]["Last Game Pts"] = playerStats[i].pop(n)
            case 1:
                playerStats[i]["2nd Last Pts"] = playerStats[i].pop(n)
            case 2:
                playerStats[i]["3rd Last Pts"] = playerStats[i].pop(n)
            case 3:
                playerStats[i]["4th Last Pts"] = playerStats[i].pop(n)
            case 4:
                playerStats[i]["5th Last Pts"] = playerStats[i].pop(n)
    
    # Index 7 holds the Last 7 Day AVG Fantasy Points
    playerStats[i]["Last 7 Day Avg"] = round(espn_data[i]['stats'][7]['appliedAverage'], 1) # Rounds to nearest tenths place

# This section get the player's Position

    #Creates a nested dictionary by creating a dictionary at index q to store all each player's position
    playerPosition[i] = {}

    idx = 0
    slots = espn_data[i]['eligibleSlots'] # All possible position slots
    
    # Nested for loop that goes through all position slots 
    for w in range(0, len(slots)):
        # ONLY care about positions from PG to C (0-4) and NOT the bench slots (5-13)
        if((espn_data[i]['eligibleSlots'][w]) <= 4): 
            playerPosition[i][idx] = espn_data[i]['eligibleSlots'][w]
            idx+=1

# This section converts the player's position slot numbers to their actual position (PG - C)

    for p in range(0, len(playerPosition[i])):
        position = playerPosition[i][p]
        
        # Switch statement to convert the position slot to the actual position
        match position:
            case 0:
                playerPosition[i][p] = "PG"
            case 1:
                playerPosition[i][p] = "SG"
            case 2:
                playerPosition[i][p] = "SF"
            case 3:
                playerPosition[i][p] = "PF"
            case 4:
                playerPosition[i][p] = "C"

# This section concatenates the player's primary position to any secondary positions (i.e SG/SF)

    position = playerPosition[i][0] # Primary position of player
    for u in range(1, len(playerPosition[i])):
        position += '/' + playerPosition[i][u] # Adds the secondary position(s) to replicate the real position on fantasy app
    playerStats[i]['position'] = position  # Adds the positions(s) to playerStats dictionary

# Converts the dictionaries into dataframes
df1 = pd.DataFrame(espn_data)
df2 = pd.DataFrame(playerStats)

# Swaps the order of the columns and rows: columns = stats, rows = players
# Swapped in order to match the index with df1
df2 = df2.transpose()

# Filters only the 'fullName', 'injured', and 'injuryStatus' status from the dataframe
player_df = df1[['fullName', 'injured', 'injuryStatus']]

# Joins the two dataframes and matches the index of player_df
result = player_df.join(df2, how = 'left')

# Reorders the columns
result = result[['fullName', 'position', 'injured', 'injuryStatus', 'Last 7 Day Avg', 'Last Game Pts', '2nd Last Pts', '3rd Last Pts', '4th Last Pts', '5th Last Pts']]

print()
print(result.to_string())
print()

result.to_csv("Fantasy_Basketball_Trending_Players_Stats.csv", index = False) 
