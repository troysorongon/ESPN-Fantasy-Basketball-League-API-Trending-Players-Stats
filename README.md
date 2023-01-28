# ESPN Fantasy Basketball League API Trending Players Stats 

This Python3 program uses ESPN Fantasy Basketball API to show the **stats of the Trending available players/free agents** stats in your ESPN Fantasy Basketball League. The information of the players and the stats are displayed in a dataframe format. 

<hr>

## Output
This project displays the relevant facts of the players such as:

* Player's Full name
* Player's Position(s)
* Injured (True/False)
* Injury Status (Active/Day-to-Day/Out)

as well as the relevant stats of the players such as:

* **Last 7 Day** Average Stats
* **Last Game** Fantasy Points
* **2nd Last Game** Fantasy Points
* **3rd Last Game** Fantasy Points
* **4th Last Game** Fantasy Points
* **5th Last Game** Fantasy Points

## Required Fields **(Refer to Jupyter Notebook file to find where to get this information)**
1. swid
2. espn_s2
3. User-Agent
4. Referer
5. LeagueID

## Installation

With Git in Terminal:
```
git clone https://github.com/troysorongon/ESPN-Fantasy-Basketball-League-API-Trending-Players-Stats.git
cd ESPN-Fantasy-Basketball-League-API-Best-Last-7-Day-Avg-Stats
```
**

Using IDE (e.g Visual Studio Code)
1. Download ZIP file
2. Unzip ZIP file
3. Open folder in IDE
4. Install **requests** (If not already installed, use "sudo" if needed)
```
pip install requests
```
5. Install **pandas** (If not already installed, use "sudo" if needed)
```
pip install pandas
```

## Steps Before Executing

1.**"micro"** into the file (If using Terminal)
```
micro ESPN_Fantasy_API_Best_Last_7_Day_Avg_git.py
```
2. Fill in the fields that say "Fill in" with your information **OR** uncomment the options to get a user input for those fields
3. Save File (Ctrl + S **OR** Command + S)

## Executing
On Terminal:
```
python3 ESPN_Fantasy_API_Best_Last_7_Day_Avg_git
```
**

On IDE:  Run program 

**May take a few seconds for the progeam to finish executing due to requesting data from the ESPN API, computation algorithm, and/or CPU speed on your host machine**

## Future Implementations
1. Filter the players based on position
2. Select the amount of players to display 
3. Make the program faster with better algorithms

## [Discussions](https://github.com/troysorongon/ESPN-Fantasy-Basketball-League-API-Best-Last-7-Day-Avg-Stats/discussions)
If you would like to share any ideas of new implementations or have any comments about the program. please feel free to share in **Discussions**!

## [Issues](https://github.com/troysorongon/ESPN-Fantasy-Basketball-League-API-Best-Last-7-Day-Avg-Stats/issues)
Please report any issues or bugs that may come across [here](https://github.com/troysorongon/ESPN-Fantasy-Basketball-League-API-Best-Last-7-Day-Avg-Stats/issues)
