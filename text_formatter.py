# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 09:31:53 2020

@author: jmyou
"""


import pandas as pd
import matplotlib.pyplot as plt
import json
import csv
import re
from sklearn.model_selection import train_test_split

def build_text_files(data_json,dest_dir):
    f = open(dest_dir,'w',encoding='Utf-8')
    data = ''
    count = 0
    for texts in data_json:
        print(count)
        count += 1
        summary = str(texts).strip()
        summary = re.sub(r"\s", " ", summary)
        data += summary + "  "
    
    f.write(data)

    return data


data = pd.read_csv('Article_Data.csv')

articles = data[data['Page_Type'] == 'Article']


save_path = 'Article_json_paths.csv'




art_paths = list(articles.loc[:,'json_filename'])
art_titles = list(articles.loc[:,'Title'])
art_descript = list(articles.loc[:,'Description'])
texts = []
text_data = []
for i in range(len(art_paths)):
    article_data = []
    
    article_data = [art_paths[i],art_titles[i],art_descript[i]]

    
    
    raw_text = ""
    structured_text = ""
    full_article = ""
    
    
    with open(art_paths[i]) as f:
      j_data = json.load(f)
      for key,val in j_data.items():
          if val['Title']:
              # raw_text += val['Title'].replace('\n',' ') + ' '
              
              if key == '0':
                  # structured_text += val['Title'].replace('\n',' ') + '\n'
                  full_article += val['Title'].replace('\n',' ') + '\n'
              else:
                  
                  # structured_text += '\n' + val['Title'].replace('\n',' ') + '\n'
                  full_article += '\n' + val['Title'].replace('\n',' ') + '\n'
                  
          if val['Media_Type']: 
              full_article += '\n[' + val['Media_Type'] + ']\n'
              # print('\n[' + val['Media_Type'] + ']\n')
          if val['Text']:
              # raw_text += val['Text'].strip().replace('\n','') + ' '
              # structured_text += '\n' + val['Text'].strip().replace('\n','') + '\n'
              full_article += '\n' + val['Text'].strip().replace('\n','') + '\n'
              # print(val['Text'].strip().replace('\n','') + '\n')
    
    
    article_data.append(full_article)
    
    text_data.append(article_data)
    
    # print('-----(' + str(i+1) + '/' + str(len(art_paths)) + ')')



data = [str('\n'.join(['\n'.join([str(t[1]),str(t[2])]),str(t[3])])) for t in text_data]
title_train,title_test = train_test_split(art_titles,test_size=0.15)
art_train, art_test = train_test_split(data,test_size=0.15)

tr_t = build_text_files(title_train,'title_train_dataset.txt')
ts_t = build_text_files(title_test,'title_test_dataset.txt')
tr_art = build_text_files(art_train,'art_train_dataset.txt')
ts_art = build_text_files(art_test,'art_test_dataset.txt')



