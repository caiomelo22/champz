from urllib.request import Request, urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import requests
import io
import json
import os

positions_dict = {'Goalkeepers': 'GK', 'Center Backs': 'CB', 'Full Backs': 'RB,LB, RWB, LWB', 'Defensive Midfielders': 'CDM,CM',
                 'Ofensive Midfielders': 'CAM', 'Wingers': 'LW,LF,LM,RF,RW,RM', 'Attackers': 'ST,CF'}

base_url = "https://www.futbin.com/players?page=1&version=gold_rare&pos_type=all&position="

def save_image(img, directory, file_name):
    image_content = requests.get(img).content
    image_file = io.BytesIO(image_content)
    directory = f"dist/{file_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = f'{directory}/{file_name}'
    
    open(file_path, "wb").write(image_file.getbuffer())
    return file_path

positions = []
teams = []
nations = []
players = []

options = uc.ChromeOptions() 
options.headless = False  
driver = uc.Chrome(use_subprocess=True, options=options)
driver.maximize_window()

for index, name in enumerate(positions_dict):
    positions.append({
        'id': index + 1,
        'name': name,
        'specific_positions': positions_dict[name]
    })

    for page in range(1, 4):
        url = base_url + positions_dict[name]

        url = f'{url}&page={page}'
        print(url)

        driver.get(url)

        driver.maximize_window()
        time.sleep(5)

        players_1 = driver.find_elements(By.CLASS_NAME, "player_tr_1")
        players_2 = driver.find_elements(By.CLASS_NAME, "player_tr_2")
        players_trs = players_1 + players_2
        cont = 0
        
        for p in players_trs:
            player = {
                'position': positions[-1]['id']
            }

            tds = p.find_elements(By.TAG_NAME, "td")

            player["id"] = tds[0].find_element(By.TAG_NAME, "div").get_attribute('data-playerid')
            player["name"] = tds[1].find_element(By.XPATH, "div[2]/div[1]/a").text

            players_club_nation = tds[1].find_element(By.XPATH, "div[2]/div[2]/span").find_elements(By.TAG_NAME, "a")
            player['team'] = players_club_nation[0].get_attribute('data-original-title')
            player['nation'] = players_club_nation[1].get_attribute('data-original-title')
            player['league'] = players_club_nation[2].get_attribute('data-original-title')
            player['specific_position'] = tds[3].find_element(By.TAG_NAME, "div").text
            player['skills'] = tds[6].text
            player['weak_foot'] = tds[7].text
            player['work_rate'] = tds[8].text

            player['pace'] = tds[9].find_element(By.TAG_NAME, "span").text
            player['shooting'] = tds[10].find_element(By.TAG_NAME, "span").text
            player['passing'] = tds[11].find_element(By.TAG_NAME, "span").text
            player['dribbling'] = tds[12].find_element(By.TAG_NAME, "span").text
            player['defending'] = tds[13].find_element(By.TAG_NAME, "span").text
            player['physical'] = tds[14].find_element(By.TAG_NAME, "span").text
            
            # player_img_url = tds[1].find(
            # 'img', {"class": "player_img"})['src']
        
            # if('notfound_player' not in player_img_url):
            #     file_path = save_image(player_img_url, 'players', f"{player['name'].replace(' ', '')}_{player['id']}.jpg")
            #     player['image_path'] = file_path
            # else:
            #     cont += 2
            #     continue

            players.append(player)


        # page_soup = soup(htmlContent, "html.parser")

        # table = page_soup.find("table")
        # trList = table.findAll("tr")[1+cont:1+cont+2]

        # # Basic Info
        # player = {
        #     'position': positions[-1]['id']
        # }

        # tds = trList[0].findAll("td")
        # player['id'] = tds[0].find(
        #     'div', {"class": "igs-btn"})['data-playerid']

        # try:
        #     other_player = next(filter(lambda x: x.id == player['id'], players))
        #     cont += 2
        #     continue
        # except:
        #     pass

        # team = (tds[1].findAll(
        #     'img', {"class": "team-img"})[0]['data-original-title']).strip()
        # nation = (tds[1].findAll(
        #     'img', {"class": "team-img"})[1]['data-original-title']).strip()
        # team_img = tds[1].findAll(
        #     'img', {"class": "team-img"})[0]['src']
        # nation_img = tds[1].findAll(
        #     'img', {"class": "team-img"})[1]['src']
        
        # try:
        #     team_obj = next(filter(lambda x: x['name'] == team, teams))
        # except StopIteration:
        #     if('notfound' not in team_img):
        #         file_path = save_image(team_img, 'teams', f"{team.replace(' ', '')}.jpg")
        #         team_img = file_path
                
        #     teams.append({
        #         'id': len(teams) + 1,
        #         'name': team,
        #         'image_path': team_img
        #     })
            
        #     team_obj = teams[-1]
            
        # player['team_origin'] = team_obj['id']
            
        # try:
        #     nation_obj = next(filter(lambda x: x['name'] == nation, nations))
        # except StopIteration:
        #     if('notfound' not in nation_img):
        #         file_path = save_image(nation_img, 'nations', f"{nation.replace(' ', '')}.jpg")
        #         nation_img = file_path
                
        #     nations.append({
        #         'id': len(nations) + 1,
        #         'name': nation,
        #         'image_path': nation_img
        #     })
            
        #     nation_obj = nations[-1]
            
        # player['nation'] = nation_obj['id']

        # player['specific_position'] = ''.join(tds[1].find(
        #     'div', {"class": "player-position-cln"}).findAll(text=True)).split(',')[0].split('|')[0].strip()
        # stats = trList[1].find(
        #     "div", {"class": "player-stats"}).findAll("div", {"class": "col-md-2"})
        # player['name'] = (''.join(tds[1].find(
        #     'div', {"class": "player-name"}).find("a").findAll(text=True))).strip()

        # player_img_url = tds[1].find(
        #     'img', {"class": "player-img-info"})['src']
        
        # if('notfound_player' not in player_img_url):
        #     file_path = save_image(player_img_url, 'players', f"{player['name'].replace(' ', '')}_{player['id']}.jpg")
        #     player['image_path'] = file_path
        # else:
        #     cont += 2
        #     continue
            
        # player['overall'] = ''.join(tds[2].find(
        #     'div', {"class": "player-overall"}).findAll(text=True))
        # player['pace'] = ''.join(stats[0].find(
        #     "div", {"class": "main-stat-rating-title"}).findAll(text=True))
        # player['shooting'] = ''.join(stats[1].find(
        #     "div", {"class": "main-stat-rating-title"}).findAll(text=True))
        # player['passing'] = ''.join(stats[2].find(
        #     "div", {"class": "main-stat-rating-title"}).findAll(text=True))
        # player['dribbling'] = ''.join(stats[3].find(
        #     "div", {"class": "main-stat-rating-title"}).findAll(text=True))
        # player['defending'] = ''.join(stats[4].find(
        #     "div", {"class": "main-stat-rating-title"}).findAll(text=True))
        # player['physical'] = ''.join(stats[5].find(
        #     "div", {"class": "main-stat-rating-title"}).findAll(text=True))

        # players.append(player)

        # cont += 2

driver.quit()

print('players', players)

def save_list_to_json(asset_list, file_path):
    with open(file_path, 'w') as f:
        json.dump(asset_list, f)

directory = 'dist'

if not os.path.exists(directory):
    os.makedirs(directory)
    
save_list_to_json(positions, f'{directory}/positions.json')
save_list_to_json(players, f'{directory}/players.json')
save_list_to_json(nations, f'{directory}/nations.json')
save_list_to_json(teams, f'{directory}/teams.json')