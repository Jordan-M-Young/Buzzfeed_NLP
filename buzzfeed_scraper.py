# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 14:07:26 2020

@author: jmyou
"""

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import hashlib
import os


def get_reactions(soup):
    """Gets the numbers of the allowed reactions on the article"""
    
    reactions = soup.find_all('li',class_='reaction__3UIWmmjH6i')
    reaction_count = []
    reaction_type = []
    for r in reactions:
        q = r.find('span',class_='label__TzBvZAAyDP').text
        
        if q:
            reaction_type.append(q)
        else:
            q = str(r.find('img')).split('alt="')[1].split('"')[0].upper()
            reaction_type.append(q)
            
        try:
            r_c = r.find('span',class_='count__3wZo7oEMVq').text
        except AttributeError:
            r_c = 0
        
        reaction_count.append(r_c)
    
    love_ct = 0
    fail_ct = 0
    lol_ct = 0
    cute_ct = 0
    omg_ct = 0
    win_ct = 0
    wtf_ct = 0
    h_brk_ct = 0
    
    
    try:
        for r in reaction_type:
            if r.upper() == 'LOVE':
                love_ct = int(reaction_count[reaction_type.index(r)])
            elif r.upper() == 'FAIL':
                fail_ct = int(reaction_count[reaction_type.index(r)])
            elif r.upper() == 'LOL':
                lol_ct = int(reaction_count[reaction_type.index(r)])
            elif r.upper() == 'CUTE':
                cute_ct = int(reaction_count[reaction_type.index(r)])
            elif r.upper() == 'OMG':
                omg_ct = int(reaction_count[reaction_type.index(r)])
            elif r.upper() == 'WIN':
                win_ct = int(reaction_count[reaction_type.index(r)])
            elif r.upper() == 'WTF':
                wtf_ct = int(reaction_count[reaction_type.index(r)])
            else:
                h_brk_ct = int(reaction_count[reaction_type.index(r)])
    except ValueError:
        print('Reactions Error:',r,reaction_type)
    except UnboundLocalError:
        print('Reactions Error:',reaction_type)
    
    reactions = [love_ct, fail_ct, lol_ct, cute_ct, omg_ct, win_ct, wtf_ct, 
                 h_brk_ct]
    
    return reactions

def get_subbuzzes_news(soup,title,url):
    """Gets the types of media in each subbuzz of buzzfeed news articles"""
    
    buzz ={}
    im_num = 0
    gif_num = 0
    twt_num = 0
    tik_num = 0
    rdt_num = 0
    inst_num = 0
    yt_num = 0
    tb_num = 0
    
    c1 = 'subbuzz subbuzz-text xs-mb4 xs-relative'
    c2 = 'subbuzz subbuzz-image xs-mb4 xs-relative xs-mb1'
    
    buzzes = list(soup.find_all('div',class_=c1))
    buzz_media = list(soup.find_all('div',class_=c2))
    
    
    for i in range(len(buzzes)):
        sub_buzz = {}
        sub_buzz['Text'] = buzzes[i].text.strip() 
        buzz[str(i)] = sub_buzz
    
    for j in range(len(buzz_media)):
        sub_buzz = {}
        subbuz_media = str(buzz_media[1]).split('src="')[1].split('"')[0]
        sub_buzz['Media'] = subbuz_media
        buzz[str(i+j+1)] = sub_buzz
        im_num += 1

    nums = [im_num, tik_num, twt_num, gif_num, rdt_num, inst_num, yt_num, 
        tb_num]
    
    
    return buzz, nums


def get_subbuzzes(soup,title,url):
    """Gets the types of media in each subbuzz of regular buzzfeed articles"""
    
    buzz = {}
    im_num = 0
    gif_num = 0
    twt_num = 0
    tik_num = 0
    rdt_num = 0
    inst_num = 0
    yt_num = 0
    tb_num = 0
    
    buzzes = list(soup.find_all('div',class_="js-subbuzz-wrapper"))
    
    for i in range(len(buzzes)):
        try:
            
            #Dictionary containing pertinent subbuzz information
            sub_buzz = {}
            
            
            #Gets the number of the subbuzz if it exists
            try:
                sbz_number = buzzes[i].find('span').text
            except AttributeError:
                sbz_number = None
            
            
            #Gets the subbuzz text if it exists
            try:
                sbz_title = buzzes[i].find('h2',class_='subbuzz__title xs-mb1 bold')
                sbz_title_text = str(sbz_title.text).strip()
            except AttributeError:
                sbz_title_text = None
            
            
            
            #Gets subbuzz media information if media exists
            sbz_media = buzzes[i].find('blockquote')
            if not sbz_media:
                sbz_media = buzzes[i].find('figure')
                
            if 'subbuzz-tweet' in str(sbz_media):
                media_type = 'Tweet'
                twt_num += 1
                
            elif 'tiktok-embed' in str(sbz_media):
                media_type = 'Tiktok'
                tik_num += 1
                
            elif 'instagram' in str(sbz_media):
                media_type = 'Instagram'
                inst_num += 1
            
                
            elif 'youtube' in str(sbz_media):
                media_type = 'Youtube'
                yt_num += 1
            
            elif 'tumblr' in str(sbz_media):
                media_type = 'Tumblr'
                tb_num += 1
                
            elif 'subbuzz__media' in str(sbz_media):
                if 'data-type="image-gif"' in str(sbz_media):
                    media_type = 'gif'
                    gif_num += 1
                    
                else:
                    media_type = 'Image'
                    im_num += 1
                    
            elif 'reddit' in str(sbz_media):
                media_type = 'Reddit_Post'
                rdt_num += 1
            
            
            
            else:
                media_type = None        
            

            #Gets media caption if it exists
            try:
                sbz_text = buzzes[i].find('figcaption',class_='subbuzz__caption').text
                sbz_text.strip()
                if len(sbz_text) == 1:
                    sbz_text = None
                    
            except AttributeError:
                try:
                    sbz_text = buzzes[i].find('p').text
                except AttributeError:
                    sbz_text = None
        
            
        
            #Gets Tweet Data if it exists
            if media_type == 'Tweet':
                tweet_txt = buzzes[i].find('figure').text.strip()
                tweet_info = buzzes[i].find('figure').find_all('a')
                tweet_info = [str(t) for t in tweet_info]
                sub_buzz['Tweet_Data'] = [tweet_txt,tweet_info]
            
            else:
                sub_buzz['Tweet_Data'] = [None,None]
                
                
            
            #Gets Tiktok Data if it exists 
            if media_type == 'Tiktok':
                tik_data = str(sbz_media)
                sub_buzz['Tik_Data'] = tik_data.split('cite="')[1].split('"')[0]
                
            else:
                sub_buzz['Tik_Data'] = None
            
            
            #Gets instagram Data if it exists
            if media_type == 'Instagram':
                inst_data = str(sbz_media)
                inst_data = inst_data.split('src="')[1].split('"')[0]
                sub_buzz['Instagram_Data'] = inst_data
            else:
                sub_buzz['Instagram_Data'] = None
            
            
            if media_type == 'Youtube':
                yt_data = str(sbz_media)
                yt_data = yt_data.split('src="')[1].split('?')[0]
                sub_buzz['Youtube_Data'] = yt_data
            else:
                sub_buzz['Youtube_Data'] = None
            
            #Gets Reddit Post Data if it exists
            if media_type == 'Reddit_Post':
                rdt_data = str(sbz_media)
                rdt_data = rdt_data.split('href="')[1].split('?')[0]
                sub_buzz['Reddit_Data'] = rdt_data
            
            else:
                sub_buzz['Reddit_Data'] = None
            
            if media_type == 'Tumblr':
                tb_data = sbz_media.find_all('a',class_='photoset_photo')
                tb_data = [str(d).split('href="')[1].split('"')[0] for d in tb_data]
                sub_buzz['Tumblr'] = tb_data
            else:
                sub_buzz['Tumblr'] = None
                
            #Gets image data if it exists
            if media_type == 'Image':
                try:
                    im_url = (str(sbz_media.find('img')).split('src="')[1].split('">')[0])
                    sub_buzz['Image_Url'] = im_url
                except IndexError:
                    print('Image Collection Error:','\n',
                          'Title: ',title,'\n',
                          'Url: ',url,'\n',
                          'Image: ',i,'\n',
                          'Html: ',sbz_media.find('img'),'\n')
                    
                    sub_buzz['Image_Url'] = None
            else:
                sub_buzz['Image_Url'] = None
    
            #Gets gif data if it exists
            if media_type == 'gif':
                gif_url = str(sbz_media).split('src="')[1].split('?')[0]
                sub_buzz['Gif_Url'] = gif_url
            else:
                sub_buzz['Gif_Url'] = None
            
            
            #Writes Data to subbuzz dictionary
            sub_buzz['Title'] = sbz_title_text
            sub_buzz['Number'] = sbz_number
            sub_buzz['Media_Type'] = media_type
            sub_buzz['Text'] = sbz_text
                
            
            #adds subbuzz dictionary to buzz dictionary
            buzz[str(i)] = sub_buzz
        
    
    
        except AttributeError:
           print(i)

    nums = [im_num, tik_num, twt_num, gif_num, rdt_num, inst_num, yt_num, 
            tb_num]
    
    return buzz, nums

def check_content(soup,title,url):
    """gets the content of the article"""
    
    if 'buzzfeednews' in url:
        buzz,nums = get_subbuzzes_news(soup,title,url)
    
    else:
        #article text
        buzz,nums = get_subbuzzes(soup,title,url)
        
    
    return buzz, nums
    
def check_trending_status(soup):
    """checks to see if the article is trending and gets view count if so"""
    
    trending_status = soup.find('div',class_='trendingText__1g3uLDFb1X')
    if trending_status:
        trending_count = trending_status.text
        trending_count = trending_count.split('Trending')[1].split(' ')[0]
        trending_count = int(trending_count.replace(',',''))
        trending_status = 'Trending'
        
    else:
        trending_status = None
        trending_count = None
        
    
    return trending_status,trending_count


def check_badges(soup):
    """Checks for article badges"""
    
    try:
        badges = soup.find('ul',class_='badgeList__1LHbcTIq2k')
        badges = badges.find_all('img')
        badges = [str(badge).split('alt="')[1].split('"')[0] for badge in badges]
        if 'Quiz badge' in badges:
            page_type = 'Quiz'
        else:
            page_type = 'Article'
    except AttributeError:
        page_type = 'News'
        
    
    return badges,page_type

def check_time(soup,url):
    """Gets the time/date the article was posted on"""
    
    try:
        date = soup.find('time').text
        date = date.split('Posted on ')[1]
    except IndexError:
        print(date)
        try: 
            date = date.split('Updated ')[1]
        except IndexError:
            try:
                print(date)
                date = date.split('Posted ')[1]
            except IndexError:
                print(date)
    
    except AttributeError:
        try:
            date = soup.find('p',class_='news-article-header__timestamps-posted').text
            date = date.split('Posted on ')[1].split(' at')[0]
        except IndexError:
            print('DateError',url)
            date = None
            
            
    return date

def check_author(soup,url):
    """Gets the author of the article"""
    
    try:
        headline = soup.find('a',class_='headlineByline__1xvw0GX5iL')
        author = soup.find('span',class_='metadata-link bylineName__8t-CbLgGCD').text
        author_role = headline.find('p').text
    
    except AttributeError:
        try: 
            headline = soup.find('div',class_='headline__2V6cg6yv2y')
            author = headline.find('span',class_='metadata-link').text
            author_role = None
        except AttributeError:
            c1 = 'news-byline-full__name xs-block link-initial--text-black'
            c2 = 'news-byline-full__role xs-text-5 xs-block'
            author = soup.find('span',class_=c1).text
            author_role = soup.find('span',class_=c2).text
            
    return author, author_role

def check_comments(soup):
    """Finds the number of posted comments in the article comment section"""
    
    try:
        n_comments = soup.find('span',class_='commentCount__2iANm').text
        n_comments = int(n_comments.split(' ')[0])
    except AttributeError:
        n_comments = None
    
    return n_comments

def check_likes(soup):
    """Gets the number of times the article was liked"""
    
    try:
        like_counts = soup.find_all('span',class_='likesCount__20vtX')
        max_likes = max([int(like_counts[i].text) for i in range(len(like_counts))])
    except ValueError:
            max_likes = 0
    
    return max_likes

def check_article_subject(soup):
    """Gets the article's subject"""
    
    try:
        article_class = soup.find('a',class_='metadata-link').text
    except AttributeError:
        c = 'link-initial--text-black link-hover--text-gray link-hover--underline-gray analyt-internal-link'
        article_class = str(soup.find('a',class_=c))
        article_class = article_class.split('item-name="')[1].split('"')[0]
    
    return article_class

def check_title(soup):
    """gets the article title"""
    
    try:
        title = soup.find('h1',class_="title__2wEoS_Bqpp").text
    except AttributeError:
        title = soup.find('h1',class_='news-article-header__title').text
        
    return title


def check_description(soup):
    """gets the article description"""
    
    try:
        description = soup.find('p',class_="description__1bzzdbaw8q").text
    except AttributeError:
        description = soup.find('p',class_='news-article-header__dek').text
        
    return description
    
def buzzfeed_scraper(driver,url,articles,h,path):
    """scrapes an article for pertinent data. Tabular data is added to the 
    articles list. Non tabular data is saved to a json file"""
    
    driver.get(url)
    time.sleep(2)
    page = driver.page_source
    
    
    #The beautiful soup; a parsed-html document
    soup = BeautifulSoup(page,'html.parser')
    
    #checks date on which the article was posted
    date = check_time(soup,url)
    
    
    #Badges
    badges,page_type = check_badges(soup)
    
    
    #Gets trending status and number of pageviews
    trending_status,trending_count = check_trending_status(soup)
    
        
    #Author Data Data
    author, author_role = check_author(soup,url)
        
    #Article subject
    article_sub = check_article_subject(soup)
        
    
    #number of comments
    n_comments = check_comments(soup)
    
    #reaction data
    rxns = get_reactions(soup) 
    love_ct, fail_ct, lol_ct, cute_ct, omg_ct, win_ct, wtf_ct, h_brk_ct = rxns
    
    #article title
    title = check_title(soup)
        
    #article description
    description = check_description(soup)
    
    #'Like' count on the most liked article comment
    max_likes = check_likes(soup)    
    
    #Gets media
    buzz, nums = check_content(soup,title,url)
    im_num, tik_num, twt_num, gif_num, rdt_num, inst_num, yt_num, tb_num = nums
    
    h.update(url.encode('utf-8'))
    hash_id = h.hexdigest()
    
    json_path = '/'.join([path,'json/'])
    json_file = ''.join([hash_id,'.json'])
    json_filename = ''.join([json_path,json_file])
    
     
    with open(json_filename,'w') as jf:
        json.dump(buzz,jf) 
        
    #compiles all data into one list
    article_data = [title,            #Article Title
                    description,      #Article Description
                    author,           #Author
                    author_role,      #Author role
                    date,             #Date published
                    article_sub,      #Article Subject
                    page_type,        #Webpage type (Quiz vs. Article)
                    trending_status,  #Article's trending status
                    trending_count,   #Trending page views
                    im_num,           #Number of Images used in article
                    tik_num,          #Number of Tiktok vids in article
                    twt_num,          #Number of Tweets used in article
                    gif_num,          #Number of Gifs used in article
                    rdt_num,          #Number of Reddit posts used in article
                    inst_num,         #Number of Instagram posts in article
                    yt_num,           #Number of Youtube vids used in article
                    tb_num,           #Number of Tumblr posts used in article
                    love_ct,          #Number of 'loves' article received
                    fail_ct,          #Number of 'fails' article received
                    lol_ct,           #Number of 'LOLs' article received
                    cute_ct,          #Number of 'cutes' article received
                    omg_ct,           #Number of OMGS article received
                    win_ct,           #Number of 'Wins' article received
                    wtf_ct,           #Number of 'Wtfs' article received
                    h_brk_ct,         #Number of 'HeartBreaks' article received
                    max_likes,        #Likes on highest rated comment
                    n_comments,       #Number of comments on article
                    url,              #Article URL
                    json_filename]    #JSON filename 
    
    #Adds badge data to article data list
    if badges:
        b_num = len(badges)
        for i in range(b_num):
            article_data.append(badges[i])
        
        for i in range(3-b_num):
            article_data.append(None)
            
    else:
        for i in range(3):
            article_data.append(None)    
    
    
    #adds article
    articles.append(article_data)
    

    
    return articles, hash_id


def initialize_data(path):
    """Loads data and data logs to make sure scraper doesn't rescrape
    previously collected data"""



    data_file_path = '/'.join([path,'Article_Data.csv'])
    scrape_file_path = '/'.join([path,'Scraped__Url_Data.csv'])
    
    if os.path.exists(data_file_path):
        data = pd.read_csv(data_file_path)
        headers = list(data.columns)
        articles = [list(v) for v in list(data.values)]
    
    else:
        articles = []
        headers = ['Title','Description','Author','Author_Role','Date',
                   'Article_Sub','Page_Type','Trending','Trending_Views',
                   '#_Images','#Tiktoks','#Tweets','#Gifs','#Reddit_Posts',
                   '#Instagrams','#Youtubes','#Tumblr','Love_count','Fail_count',
                   'Lol_count','Cute_count','Omg_count','Win_count',
                   'Wtf_count','ht_bk_count','Max_Likes','#Comments','URL',
                   'json_filename','Badge1','Badge2','Badge3']
    
    
    if os.path.exists(scrape_file_path):
        scraped_data = pd.read_csv(scrape_file_path)
        scraped_urls = list(scraped_data.iloc[:,0])
        scraped_hashes = list(scraped_data.iloc[:,1])
    else:
        scraped_urls = []
        scraped_hashes = []

    return articles, scraped_urls, scraped_hashes, headers

def page_scraper(articles,urls,url_num,h,path):
    """Main scraping loop"""
    
    count = 0
    i = 0
    while count < url_num:
        try:
            if 'buzzfeednews' in urls[i]:
                i += 1
                continue
            else:
                #Checks to see if url has been scraped before
                if urls[i] not in scraped_urls:
                    
                    #page scraper, adds data to articles list
                    articles, hash_id = buzzfeed_scraper(driver,urls[i],articles,h,path)
                    
                    #adds url to scraped_urls list
                    scraped_urls.append(urls[i])
                    scraped_hashes.append(hash_id)
        
                    print('-------','(' + str(count+1) + ' / ' + str(url_num) + ')' )
                    time.sleep(1)
                    count += 1
                    
                    if i == len(urls)-1:
                        break
                    else:
                        i += 1
                
                else:
                    i += 1
                    continue
        
        except KeyboardInterrupt:
            break
    
    return articles,scraped_urls,scraped_hashes

#Path for saved files
path = '/Buzzfeed_NLP'

#Article data and scraped urls list
articles, scraped_urls, scraped_hashes, headers = initialize_data(path)
json_path = '/'.join([path,'json/'])

#Selenium webdriver used to run web browser
driver = webdriver.Chrome('/'.join([path,'chromedriver.exe']))

#Hash function used to give articles unique IDs
h = hashlib.blake2b(digest_size=10)

#File containing urls to be scraped
collected_url_file = '/Buzzfeed_NLP/some_collected_urls.csv'

#urls to be scraped
urls = list(pd.read_csv(collected_url_file).iloc[:,1])


url_num = 100

#gets article data from urls
articles,scraped_urls,scraped_hashes = page_scraper(articles,urls,url_num,h,path)


#Saves Article data to a .csv file
data_file_path = '/'.join([path,'Article_Data.csv'])
data = pd.DataFrame(articles,columns=headers)
data.to_csv(data_file_path,index=False)


#Saves scraped urls list to a .csv file
scrape_file_path = '/'.join([path,'Scraped__Url_Data.csv'])
scraped_data = [scraped_urls,scraped_hashes]
scraped_data = pd.DataFrame(scraped_data).transpose()
scraped_data.to_csv(scrape_file_path,index=False)
    
    
