import urllib.request
from bs4 import BeautifulSoup
import requests
import tweepy
import os

# Twitter 各種キーをセット
CONSUMER_KEY = 'PBLg7debh2muWBMc3twnliHQ0'
CONSUMER_SECRET = 'V8Afu4wF5cvdqz1PKS60Pq5S1NOUYTUs6pauV3Ibl6FjfP1piD'
ACCESS_TOKEN = '912456000564715520-rv82MBrVUb4U4O0cjEtTx0xy2NohWGP'
ACCESS_SECRET = '1hPUDY57zSmP9x7JpsPSJrU6UaofBnvEz533yOiUZ3IPv'
 
#apiを取得
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
 
# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update_with_media.json"
 
# DMMのAPP ID, AFFILIATE ID, 検索キーワードをセット
 
APPID = "J5PPSfQ1SVZ6zzT5We1U"
AFFILIATEID = "kdmgs110-999"
KEYWORD = "%E5%87%B0%E3%81%8B%E3%81%AA%E3%82%81"
 
#DMMのAPIを取得し、XMLをBeautifulsoupで取得
html = urllib.request.urlopen("https://api.dmm.com/affiliate/v3/ItemList?api_id=" + APPID + "&affiliate_id=" + AFFILIATEID + "%20&site=DMM.R18&service=digital&floor=videoa&hits=5&sort=date&keyword=" + KEYWORD + "&output=xml")
soup = BeautifulSoup(html,"lxml")
 
#取得したXMLを整理して表示する
 
print("取得したデータを表示します")
print(soup.prettify())
 
#タイトル・女優・画像URL・動画URLを追加
 
items = soup.items #1つ1つのitemオブジェクトを取得
print("取得したitems数:{}".format(len(items.item)))
for item in items:
    print("--------------")
    title = item.title.string #動画タイトル
    title = (title[:40] + "..動画はこちら→") if len(title) > 75 else title #タイトルが40字過ぎたら省略
    print("title:{}".format(title))
    photoURL = item.imageurl.large.string  #画像URL
    print("photoURL: {}".format(photoURL))
    
    #動画によってはサンプル動画がない。ない場合エラーになるので、tryで囲む
    
    try:
        videoURL = item.samplemovieurl.size_476_306.string
        print("videoURL: {} ".format(videoURL))
        
        #ツイート内容
        content = title + "|" + videoURL
        print("ツイート内容：{}".format(content))
        
        #DMMから取得した画像を一度ローカルに保存
        
        request = requests.get(photoURL, stream=True)
        filename = "temp.jpg"
        if request.status_code == 200:
            print("status_code == 200")
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            api.update_with_media(filename, status = content)
            print("ツイートに成功しました")
            os.remove(filename)
        else:
            print("画像をダウンロードできませんでした")
    except Exception as e:
        print(e)
print("プログラムを終了しました")