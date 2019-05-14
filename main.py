import csv
import time
import json
from urllib import request

from bs4 import BeautifulSoup

data_stat_dict = {
    'Batters': {
        'G': 'G',
        'PA': 'PA',
        'AB': 'AB',
        'R': 'R',
        'H': 'H',
        '2B': '2B',
        '3B': '3B',
        'HR': 'HR',
        'RBI': 'RBI',
        'SB': 'SB',
        'CS': 'CS',
        'BB': 'BB',
        'SO': 'SO',
        'BA': 'batting_avg',
        'OBP': 'onbase_perc',
        'SLG': 'slugging_perc',
        'OPS': 'onbase_plus_slugging',
        'TB': 'TB',
        'GDP': 'GIDP',
        'HBP': 'HBP',
        'SH': 'SH',
        'SF': 'SF',
        'IBB': 'IBB',
    },
    'Pitchers': {
        'W': 'W',
        'L': 'L',
        'W-L%': 'win_loss_perc',
        'ERA': 'earned_run_avg',
        'G': 'G',
        'GS': 'GS',
        'SV': 'SV',
        'IP': 'IP',
        'H': 'H',
        'R': 'R',
        'ER': 'ER',
        'HR': 'HR',
        'BB': 'BB',
        'IBB': 'IBB',
        'SO': 'SO',
        'HBP': 'HBP',
        'BK': 'BK',
        'WP': 'WP',
        'BF': 'batters_faced',
        'WHIP': 'whip',
        'SO9': 'strikeouts_per_nine',
        'SO/W': 'strikeouts_per_base_on_balls',
    }
}


def parse_data(player_type, url, player_data, player_name):
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    game_logs = {'Pitchers': 'pitching_gamelogs_milb', 'Batters': 'batting_gamelogs_milb'}
    latest_row = soup.find(id=game_logs[player_type]).find_all('tr')[-1]
    level = latest_row.find('td', {'data-stat': 'level'}).text.split('-')[0]
    table_name = {'Pitchers': 'pitching_splits_milb_gl', 'Batters': 'batting_splits_milb'}
    table = soup.find(id=table_name[player_type])
    headers = [header.text for header in table.find('thead').find('tr').find_all('th')]
    headers.remove('Split')
    for row in table.find_all('tr', {'class': 'full'})[:4]:
        try:
            split_val = row.find('th', {'data-stat': 'split_name'}).text
            row_dict = {}
            for header in headers:
                    data_stat_instance = {'data-stat': data_stat_dict[player_type][header]}
                    row_val = row.find('td', data_stat_instance)
                    row_dict[header] = row_val.text
                    row_dict['Name'] = f'{player_name} ({level})'
            player_data[player_type][split_val].append(row_dict)
        except Exception as e:
            print(e)

    return player_data


player_data = {
    'Pitchers': {
        'Total': [],
        'Last 7 days': [],
        'Last 28 days': [],
        'Last 90 days': [],
    },
    'Batters': {
        'Total': [],
        'Last 7 days': [],
        'Last 28 days': [],
        'Last 90 days': [],
    }
}

# csv_string = 'owned_links.csv'
csv_string = 'tracking_links.csv'
json_string = f'{csv_string.split("_")[0]}.json'
with open(csv_string) as f:
    reader = csv.reader(f)
    for csv_row in reader:
        print(csv_row[0])
        # try:
        player_data = parse_data(csv_row[2], csv_row[1], player_data, csv_row[0])
        # except Exception as e:
        #     print(e)
        #     data = None
        # player_data[csv_row[0]] = data
        time.sleep(1)

f = open(f'../frontend/milb_tracker/src/assets/output/{json_string}', 'w')
f.write(json.dumps(player_data))
f.close()
