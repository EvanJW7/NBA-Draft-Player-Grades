from bs4 import BeautifulSoup
import requests 
import pandas as pd 

headers = {'User Agent':'Mozilla/5.0'}

players = ['will-barton', 'tyler-zeller', 'terrence-jones', 'anthony-davis-5', 'michael-kidd-gilchrist', 
           'bradley-beal', 'dion-waiters','thomas-robinson-2', 'damian-lillard', 'harrison-barnes', 'terrence-ross', 
           'andre-drummond', 'austin-rivers', 'meyers-leonard', 'jeremy-lamb', 'kendall-marshall', 'john-henson', 
           'maurice-harkless', 'royce-white', 'andrew-nicholson', 'jared-sullinger', 'fab-melo', 'john-jenkins', 
           'jared-cunningham', 'tony-wroten', 'miles-plumlee', 'arnett-moultrie', 'perry-jones', 'marquis-teague', 
           'festus-ezeli', 'jeff-taylor', 'bernard-james', 'jae-crowder', 'draymond-green', 'orlando-johnson', 
           'quincy-acy', 'quincy-miller', 'khris-middleton', 'tyshawn-taylor', 'doron-lamb', 'mike-scott', 
           'kim-english', 'justin-hamilton-2', 'daruis-miller', 'kyle-oquinn', 'kris-joseph', 'darius-johnson-odom', 
           'robbie-hummel', 'marcus-denmon', 'robert-sacre']

player_stats = []
playerlist = []
year_list = []
age_list = []

for player in players:
    try:
        if player[-1].isdigit():
            url = f'https://www.sports-reference.com/cbb/players/{player}.html'
        else:
            url = f'https://www.sports-reference.com/cbb/players/{player}-1.html'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        header = [th.getText() for th in soup.findAll('tr', limit = 2)[0].findAll('th')]
        rows = soup.findAll('tr')
        player_stats.append([td.getText() for td in soup.find('tr', id ='players_per_game.2012')])
        table = pd.DataFrame(player_stats, columns = header) 
        for i in player_stats:
            if i[14] == '':
                i[14] = str(0.0)
        
        player = player.replace('-',' ').title()
        if player[-2].isdigit():
            player = player[:-3]
        if player[-1].isdigit():
            player = player[:-2]
        if player[-2:] == 'jr':
            player = player.replace('jr', ' Jr')
        if player[-3:] == 'iii':
            player = player.replace('iii', ' III')
        playerlist.append(player)
        
    except:
        continue
    try:
        player = player.replace('-', '+')
        url = f'https://www.google.com/search?q={player}+basketball+birth+date'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        age = (soup.findAll('div', class_ = 'BNeawe iBp4i AP7Wnd')[0])
        for x in age:
            x = x.text
        x = x.replace(',','').split()
        months = {
            'Janurary': '1',
            'February': '2',
            'March': '3',
            'April': '4',
            'May': '5',
            'June': '6',
            'July': '7',
            'August': '8',
            'September': '9',
            'October': '10',
            'November': '11',
            'December': '12'
        } 
        birth_date = months[x[0]]+ '-' + x[1] + '-' + x[2]
        draft_date = '7-1-2012'
        import datetime 
        birth_date_final = datetime.datetime.strptime(birth_date, '%m-%d-%Y')  
        draft_date_final = datetime.datetime.strptime(draft_date, '%m-%d-%Y')

        age_on_draft_night = draft_date_final - birth_date_final
        age = round(age_on_draft_night.days/365, 1)
        age_list.append(age)
        year = round(((1-(age/35))*2.33), 2)
        year_list.append(year)
        
    except:
        age_list.append("No data")
        year_list.append(.85)
        
age_list[0] = 21.5
year_list[0] = .88
age_list[1] = 22.5
year_list[1] = .82
age_list[2] = 20.5
year_list[2] = .95

table.insert(0, "Name", playerlist)
table.insert(2, "Year", year_list)
table.insert(2, "Age", age_list)

table['MP'] = table['MP'].astype(float)
table['PTS'] = table['PTS'].astype(float)
table['AST'] = table['AST'].astype(float)
table['TRB'] = table['TRB'].astype(float)
table['BLK'] = table['BLK'].astype(float)
table['STL'] = table['STL'].astype(float)
table['3P'] = table['3P'].astype(float)
table['3PA'] = table['3PA'].astype(float)
table['TOV'] = table['TOV'].astype(float)
table['SOS'] = table['SOS'].astype(float)
table['PF'] = table['PF'].astype(float)
table['FT%'] = table['FT%'].astype(float)
table['3P%'] = table['3P%'].astype(float)

table["Player Grade"] = ((table['PTS']) + (table['TRB']*1.25) + (table['AST']*2) +
(table['BLK']*2) + (table['STL']*3) + (table['3P']*2) + (table['3PA']) + (table['SOS']/2)) * table['Year']

table["Player Grade"] = table["Player Grade"]*1.75
table["Player Grade"] = (round(table["Player Grade"], 1))
table["Player Grade"]= table["Player Grade"].astype(float)
                        
table = table.sort_values(by= "Player Grade", ascending=False)
table.insert(5, 'SoS', table['SOS'])
table.reset_index(drop = True, inplace=True)
import numpy as np
table.index = np.arange(1, len(table)+1)
del table['SOS']
del table['Conf']
del table['ORB']
del table['DRB']
del table['GS']
del table['FG']
del table['FGA']
del table['FT']
del table['FTA']
del table['2P']
del table['2PA']
del table['2P%']
del table['Year']
del table['TOV']
del table['PF']

print(table)