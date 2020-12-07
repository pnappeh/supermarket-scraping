# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 18:28:29 2020

@author: Pablo
"""

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
import sqlite3
import re
    
def scrape(url):
    
    browser = webdriver.Chrome(ChromeDriverManager().install())
    '''
    #-- FireFox
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    browser = webdriver.Firefox(capabilities=caps)
    '''
    
    browser.get(url)
    time.sleep(5) #seconds
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    name_check = len([name.text for name in soup.find_all('span', class_="product-description js-ellipsis")])
    image_check = len([image.get('src') for image in soup.find_all('img', class_="img-responsive lazyloaded")])
    brands_check = len([brands.text for brands in soup.find_all('span', class_="product-name")])
    links_check = len([links.get('href') for links in soup.find_all('a', class_="product-link")])
    quantity_check = len([quantity.text for quantity in soup.find_all('span', class_="product-attribute")])
    scrolls = 0
    while True: 
        browser.execute_script("window.scrollBy(0, 250)")
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        name_check = len([name.text for name in soup.find_all('span', class_="product-description js-ellipsis")])
        image_check = len([image.get('src') for image in soup.find_all('img', class_="img-responsive lazyloaded")])
        brands_check = len([brands.text for brands in soup.find_all('span', class_="product-name")])
        links_check = len([links.get('href') for links in soup.find_all('a', class_="product-link")])
        quantity_check = len([quantity.text for quantity in soup.find_all('span', class_="product-attribute")])
        #print(name_check, image_check, brands_check, links_check, quantity_check)
        if (name_check == image_check == image_check == brands_check == links_check / 2 == quantity_check):
           break
        scrolls += 1
        if scrolls % 50 == 0:
           browser.execute_script("window.scrollTo(0, 0)") 
       
    browser.execute_script("window.scrollBy(0, -250)")
    
    # Give source code to BeautifulSoup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    # Take the buttons to navigate through
    navegacion = soup.find_all('li', class_="active")
    next_page = navegacion[len(navegacion) - 1].find_next('li')
    element = browser.find_element(By.LINK_TEXT, next_page.text)
    next_pages = navegacion[len(navegacion) - 1].find_all_next('li', limit = 3)  
    #for i in range(len(next_pages)):
    #    print(next_pages[i])
    pages = re.findall("(\d+(?:\.\d{3})?)", next_pages[2].text)

    
    # Create lists for data
    names = []
    brands = []
    price = []
    price_discount = []
    savings = []
    links = []
    quantity = []
    image = []
    details = []
    
    
    for i in range(int(pages[0])):
        if i == int(pages[0]) - 1:
            names.extend([name.text for name in soup.find_all('span', class_="product-description js-ellipsis")])
            brands.extend([brands.text for brands in soup.find_all('span', class_="product-name")])
            links.extend([links.get('href') for links in soup.find_all('a', class_="product-link")])
            quantity.extend([quantity.text for quantity in soup.find_all('span', class_="product-attribute")])
            image.extend([image.get('src') for image in soup.find_all('img', class_="img-responsive lazyloaded")])
            details.extend([details.text for details in soup.find_all('span', class_=["price-sell", "price-internet", "price-save"])])
            
            # Make the loop to check prices
            for k in range(len(details)):
                try:
                    details[k + 1]
                except:
                    break
                
                if "Normal" in details[k]:
                    if "Ahorro" in details [k + 1]:
                        details[k - 1] = re.findall("(\d+(?:\.\d{3})?)", details[k - 1])
                        details[k] = re.findall("(\d+(?:\.\d{3})?)", details[k])
                        details[k + 1] = re.findall("(\d+(?:\.\d{3})?)", details[k + 1])
                        #print(details[k - 1], details[k], details[k + 1])
                        details[k - 1] = [details[k - 1], details[k], details[k + 1]]
                        details.remove(details[k])
                        details.remove(details[k])
                    else:
                        details[k - 1] = re.findall("(\d+(?:\.\d{3})?)", details[k - 1])
                        details[k] = re.findall("(\d+(?:\.\d{3})?)", details[k])
                        details[k - 1] = [details[k - 1], details[k]]
                try:
                    details[k + 1]
                except:
                    break
    
            for l in range(len(details)):
                if len(details[l]) == 3:
                    price.append(details[l][0][0])
                    price_discount.append(details[l][1][0])
                    savings.append(details[l][2][0])
                elif len(details[l]) == 2:
                    price.append(details[l][0][0])
                    price_discount.append(details[l][1][0])
                    savings.append(None)
                else:
                    details[l] = re.findall("(\d+(?:\.\d{3})?)", details[l])
                    price.append(details[l][0])
                    price_discount.append(None)
                    savings.append(None)
            details.clear()          
            continue
        
        names.extend([name.text for name in soup.find_all('span', class_="product-description js-ellipsis")])
        brands.extend([brands.text for brands in soup.find_all('span', class_="product-name")])
        #price.extend([price.text for price in soup.find_all('span', class_="price-sell")])
        links.extend([links.get('href') for links in soup.find_all('a', class_="product-link")])
        quantity.extend([quantity.text for quantity in soup.find_all('span', class_="product-attribute")])
        image.extend([image.get('src') for image in soup.find_all('img', class_="img-responsive lazyloaded")])
        details.extend([details.text for details in soup.find_all('span', class_=["price-sell", "price-internet", "price-save"])])
        
        # Make the loop to check prices
        for k in range(len(details)):
            try:
                details[k + 1]
            except:
                break
            
            if "Normal" in details[k]:
                if "Ahorro" in details [k + 1]:
                    details[k - 1] = re.findall("(\d+(?:\.\d{3})?)", details[k - 1])
                    details[k] = re.findall("(\d+(?:\.\d{3})?)", details[k])
                    details[k + 1] = re.findall("(\d+(?:\.\d{3})?)", details[k + 1])
                    #print(details[k - 1], details[k], details[k + 1])
                    details[k - 1] = [details[k - 1], details[k], details[k + 1]]
                    details.remove(details[k])
                    details.remove(details[k])
                else:
                    details[k - 1] = re.findall("(\d+(?:\.\d{3})?)", details[k - 1])
                    details[k] = re.findall("(\d+(?:\.\d{3})?)", details[k])
                    details[k - 1] = [details[k - 1], details[k]]
                    details.remove(details[k])
            try:
                details[k + 1]
            except:
                break

        for l in range(len(details)):
            if len(details[l]) == 3:
                price.append(details[l][0][0])
                price_discount.append(details[l][1][0])
                savings.append(details[l][2][0])
            elif len(details[l]) == 2:
                price.append(details[l][0][0])
                price_discount.append(details[l][1][0])
                savings.append(None)
            else:
                details[l] = re.findall("(\d+(?:\.\d{3})?)", details[l])
                price.append(details[l][0])
                price_discount.append(None)
                savings.append(None)
        details.clear()
        for i in range(len(names)):
            print('LIDER', names[i], brands[i], price[i], price_discount[i], savings[i], "www.lider.cl" + links[2 * i], quantity[i], image[i])
        # Click to next page
        element.click()
        
        url = browser.current_url
        browser.get(url)
        time.sleep(5) #seconds
        scrolls = 0
        while True: 
            browser.execute_script("window.scrollBy(0, 250)")
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            name_check = len([name.text for name in soup.find_all('span', class_="product-description js-ellipsis")])
            image_check = len([image.get('src') for image in soup.find_all('img', class_="img-responsive lazyloaded")])
            brands_check = len([brands.text for brands in soup.find_all('span', class_="product-name")])
            links_check = len([links.get('href') for links in soup.find_all('a', class_="product-link")])
            quantity_check = len([quantity.text for quantity in soup.find_all('span', class_="product-attribute")])
            #print(name_check, image_check, brands_check, links_check, quantity_check)
            if (name_check == image_check == image_check == brands_check == links_check / 2 == quantity_check):
               break
            scrolls += 1
            if scrolls % 50 == 0:
               browser.execute_script("window.scrollTo(0, 0)") 
        # Give source code to BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        navegacion = soup.find_all('li', class_="active")
        next_page = navegacion[len(navegacion) - 1].find_next('li')
        element = browser.find_element(By.LINK_TEXT, next_page.text)
  
    try:
        db = sqlite3.connect('super.db') 
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lider(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, supermercado TEXT, name TEXT, brand TEXT, price TEXT, price_discount TEXT, savings TEXT, link TEXT, quantity TEXT, image TEXT)''')
        db.commit()
        for p in range(len(names)):
            print(names[p], " ", brands[p], " ",  "www.lider.cl" + links[2 * p], " ", price[p], " ", quantity[p], sep="")
        for i in range(len(names)):
            cursor.execute('''INSERT INTO lider(supermercado, name, brand, price, price_discount, savings, link, quantity, image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''', ('LIDER', names[i], brands[i], price[i], price_discount[i], savings[i], "www.lider.cl" + links[2 * i], quantity[i], image[i]))
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        
    
scrape('https://www.lider.cl/supermercado/category/Bebidas-Licores/Destilados/_/N-7n2dag')
scrape('https://www.lider.cl/supermercado/category/Bebidas-Licores/Coctel-y-Licores/_/N-8rxdu7')
scrape('https://www.lider.cl/supermercado/category/Bebidas-Licores/Vinos-y-Espumantes/_/N-she0ig')
scrape('https://www.lider.cl/supermercado/category/Bebidas-Licores/Cervezas/_/N-1mi8n3m')
#browser.close()
