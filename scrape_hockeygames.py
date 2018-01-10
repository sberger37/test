from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import csv
import pandas as pd
import numpy as np

# Tell python where chrome driver path is.
chrome_path = r"C:\Users\Scott\Downloads\chromedriver_win32\chromedriver.exe"
# Set driver to path.
driver = webdriver.Chrome(chrome_path)

# Open website
driver.get('http://www.naturalstattrick.com/games.php')

# Select options in dropdown

# Select which season to pull
mySelect = Select(driver.find_element_by_name('season'))
# Values are 'yyyyyyyy'
mySelect.select_by_value('20172018')

# Select pre-season, regular season or playoffs data.
mySelect = Select(driver.find_element_by_name('stype'))
# Values are: '1' (Pre-Season), '2' (Regular Season), '3' (Playoffs)
mySelect.select_by_value('2')

# Select which situations to pull.
mySelect = Select(driver.find_element_by_name('sit'))
# Values are 'all' (All Strengths), 'ev' (Even Strength), '5v5' (5 on 5), 'sva' (5v5 Score & Venue Adjusted), 'pp' (Power Play), 'pk' (Penalty Kill)
mySelect.select_by_value('sva')

# Select teams to pull
mySelect = Select(driver.find_element_by_name('team'))
# Values are 'All' (All Teams) and each teams 3 letter id
mySelect.select_by_value('All')

# Select whether stats are raw or /60
mySelect = Select(driver.find_element_by_name('rate'))
# Values are 'y' (Yes), 'n' (No)
mySelect.select_by_value('y')

# Submit selections
driver.find_element_by_xpath("""/html/body/div/div[5]/div[1]/form/input""").click()

# Send updated page to source variable
source = driver.page_source

# Send source to BeautifulSoup package
soup = BeautifulSoup(source, 'lxml')

# Find table on page
table = soup.find('tbody')

header_titles = ['Date', 'Team', 'TOI', 'CF','CA','CF%','FF','FA','FF%','SF','SA','SF%', 'GF','GA','GF%','SCF','SCA','SCF%','HDCF','HDCA','HDCF%','HDGF','HDGA','HDGF%','HDSH%','HDSV%','SH%','SV%','PDO']


fullScrape = []

# Find all rows
for row in table.find_all('tr'):
    date = row.find_all('td')[0].a.text[:10]
    team = row.find_all('td')[1].text
    cf = row.find_all('td')[3].text
    ca = row.find_all('td')[4].text
    ff = row.find_all('td')[6].text
    fa = row.find_all('td')[7].text
    scf = row.find_all('td')[15].text
    sca = row.find_all('td')[16].text
    hdcf = row.find_all('td')[18].text
    hdca = row.find_all('td')[19].text
    fullScrape.append((date, team,cf,ca,ff,fa,scf,sca,hdcf,hdca))


fullScrape = pd.DataFrame(fullScrape, columns=('Date', 'Team', 'CF', 'CA', 'FF', 'FA','SCF','SCA','HDCF','HDCA'))


print(fullScrape)

fullScrape.to_csv('nhl.csv')


driver.close()

