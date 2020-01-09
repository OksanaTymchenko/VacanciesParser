from bs4 import BeautifulSoup
import requests
import os
import sys
import re
import pandas as pd
import numpy as np
import json

response = requests.get('https://api.hh.ru/areas?host=hh.ua&locale=UA')
ukr_areas = response.json()[0]
id_exp = "\"id\"\:\s?\"(\d+)\""
s = json.dumps(ukr_areas)
res = re.findall(id_exp, s)

def get_categories():
	response = requests.get('https://api.hh.ru/specializations?locale=UA&host=hh.ua')
	categories_json = response.json()
	categories_list = []
	for c in categories_json:
		del c["specializations"]
		yield c
	# yield category
# clist = [int(c['id']) for c in categories]

url = 'https://api.hh.ru/vacancies/?host=hh.ua&locale=UA&date_from=2019-01-01'



	
