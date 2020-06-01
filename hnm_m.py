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
                
                
                
prod_urls=["https://www2.hm.com/en_us/men/products/t-shirts-tank-tops.html?product-type=men_tshirtstanks&sort=stock&image-size=small&image=model&offset=0&page-size=378",
           "https://www2.hm.com/en_us/men/products/hoodies-sweatshirts.html?product-type=men_hoodiessweatshirts&sort=stock&image-size=small&image=model&offset=0&page-size=72",
          "https://www2.hm.com/en_us/men/products/shirts.html?product-type=men_shirts&sort=stock&image-size=small&image=model&offset=0&page-size=260",
          "https://www2.hm.com/en_us/men/products/jeans.html?product-type=men_jeans&sort=stock&image-size=small&image=model&offset=0&page-size=92",
          "https://www2.hm.com/en_us/men/products/pants.html?product-type=men_trousers&sort=stock&image-size=small&image=stillLife&offset=0&page-size=177",
           "https://www2.hm.com/en_us/men/products/shorts.html?product-type=men_shorts&sort=stock&image-size=small&image=model&offset=0&page-size=222",
          "https://www2.hm.com/en_us/men/products/suits-blazers.html?product-type=men_blazerssuits&sort=stock&image-size=small&image=stillLife&offset=0&page-size=133",
          "https://www2.hm.com/en_us/men/products/swim-wear-trunks.html?sort=stock&image-size=small&image=stillLife&offset=0&page-size=90",
          "https://www2.hm.com/en_us/men/products/cardigans-sweaters.html",
          "https://www2.hm.com/en_us/men/products/jackets-coats.html?product-type=men_jacketscoats&sort=stock&image-size=small&image=model&offset=0&page-size=72"
          ]
parent_dir="tops-data/hnm_m"
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
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a=soup.select('a.item-link.remove-loading-spinner')
    links=[]
    for i in a:
        links.append("https://www2.hm.com/"+str(i["href"]))
#     links=(links)
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
            driver.get(link)
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
            
      
        
    
    


