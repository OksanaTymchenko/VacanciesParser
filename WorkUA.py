from bs4 import BeautifulSoup
import requests
import os
import sys
import re
import pandas as pd
import numpy as np

# url = 'https://www.work.ua/stat/count/category=0&?time=year2019&quantity=1'

def GetParser(url):
	response = requests.get(url)
	return BeautifulSoup(response.content, 'html.parser')

def Vacancies_per_Category(url):
	ind = url.index('0')
	soup = GetParser(url)
	categories = soup.find(id="category")
	for c in categories.find_all("option"):
		cat_url = url[:ind] + c['value'] + url[ind+1:]
		category = {'url': cat_url, 'name': c.string}
		yield category

def GetMonth(soup):
	months = []
	mlist = soup.find_all(class_="col-sm-8")
	for m in mlist[1:]:
		months.append(m.string)
	return months

def GetVacancyNum(category):
	soup = GetParser(category['url'])
	rows = soup.find_all(class_='row')
	nlist = []
	for r in rows[1:13]:
		n_vacancies = r.find(class_="col-sm-2 text-right nowrap").b.string
		nlist.append(n_vacancies)
	return nlist

def CategoriesSaver(url):
	soup = GetParser(url)
	months = GetMonth(soup)
	print(months)
	names = []
	data = []
	Categories_df = pd.DataFrame()
	for cat in Vacancies_per_Category(url):
		names.append(cat['name'])
		data.append(GetVacancyNum(cat))
	print(len(data[0]))
	print(len(months))
	Categories_df = pd.DataFrame(np.array(data).T, index = months, columns = names)
	Categories_df.head()
	Categories_df.to_excel('test.xlsx', index=False)

if __name__ == "__main__":
    CategoriesSaver("https://www.work.ua/stat/count/?category=0&time=year2019&quantity=1")

