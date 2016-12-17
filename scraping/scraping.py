#!/usr/bin/env python
#coding: UTF-8

'''
netkeibaから過去の競馬データをスクレイピングする
'''

from bs4 import BeautifulSoup
import urllib3 as ul
import pdb
import time
import itertools

# 1レース分のデータを取得
def get_race(url):
	html = ul.PoolManager().urlopen("GET", url).data
	soup = BeautifulSoup(html)
	try:
		print soup.find("div", class_="mainrace_data").find("p", class_="smalltxt").string
	except:
		print "ページが存在しません"


# 1頭分の馬データを取得
def get_horse(url):
	print "a"


# 過去のレースデータを取得
def scraping_races():
	root_url = "http://db.netkeiba.com/race/"
	years  = [str(i) for i in range(2011, 2016)]
	places = [str(i).zfill(2) for i in range(1, 11)]   # 1:札幌, 2:函館, 3:福島, 4:新潟, 5:東京, 6:中山, 7:中京, 8:京都, 9:阪神, 10:小倉
	times  = [str(i).zfill(2) for i in range(1, 7)]
	days   = [str(i).zfill(2) for i in range(1, 13)]
	races  = [str(i).zfill(2) for i in range(1, 13)]

	for year, place, t, day, race in itertools.product(years, places, times, days, races):
		url = root_url + year + place + t + day + race
		get_race(url)
		time.sleep(1)


if __name__ == '__main__':
	scraping_races()
