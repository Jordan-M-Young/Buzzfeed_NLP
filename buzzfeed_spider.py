# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:45:54 2020

@author: jmyou
"""


import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os


def get_related_urls(page,collected_urls):
    

    """This function searches the page for related articles and grabs their
    urls"""
    try:
        soup = BeautifulSoup(page,'html.parser')
        
        ls = list(soup.find_all('a',class_="stacked__2HXQGZ37eK recircItemLink__3DkqDpHOOg"))
        
        for l in ls:
            l = str(l).split('href="')[1].split('">')[0]
            if l not in collected_urls:
                print(l)
                collected_urls.append(l)
    except AttributeError:
        print('error')
    
    return collected_urls



def get_main_page_urls(url,collected_urls):
    """gets the urls for the articles on the buzzfeed homepage"""

    for i in range(1,5):
        print(i)
        url = url + '?page=' + str(i)
        
        
        
        page = requests.get(url)
        print(str(page.status_code) + '\n-----')
        
        #Navigates the page
        soup = BeautifulSoup(page.content,'html.parser')
        x = list(soup.find_all('a'))
        
        urls = []
        for i in range(121,len(x)-1):
            z = str(x[i]).split('href=')
            z2 = z2 = [p.split('>')[0].replace('"','') for p in z if '"https' == p[0:6]] 
            for el in z2:
                urls.append(el)
                if el not in collected_urls:
                    collected_urls.append(el)
        
        
        if not urls:
            break
        
        
    return collected_urls




def run_spider(url_num=None,collected_url_file=None,checked_urls_file=None):
    """calling this function will run the buzzfeed url spider"""
    

    #loads collected url file
    if collected_url_file == None:
        collected_url_file = '/Buzzfeed_NLP/some_collected_urls.csv'
        
    if checked_urls_file == None:
        checked_urls_file = '/Buzzfeed_NLP/some_checked_urls.csv'

    if url_num == None:
        url_num = 800
    
    
    #checks to see if the collected url file exists
    if os.path.exists(collected_url_file):
        collected_urls = list(pd.read_csv(collected_url_file).iloc[:,1])
    
    #checks to see if the checked urls file exists
    if os.path.exists(checked_urls_file):
        checked_urls = list(pd.read_csv(checked_urls_file).iloc[:,1])
    
    
    #loads the webdriver
    driver = webdriver.Chrome('/Buzzfeed_NLP/chromedriver.exe')
    collected_urls = get_main_page_urls('https://www.buzzfeed.com/tvandmovies',
                                        collected_urls)
    
    
    count = 0
    i = 0
    
    #Runs spider main loop
    while count < url_num:
        try:
            #checks to see if current url has been checked
            if collected_urls[i] in checked_urls:
                i += 1
                continue
            
            #if url hasn't been checked
            else:
                #grabs related urls from page 
                driver.get(collected_urls[i])
                html = driver.page_source
                collected_urls = get_related_urls(html,collected_urls)
                checked_urls.append(collected_urls[i])
                print('-------','(' + str(count) + ' / ' + str(url_num) + ')' )
                time.sleep(4)
                count += 1
                i += 1
                
        #allows you to terminate spider early if you dont want to wait for it
        #to finish
        except KeyboardInterrupt:
            print('\n----Terminated Early----')
            break
    
    #saves downloaded urls
    print('-------Data  Saved------')
    checked_urls = pd.DataFrame(checked_urls)
    collected_urls = pd.DataFrame(collected_urls)
    
    checked_urls.to_csv(checked_urls_file)
    collected_urls.to_csv(collected_url_file)