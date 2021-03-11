# 抓取 樂透號碼 資料 
# 每個人都有夢想,我的夢想就是能夠中樂透,所以我想搜尋樂透號碼    來分析關鍵的數字
 
# 儲存成果

# 遇到問題 
# 亂碼 
# 1.以為是瀏覽器被擋住用了headers來處理,結果還是一樣亂碼,最後     是用encoding編碼轉換來用utf-8
# 爬蟲
# 2.在爬蟲的過程中這個網站用了四層table,用了find_all最後沒      辦法抓取,解決用select

import requests
from bs4 import BeautifulSoup
import jieba
import jieba.analyse

def get_fulltext():
    fulltext = ""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'ASPSESSIONIDQUCQSCRQ=GKNBMDHDECJNGMECEFEDINCG; ASPSESSIONIDAWQRRAQS=CIDJODHDMMJJPFKEFAENHPCP; ASPSESSIONIDAGQTRDSQ=GMEFFOGDAICDIAJFBJLNAMFL',
    'referer': 'https://www.lotto-8.com/listltobigbbk.asp?%20indexpage=1&orderby=new',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'
    }

    url = "https://www.lotto-8.com/listltobigbbk.asp?indexpage=1&orderby=new"
    response = requests.get(url,headers=headers)
    html = BeautifulSoup(response.text)
    final_page = html.find_all("a", target="_self")[-1]['href']
    final_page = final_page.split("?")[-1].split("&")[0].split("=")[-1]
    final_page = int(final_page)

    # fulltext=""
    for i in range(final_page):
        url="https://www.lotto-8.com/listltobigbbk.asp?indexpage="+str(i+1)+"&orderby=new"
        response = requests.get(url,headers=headers)
        response.encoding="utf-8" # 編碼轉換
        # print(response.text)
        html = BeautifulSoup(response.text)
        # print(html.text)
        # print(url)
        td_tag = html.find("table",class_="auto-style4").find("tbody").find_all("td",class_="auto-style5")

        total_td = len(td_tag)
        for x in range(4,total_td):
            # print(i, total_td)
            if i==(final_page-1) and x >= (total_td-1):
                return fulltext
            if  0 == (x-1)%4:
                # print(td_tag[int(x)])
                posts = td_tag[int(x)]
                # print(posts.text.strip()+"\n")
                fulltext = fulltext + "," + " ".join(jieba.cut(posts.text.strip()))
            elif 1 == (x-1)%4:
                posts = td_tag[int(x)]
                # print(posts.text.strip()+"\n")
                fulltext = fulltext + "," + " ".join(jieba.cut(posts.text.strip()))

fulltext = get_fulltext()

fulltext = fulltext.replace(" ", "").replace("&nbsp", "").replace("\xa0", "").strip().split(",")
# print("text: ", fulltext)
# print(len(fulltext))


keywords = jieba.analyse.extract_tags(" ".join(fulltext) ,topK=12)
print("keywords", keywords)
result = []
for key in keywords:
    result.append(key+"號")
print("result: ", type(result), result)

# 準備文字雲
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# 先把我們要做文字雲的圖片開起來
mask_path = "money.jpg"
mask = np.array(Image.open(mask_path))
# 準備WordCloud
wc = WordCloud(font_path="./NotoSansCJKtc-Bold.otf", 
               background_color="white", 
               max_words=5000,
               mask=mask,
               collocations=False)
wc.generate(" ".join(result))

# 剛才不足的地方-> 色彩不對，把原圖的色彩擷取出來，而且用來上色wc(文字雲)
color = ImageColorGenerator(mask)
wc.recolor(color_func = color)
# 儲存檔案, 你可在你的project 看到這個檔案
wc.to_file("./money.png")