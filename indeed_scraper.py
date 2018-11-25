# coding: utf-8
# Trying to update the Webscraping Indeed Notebook to Python 3
# API Calls
import requests
# Parse HTML
import bs4
# Handle Dataframes (excel data)
import pandas as pd
# Better Math functions
import numpy as np
# Plotting library
# import matplotlib as plt
# Time library to create timestamps for filenames
import time
# Creating Folders
import os

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

# ### Query Params in Indeed URL
# - q= refers to the query, usually the job title and salary you want
# - l= refers to the location, usually the city or state
# - start= refers to the result number you are at. i.e., start=10, you are viewing results 11-20.

# URL Format for Indeed Search
INDEED_URL_TEMPLATE = "http://www.indeed.com/jobs?q={}&l={}&start={}"

# Functions to extract specific pieces of data from the html of a indeed search page.
def extract_location(posting, null_value=None):
    try:
        return posting.find('div', {'class': 'location'}).text
    except:
        return null_value

def extract_company(posting, null_value=None):
    try:
        return posting.find('span', {'class':'company'}).text
    except:
        return null_value

def extract_job_title(posting, null_value=None):
    try:
        return posting.find('a', attrs = {'data-tn-element':'jobTitle'}).text
    except:
        return null_value
    
def extract_salary(posting, null_value=None):
    try:
        return posting.find(name="span", attrs={"class":"no-wrap"}).text
    except:
        return null_value

def extract_summary(posting, null_value=None):
    summaries=""
    try:
        spans = posting.findAll('span', attrs={'class': 'summary'})
        for span in spans:
            summaries += span.text.strip()
        return summaries
    except:
        return null_value

def extract_url(posting, null_value=None):
    try:
        return posting.get('data-jk')
    except:
        return null_value

def search_indeed(query, cities, max_results_per_city, null_value=None):
    df = pd.DataFrame()
    for city in cities:
        for start in range(0, max_results_per_city, 10):
            url = INDEED_URL_TEMPLATE.format(query,city,start)
            html = requests.get(url).text
            soups = bs4.BeautifulSoup(html, "html.parser")
            rows = soups.find_all('div', attrs = {'class':'row'})
            for posting in rows:
                df = df.append({
                    "location": extract_location(posting, city),
                    "company": extract_company(posting, null_value),
                    "job_title": extract_job_title(posting, null_value),
                    "salary": extract_salary(posting, null_value),
                    "url": extract_url(posting, null_value)
                }, ignore_index=True)
    return df

def clean_data(df):
    # dropping duplicates
    df_copy = df.drop_duplicates()
    # getting rid of newlines in company
    df_copy.company.replace(regex=True,inplace=True,to_replace=["\n", "\r"],value="")
    # getting rid of $ in salary
    df_copy.salary.replace(regex=True, inplace=True, to_replace=["\n", "\r", "\$"], value="")
    df_copy.loc[:, 'url'] = "https://www.indeed.com/viewjob?jk=" + df_copy.loc[:, 'url']
    df_copy.reset_index(drop=True, inplace=True)
    return df_copy

def save_data(df, query):
    timestr = time.strftime("%Y_%m_%d-%H%M%S")
    filename = f"{query}-{timestr}"
    df.to_csv(f"{filename}.csv" , sep=',', encoding='utf-8')
    return filename

# Code to get all descriptions from urls and append filenames to desc column
# Getting one posting worth of data
# url = data.loc[:, 'url'].values[0]
# html = requests.get(url).text
# soups = bs4.BeautifulSoup(html, "html.parser")

# # Print out job description as one srting
# main_content = soups.find('div', {'class': "jobsearch-JobComponent icl-u-xs-mt--sm jobsearch-JobComponent-bottomDivider"})
# job_description = soups.find('div', {'class': "jobsearch-JobComponent-description icl-u-xs-mt--md"})
# print(job_description.get_text("  ", strip=True).strip())
def posting_scraper(data, filename):
    x,y = data.shape
    desc_df = pd.DataFrame()
    dir_path = f'./{filename}/'
    create_folder(dir_path)
    for i in range(x):
        url = data.iloc[i]['url']
        html = requests.get(url).text
        soups = bs4.BeautifulSoup(html, "html.parser")
        job_description = soups.find('div', {'class': "jobsearch-JobComponent-description icl-u-xs-mt--md"})
        description = job_description.get_text("  ", strip=True).strip()
        desc_filename = f'{dir_path}{filename}_{i}.txt'
        with open(desc_filename, 'w', encoding='utf-8') as the_file:
            the_file.write(description)
        desc_df.at[i, 'desc'] = desc_filename
    return desc_df
