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
                
                
                
prod_urls=["https://www2.hm.com/en_us/women/products/dresses.html?product-type=ladies_dresses&sort=stock&image-size=small&image=model&offset=0&page-size=1024",
           "https://www2.hm.com/en_us/women/products/tops.html?product-type=ladies_tops&sort=stock&image-size=small&image=model&offset=0&page-size=709",
          "https://www2.hm.com/en_us/women/products/shirts-blouses.html?product-type=ladies_shirtsblouses&sort=stock&image-size=small&image=model&offset=0&page-size=433",
          "https://www2.hm.com/en_us/women/products/pants.html?product-type=ladies_trousers&sort=stock&image-size=small&image=model&offset=0&page-size=362",
          "https://www2.hm.com/en_us/women/products/jeans.html?product-type=ladies_jeans&sort=stock&image-size=small&image=model&offset=0&page-size=203",
           "https://www2.hm.com/en_us/women/products/sleepwear-loungewear.html",
          "https://www2.hm.com/en_us/women/products/skirts.html?product-type=ladies_skirts&sort=stock&image-size=small&image=model&offset=0&page-size=284",
          "https://www2.hm.com/en_us/women/products/shorts.html?product-type=ladies_shorts&sort=stock&image-size=small&image=model&offset=0&page-size=137",
          "https://www2.hm.com/en_us/women/products/workout-clothes.html?product-type=ladies_sport&sort=stock&image-size=small&image=model&offset=0&page-size=90",
          "https://www2.hm.com/en_us/women/products/hoodies-sweatshirts.html?product-type=ladies_hoodiessweatshirts&sort=stock&image-size=small&image=model&offset=0&page-size=72",
           "https://www2.hm.com/en_us/women/products/jumpsuits-rompers.html?product-type=ladies_jumpsuits&sort=stock&image-size=small&image=model&offset=0&page-size=126",
           "https://www2.hm.com/en_us/women/products/blazers-vests.html?product-type=ladies_blazerswaistcoats&sort=stock&image-size=small&image=model&offset=0&page-size=129",
           "https://www2.hm.com/en_us/women/products/cardigans-sweaters.html?product-type=ladies_cardigansjumpers&sort=stock&image-size=small&image=model&offset=0&page-size=234",
           "https://www2.hm.com/en_us/women/products/jackets-coats.html?product-type=ladies_jacketscoats&sort=stock&image-size=small&image=model&offset=0&page-size=207"           
          ]
parent_dir="tops-data/hnm_wo"
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
    for href in links[0:]:
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
            driver.implicitly_wait(10)
            time.sleep(2)

            lk=driver.find_elements_by_css_selector('ul.group > li.list-item > a')

            print(len(lk))
            for j in range(len(lk)):
                try:
                    lk[j].click()
                    time.sleep(1)


                    lnk=driver.find_elements_by_css_selector('figure.pdp-secondary-image.pdp-image > img')
                    lnkp=driver.find_elements_by_css_selector('div.product-detail-main-image-container > img')
                    name = driver.find_elements_by_css_selector("h1.primary.product-item-headline")[0].text.replace("\n","").replace("\t","").strip()
                    color = driver.find_elements_by_css_selector("h3.product-input-label")[0].text.replace("\n","").replace("\t","").strip()
                    prod=name+"-"+color
            #         print(prod)

                    images=[]
                    images.append(lnkp[0].get_attribute('src'))

            #        
                    for i in lnk:
                        images.append(i.get_attribute('src'))
    #                 print(images)
                    save_img(prod,images,parent_path)



                except:
                    pass
                
            print(prod)
                
                
        except:
            pass