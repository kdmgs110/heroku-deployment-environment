from selenium import webdriver
import time
import requests # for slack  
import json # for slack 

#Phanttomjs Driverを入手
browser = webdriver.PhantomJS()  # DO NOT FORGET to set path

#TODO set search query

query = "ワンピース"  # set search query here
url = "http://okepi.net/top.aspx"

#TODO access to targeted URL

browser.get(url)
print("Successfully accessed to the targeted page! title:{}".format(browser.title))

#TODO insert query into #txtTopSearch

queryField = browser.find_element_by_xpath("//*[@id='txtTopSearch']") # This x-path locates in search form
queryField.send_keys(query) #Insert query message into search form


#TODO submit and load page

submitButton = browser.find_element_by_xpath('//*[@id="btnTopSearch"]')
submitButton.click()
print("Loading...")
browser.implicitly_wait(5) # seconds
print("Submit completed. now at:{}".format(browser.title))

#TODO retrieve ticket data

tables = browser.find_elements_by_class_name("tbl_j") #<table class = "tbl_j">
print("Retrieved tables data")
print("Number of table:{}".format(len(tables)))

#TODO print each ticket data
#TODO insert data that you want from http://okepi.net/all.aspx?key=performance&value=%83%8F%83%93%83s%81[%83X

contents = []

for table in tables:
    try:
        print("#######################")
        title = table.find_element_by_class_name("goleft") #without this, title retrieves web-element object
        print("title:{}".format(title.text)) 
        titleURL = title.find_element_by_css_selector("a").get_attribute("href")
        print("titleURL:{} ".format(titleURL))
        datetime = table.find_element_by_class_name("pdatetime").text
        print("datetime:{} ".format(datetime))
        price_place = table.find_element_by_class_name("price").text
        print("price_place:{} ".format(price_place))
        
        #TODO make summary of each data
        
        content = title.text + "\n" + datetime + "\n" + price_place + "\n" + titleURL + "\n" + "###################\n"
        print(content)
        contents.append(content) # insert contents so slack can post only once
        
    except Exception as e:
        print(e)
        continue

#TODO create summary for slack

summary = "==============" + query + "の新着情報！================\n"

for content in contents:
    summary = summary + content
    
print(summary)

#TODO post summary on slack 

slackURL = "https://hooks.slack.com/services/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" # https://api.slack.com/custom-integrations
requests.post(slackURL, data = json.dumps({
    'text': summary, # 投稿するテキスト
    'username': u'Musical Reminder', # 投稿のユーザー名
    'icon_emoji': u':ghost:', # 投稿のプロフィール画像に入れる絵文字
    'link_names': 1, # メンションを有効にする
}))

print("Successfully posted to Slack")
