from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time
import requests
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def save_img(prod,images,pp):
    #
#     parent_path=p
    path = os.path.join(pp, prod.replace("/","-"))
    # print(path)
    if not os.path.isdir(path):
        
        os.mkdir(path)
        
#     else:
#         os.mkdir(path)
    
        
    for i,l in enumerate(images):
            # if(l.startswith('https')):
        t=urlparse(l)
        x=os.path.basename(t.path)
        with open(path +"/"+ str(i)+".jpg", 'wb') as handle:
            response = requests.get(l, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
                
                
                
prod_urls=["https://www.zara.com/in/en/woman-shirts-shirts-l1244.html?v1=1445672",
           "https://www.zara.com/in/en/woman-tops-l1322.html?v1=1445752",
           "https://www.zara.com/in/en/woman-tops-crop-l1584.html?v1=1445790",
           "https://www.zara.com/in/en/woman-shirts-event-l1219.html?v1=1445730",
           "https://www.zara.com/in/en/woman-trousers-l1335.html?v1=1445724",
           "https://www.zara.com/in/en/woman-tshirts-l1362.html?v1=1445717",
           "https://www.zara.com/in/en/woman-jeans-l1119.html?v1=1445721",
           "https://www.zara.com/in/en/woman-blazers-l1055.html?v1=1445747",
           "https://www.zara.com/in/en/woman-trousers-shorts-l1355.html?v1=1445920",
           "https://www.zara.com/in/en/woman-knitwear-l1152.html?v1=1445718",
           "https://www.zara.com/in/en/woman-skirts-l1299.html?v1=1445719",
           "https://www.zara.com/in/en/woman-jackets-l1114.html?v1=1445720",
           "https://www.zara.com/in/en/woman-sweatshirts-l1320.html?v1=1445645",
           "https://www.zara.com/in/en/woman-outerwear-l1184.html?v1=1445646"
           
           
          ]
parent_dir="tops-data/zara_wo"
options = Options()
options.headless = True
           
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)
driver.maximize_window()
driver.get("https://www2.hm.com/en_us")




for prod_url in prod_urls:
    
    driver.quit()
    driver =webdriver.Firefox(options=options)
    driver.get(prod_url)
    time.sleep(3)
  
    
    folder_name=prod_url.split(".html")[0].split("/")[-1]
    parent_path = os.path.join(parent_dir, folder_name.replace("/","-"))
    if not os.path.isdir(parent_path):
        os.mkdir(parent_path)
    print(parent_path)
    
    a=driver.find_elements_by_css_selector('a.item._item')
    links=[]
    for i in a:
        links.append(i.get_attribute('href'))
    links=(list(set(links)))
    print(len(links))
           
    k=0
    for href in links:
        k+=1
        print(k)
        if k%30==0:
            driver.delete_all_cookies()
            driver.quit()
            time.sleep(20)
            driver =webdriver.Firefox(options=options)
            driver.get(href)
        try:    
            driver.get(href)
            time.sleep(4)
            driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/4);")
#             col=driver.find_elements_by_css_selector('label._color>span')
#             print(len(col))

#             if len(col)!=0:
#                 for j in range(len(col)+1):
#                     images=[]

#                     name = driver.find_element_by_css_selector("h1.product-name").text
#                     color = driver.find_element_by_css_selector("span._colorName").text
#                     prod=name+"-"+color
#                     lk=driver.find_elements_by_css_selector('a._seoImg.main-image > img.image-big._img-zoom._main-image')
#                     for i in lk:
#                         images.append(i.get_attribute('src'))

#     #                 print(images)
#                     save_img(prod,images,parent_path)
#                     if(j<len(col)):

#                         col[j].click()
#                         time.sleep(3)
#                         driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/4);")
#                         time.sleep(3)
#                         col=driver.find_elements_by_css_selector('label._color>span')


#             else:
            images=[]
            name = driver.find_element_by_css_selector("h1.product-name").text
            color = driver.find_element_by_css_selector("span._colorName").text
            prod=name+"-"+color
            lk=driver.find_elements_by_css_selector('a._seoImg.main-image > img.image-big._img-zoom._main-image')
            for i in lk:
                images.append(i.get_attribute('src'))
            save_img(prod,images,parent_path)
            print(prod)


        except:
            pass
