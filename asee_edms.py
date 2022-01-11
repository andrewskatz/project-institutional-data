# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:47:25 2020

@author: akatz4

Collect info from ASEE EDMS



"""



import requests
from bs4 import BeautifulSoup as bs
import os
#import re
import pandas as pd
#import pickle
#import itertools
#import numpy as np
from time import sleep
#from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

import shutil


os.getcwd()
proj_wd = "G:/My Drive/AK Faculty/Research/Projects/project political economy of engineering education/project institutional data"
os.chdir(proj_wd)
os.getcwd()
os.listdir()




#### use selenium and chrome webdriver to get all the links for the zip files
# from ipeds database - the big hurdle was getting past the "continue" button which
# doesn't change the url in order to get the html

url = "http://edms.asee.org/session/new"

#driver_path = "C:\\Users\\akatz4\\AppData\\Local\\Continuum\\anaconda3\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver_win32\\chromedriver.exe"
#driver = webdriver.Chrome(driver_path)



download_dir = "G:\\My Drive\\AK Faculty\\Research\\Projects\\project political economy of engineering education\\project institutional data\\edms_downloads"
print(download_dir)
os.chdir(download_dir)
os.listdir()


options = webdriver.ChromeOptions()

# profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
#                "download.default_directory": download_dir , 
#                "download.extensions_to_open": "applications/pdf",
#                "download.prompt_for_download": False,
#                "plugins.always_open_pdf_externally": True}

profile = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", profile)


driver_path = "C:\\Users\\akatz4\\AppData\\Local\\Continuum\\anaconda3\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(driver_path, options = options)


driver.get(url)

## NOTE: Need to manually log in and then click to "quick query"
driver.find_element_by_link_text("Quick query").click()

#driver.find_element_by_id("contentPlaceHolder_ibtnContinue").click()

#driver.find_element_by_class_name("close-notice close-this").click()
#driver.find_element_by_id("edit").click()



"""

Steps to click through quick query parts 1, 2, and 3

"""


#step 1, select the "sel_schools" SELECT element
select_report = Select(driver.find_element_by_id("report"))

#step 2, find the options available in the SELECT element - these should be the different universities
report_options = select_report.options

#step 3, find the visible text for each of the options in the SELECT element
report_option_labels = [option.text for option in report_options]

#step 4, confirm this is returning the correct list
print(report_option_labels)

# select the desired term
#select_report.select_by_visible_text(report_option_labels[5])


## Pick the discipline (need to also create options for department or degree for step 2)
select_discipline = Select(driver.find_element_by_id("select_query_discipline"))

discipline_options = select_discipline.options

discipline_option_labels = [option.text for option in discipline_options]

print(discipline_option_labels)

#select_discipline.select_by_visible_text(discipline_option_labels[4])



#pick the year in step three

select_year= Select(driver.find_element_by_id("select_query_year"))

year_options = select_year.options

year_option_labels = [option.text for option in year_options]

print(year_option_labels)

#select_year.select_by_visible_text(year_option_labels[4])


#step 5: select each of the school options
# for label in school_option_labels:
#     select.select_by_visible_text(label)
    

# click "Run Query"
driver.find_element_by_xpath("//input[@name='commit']").click() ## This worked!


#click the export to CSV option
driver.find_element_by_link_text("Download CSV").click()

# return back to quick query page
driver.find_element_by_link_text("Quick query").click()



# for term in term_options:
#     download_report()


"""

Loop to download each report for each discipline option for each year (1998-2018)

"""

download_dir = "G:/My Drive/AK Faculty/Research/Projects/project political economy of engineering education/project institutional data/edms_downloads"

# set download file name
dl_name = report + " " + discipline + " " + year + '.csv'

# change downloaded file name from the default name to a new name
filename = max([download_dir + "\\" + f for f in os.listdir(download_dir)], key=os.path.getctime)
shutil.move(filename, os.path.join(download_dir, dl_name))


# create a dictionary to track which reports are downloaded and whether it was successful
download_dictionary = {'report': [],
                       'discipline': [],
                       'year': [],
                       'dl_new_name': [],
                       'status': []}

query_url = "http://edms.asee.org/queries/quick"
driver.get(query_url)
print(report_option_labels[20])

# loop through reports, disciplines, and years
for report in report_option_labels[20:]:
    for discipline in discipline_option_labels[23:]:
        for year in year_option_labels:
                       
            report_name = report.replace(':', '---')
            report_name = report_name.replace('/', '--')
            discipline_name = discipline.replace('/', '--')
            
            dl_new_name = report_name + "_" + discipline_name + "_" + year + '.csv'
            print(dl_new_name)
            
            driver.get(query_url)
            
            try:
                select_report = Select(driver.find_element_by_id("report"))
                select_report.select_by_visible_text(report)
                
                select_discipline = Select(driver.find_element_by_id("select_query_discipline"))
                select_discipline.select_by_visible_text(discipline)
                
                select_year= Select(driver.find_element_by_id("select_query_year"))
                select_year.select_by_visible_text(year)
                
                sleep(2)
                
                # click "Run Query"
                driver.find_element_by_xpath("//input[@name='commit']").click() ## This worked!
                
                sleep(2)
                
                #click the export to CSV option
                driver.find_element_by_link_text("Download CSV").click()
                
                sleep(2)
    
                # change name of file in the download directory
                filename = max([download_dir + "\\" + f for f in os.listdir(download_dir)], key=os.path.getctime)
                shutil.move(filename, os.path.join(download_dir, dl_new_name))
                
                sleep(2)
                
                # return back to quick query page
                #driver.find_element_by_link_text("Quick query").click()
                
                #alternative method for returning to query page
                
                # driver.get(query_url)
                
                sleep(4)
                
                download_dictionary['report'].append(report)
                download_dictionary['discipline'].append(discipline)
                download_dictionary['year'].append(year)
                download_dictionary['dl_new_name'].append(dl_new_name)
                download_dictionary['status'].append("success")

            except:
                download_dictionary['report'].append(report)
                download_dictionary['discipline'].append(discipline)
                download_dictionary['year'].append(year)
                download_dictionary['dl_new_name'].append(dl_new_name)
                download_dictionary['status'].append("failure")                    
            
            

driver.close()



download_df = pd.DataFrame(download_dictionary)
download_df


proj_wd = "G:/My Drive/AK Faculty/Research/Projects/project political economy of engineering education/project institutional data"

os.chdir(proj_wd)
os.getcwd()
os.listdir()


download_df.to_csv("download_df_2.csv", index = False)




driver.get(url)
def download_report(term):
    driver.get(url)
    sleep(3)
    
    #select the appropriate term
    select = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlTerm"))
    select.select_by_visible_text(term)
    sleep(3)
    
    # click the submit button
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_Submit").click()

    #click the drop down menu to export
    clickExport = driver.find_element_by_id("ctl00_ContentPlaceHolder1_ReportViewer_ctl05_ctl04_ctl00_ButtonLink").click()

    #click the export to CSV option
    clickCSV = driver.find_element_by_link_text("CSV (comma delimited)").click()
    
    sleep(3)
    
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_showSelection").click()
    
    sleep(4)

driver.get(url)
     
 #click "show selections"   
driver.find_element_by_id("ctl00_ContentPlaceHolder1_showSelection").click()
    
    
    
driver.close()





#process the downloaded files
data_wd = "C:\\Users\\akatz4\\Desktop\\ak_misc\\projects\\project_institutional_data\\data"
os.chdir(data_wd)
os.listdir(data_wd)

i = 5
print()


#checking to make sure the code works as expected
grade_df = pd.read_csv('grade_distribution (1).csv')
grade_df['term'] = 'summerII_2019'


#opening each of the "grade_distribution (#).csv" files, adding a column for the
# correct term and then saving it with the term in the file name
for i, file in enumerate(os.listdir(data_wd)):
    print(file+term_option_labels[i+1])
    grade_data = pd.read_csv(file)
    grade_data['term'] = term_option_labels[i+1]
    
    filename = 'grade_distribution_' + term_option_labels[i+1] + '.csv'
    grade_data.to_csv(filename)
    



for i, file in enumerate(os.listdir(data_wd)):
    print(i, file)
    if i == 0:
        df_combined = pd.read_csv(file)
    else:
        new_df = pd.read_csv(file)
        df_combined = df_combined.append(new_df)
    
df_combined.shape #109943 x 16

#check to make sure correct number of rows (109943)
row_count = 0
for i, file in enumerate(os.listdir(data_wd)):
    print(i, file)
    df = pd.read_csv(file)
    row_count += df.shape[0]



#write the combined dataframe to a csv
df_combined.to_csv('combined_grades_2003to2019.csv', index = False)



