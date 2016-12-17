#!/usr/bin/env python
#coding: UTF-8

'''
当日のレース時刻をスクレイピングしておく
'''

from bs4 import BeautifulSoup
import urllib3 as ul
import pdb
from datetime import datetime
import os
import re

# 開催回数・場所・日目を数値に変換
def convert_kaisaidata(kai, place, day):
    kai = str(re.findall(r"\d", kai)[0]).zfill(2)
    day = str(re.findall(r"\d", day)[0]).zfill(2)
    place_index = { u"札幌":1, u"函館":2, u"福島":3, u"新潟":4, u"東京":5, u"中山":6, u"中京":7, u"京都":8, u"阪神":9, u"小倉":10 }
    place = str(place_index[place]).zfill(2)
    return kai, place, day


# シェルスクリプトを作成
def make_sh_file():
    # すでにファイルが存在している場合は削除
    if os.path.exists('make_cron.sh'):
        os.remove('make_cron.sh')

    with open('make_cron.sh', 'a') as f:
        f.write("a")


# 当日の全レース時刻を読み込んでおく
def confirm_race_time():
    url = "http://race.netkeiba.com/?pid=race_list"
    html = ul.PoolManager().urlopen("GET", url).data
    soup = BeautifulSoup(html)
    year = datetime.now().strftime('%Y')

    race_data = soup.find("div", class_="RaceList_Area").find("div", id="race_list_body").find_all("dl", class_="race_top_hold_list")
    for race_column in race_data:
        kaisai_data = race_column.find("p", class_="kaisaidata").string
        kai   = kaisai_data[:2]
        place = kaisai_data[2:4]
        day   = kaisai_data[4:]
        kai, place, day = convert_kaisaidata(kai, place, day)
        races = race_column.find("dd").find_all("div", class_="racedata")
        for i, race in enumerate(races):
            race_time = race.text.split(u"\xa0")[0].strip("\n")
            url = "http://race.netkeiba.com/?pid=race_old&id=c" + year + place + kai + day + str(i+1).zfill(2)
            print race_time, url


if __name__ == '__main__':
    confirm_race_time()
