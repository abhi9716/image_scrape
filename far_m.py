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
    if os.path.isdir(path):
        prod=prod.replace("/","-")+"_"+str(c)
        path=os.path.join(pp,prod)
        os.mkdir(path)
        
    else:
        os.mkdir(path)
    
        
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

prod_urls=["https://www.farfetch.com/in/shopping/men/coats-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/jackets-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/denim-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/polo-shirts-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/shirts-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/shorts-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/suits-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/sweaters-knitwear-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/beachwear-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/trousers-2/items.aspx?view=180","https://www.farfetch.com/in/shopping/men/t-shirts-vests-2/items.aspx?view=180"]
parent_dir="tops-data/farfetch_m"
options = Options()
options.headless = True
           
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)
driver.maximize_window()
driver.get("https://www.farfetch.com/")

           

for prod_url in prod_urls:
    
    driver.quit()
    driver =webdriver.Firefox(options=options)
    driver.get(prod_url)
#     time.sleep(5)
  
    
    folder_name=prod_url.split("/")[5]+"_"+prod_url.split("/")[6]
    parent_path = os.path.join(parent_dir, folder_name.replace("/","-"))
    if not os.path.isdir(parent_path):
        os.mkdir(parent_path)
    print(parent_path)
    
    links=[]
    n=0
    try:
        while True:

            # s[0].click()
            time.sleep(5)
            # driver.implicitly_wait(10)
            driver.execute_script("window.scrollTo(0, 0.93*document.body.scrollHeight);")
            a=driver.find_elements_by_css_selector('a._7b040e')

            for d in a:
              # print(d.get_attribute('href'))
                links.append(d.get_attribute('href'))


            h=WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a._cf3b6e._6297d2._e7b42f")))
    #         h=driver.find_elements_by_css_selector('a._cf3b6e._6297d2._e7b42f')[0]
            h.click()
            print(links[-1])
            n+=1
            print(n)
    except:
        pass
    links=(list(set(links)))
    print(len(links))
           
    h=0
    for link in links[0:]: 
        h+=1
        print(h)
        if h%30==0:
            driver.delete_all_cookies()
            driver.quit()
            time.sleep(20)
            driver =webdriver.Firefox(options=options)
            driver.get(link)
           
           
        driver.delete_all_cookies()
        driver.get(link)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0.2*document.body.scrollHeight);")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source)

        try:
            col=soup.select('div._1cbbde > picture._492380._f8a733 > source')
            a=soup.select('span._e87472._346238._e4b5ec')[0].text
            b=soup.select('span._d85b45._d85b45._1851d6')[0].text
            prod=a+"-"+b
            images=[]
            for img in col:
                images.append(img['srcset'])
            if images:
                save_img(prod,images,parent_path)
#             print(prod)
#             print(len(images))


            g=soup.select('div._5c30af > a')
            lnk=[]
            for n in g:
                lnk.append("https://www.farfetch.com"+n['href'])
            print(len(g))
            if g:
                for c,k in enumerate(lnk):
#                     print(k)
                    # time.sleep(3)
                    driver.get(k)
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, 0.2*document.body.scrollHeight);")
                    time.sleep(2)
                    soup = BeautifulSoup(driver.page_source)

                    col=soup.select('div._1cbbde > picture._492380._f8a733 > source')
                    a=soup.select('span._e87472._346238._e4b5ec')[0].text
                    b=soup.select('span._d85b45._d85b45._1851d6')[0].text
                    prod=a+"-"+b
                    images=[]
                    for img in col:
                        images.append(img['srcset'])
                    if images:
                        save_img(prod,images,parent_path)
                    print(len(images))
            print(prod)
#             print(len(images))
        except:
            pass
    

           
           