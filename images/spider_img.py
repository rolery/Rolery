import requests
from bs4 import BeautifulSoup as bs
import re,time
from PIL import Image

url='https://wallhaven.cc/toplist?page=1'

#Cookie='WC=13327034-55675-uzrfqhmF0U7LysYA'

header={"Cookie":"UM_distinctid=1794ba00230504-02724b3643baba-6d517620-144000-1794ba0023184d; chkphone=acWxNpxhQpDiAchhNuSnEqyiQuDIO0O0O; Hm_lvt_2d0601bd28de7d49818249cf35d95943=1621332504,1621422395,1621422405,1621422820; ci_session=64e2c14bb40b45d4e9c0c7284d41389ad49013ee; Hm_lpvt_2d0601bd28de7d49818249cf35d95943=1621422838; PHPSESSID=s1f6q984kvo6hps20l9c7v1o87; __jsluid_h=85ab22bec1bb35ac259925bf2ec8d3af"}
session=requests.session()

html=session.get(url,headers=header)
# print(html.text[0:2])
# for i in range(15):
#     value=''+html.text[0:2]
#     html=session.get(url+value,headers=header)
#     print(html.text[0:2])
soup=bs(html.text,"html.parser")
# print(html.text)
all=soup.find_all("a")

# print(all)
purp=[]
for i in all:
    if("class" in i.attrs and 'preview' in i['class']):
        purp.append(i['href'])
# print(purp)
for i in range(len(purp)):
    img_html=session.get(purp[i])
    img_soup=bs(img_html.text,"html.parser")
    time.sleep(1)
    if(img_soup.find_all('img')):
        purp[i]=img_soup.find_all('img')[-1]['src']
    print(purp[i])
    print('jpg'==purp[i][-3:] or 'png'==purp[i][-3:])
    if('jpg'==purp[i][-3:] or 'png'==purp[i][-3:]):
        r=session.get(purp[i],stream=True)
        with open(r"./thumb1/thumb{}.{}".format(i+1,purp[i][-3:]),"wb") as f:
            for chunk in r.iter_content(chunk_size=32):
                f.write(chunk)
        filename="./thumb1/thumb{}.{}".format(i+1,purp[i][-3:])
        image=Image.open(filename)
        image.save(filename[:-3]+"png")
