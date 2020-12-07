# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 17:26:06 2020

@author: Pablo
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    
    #last_height = browser.execute_script("return document.body.scrollHeight")
    #browser.execute_script("window.scrollTo(0, 700);")
    #while True: # adjust integer value for need
    scrolls = 0
    while True: 
        browser.execute_script("window.scrollBy(0, 250)")
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
    #   new_height = browser.execute_script("return document.body.scrollHeight")
        #print([image.get('src') for image in soup.find_all('img', class_="lazy-image") if "assets" not in image])
        if (len([name.get('title') for name in soup.find_all('a', class_="shelf-product-title")]) == len([image.get('src') for image in soup.find_all('img', class_="lazy-image") if "assets" not in image.get('src')])):
           break
        scrolls += 1
        if scrolls % 50 == 0:
           browser.execute_script("window.scrollTo(0, 0)") 
        
    #   last_h eight = new_height
    browser.execute_script("window.scrollBy(0, -250)")
    # Give source code to BeautifulSoup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    # Take the buttons to navigate through
    element = browser.find_elements_by_css_selector("button.page-number")
    
    #time.sleep(5) #seconds
    
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
    
    for i in range(len(element) - 1):
        names.extend([name.get('title') for name in soup.find_all('a', class_="shelf-product-title")])
        brands.extend([brands.text for brands in soup.find_all('h3', class_="shelf-product-brand")])
        details.extend([details.text for details in soup.find_all('div', class_=["prices-product", "product-flags", "product-single-price-container", "no-stock"]) if len(details) != 0])
        links.extend([links.get('href') for links in soup.find_all('a', class_="shelf-product-title")])
        quantity.extend([quantity.text for quantity in soup.find_all('span', class_="shelf-single-unit")])
        image.extend([image.get('src') for image in soup.find_all('img', class_="lazy-image") if "assets" not in image.get('src')])
        #print(details)
        # Make the loop to check prices and separate them
        for k in range(len(details)):
            try:
                details[k]
            except:
                break
            
            if "Oferta" in details[k]:
                digits = re.findall("(\d+(?:\.\d{3})?)", details[k + 1])
                if "X" in details[k + 1]:
                    price.append(digits[0])
                    price_discount.append(None)
                    savings.append(digits[1] + "X" + digits[2])
                #print(digits)
                elif len(digits) == 5:
                    price.append(digits[4])
                    price_discount.append(digits[0])
                    savings.append(digits[3])
                elif len(digits) == 3:
                    price.append(digits[2])
                    price_discount.append(digits[0])
                    savings.append(digits[1])
                elif len(digits) == 2:
                    price.append(digits[1])
                    price_discount.append(digits[0])
                    savings.append(None)
                details.remove(details[k + 1])
            
            elif "Sin Stock" in details[k]:
                price.append(details[k])
                price_discount.append(None)
                savings.append(None)
            else:
                digits = re.findall("(\d+(?:\.\d{3})?)", details[k])
                print(digits)
                price.append(digits[0])
                price_discount.append(None)
                savings.append(None)
        details.clear()
        for z in range(len(names)):
            print('JUMBO', names[z], brands[z], price[z], price_discount[z], savings[z], "www.jumbo.cl" + links[z], quantity[z], image[z])
        # Click to next page
        if i == 5 or i != 0 and (i - 11) % 6 == 0:
            try:
                element2 = browser.find_elements_by_css_selector("button.slider-next-button")
                element2[0].click()
                element = browser.find_elements_by_css_selector("button.page-number")
                time.sleep(5)
            except:
                pass
        
        element[i + 1].click()
        
        url = browser.current_url
        browser.get(url)
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, '_hj-f5b2a1eb-9b07_feedback_minimized_text_initial')))
        scrolls = 0
        while True: 
            browser.execute_script("window.scrollBy(0, 250)")
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
        #   new_height = browser.execute_script("return document.body.scrollHeight")
            #print([image.get('src') for image in soup.find_all('img', class_="lazy-image") if "assets" not in image.get('src')])
            if (len([name.get('title') for name in soup.find_all('a', class_="shelf-product-title")]) == len([image.get('src') for image in soup.find_all('img', class_="lazy-image") if "assets" not in image.get('src')])):
                break
            scrolls += 1
            if scrolls % 50 == 0:
               browser.execute_script("window.scrollTo(0, 0)")
        #   last_height = new_height
        browser.execute_script("window.scrollBy(0, -250)")
        
        # Give source code to BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        element = browser.find_elements_by_css_selector("button.page-number")
        
        if i == len(element) - 2:
            names.extend([name.get('title') for name in soup.find_all('a', class_="shelf-product-title")])
            brands.extend([brands.text for brands in soup.find_all('h3', class_="shelf-product-brand")])
            details.extend([details.text for details in soup.find_all('div', class_=["prices-product", "product-flags", "product-single-price-container"]) if len(details) != 0])
            links.extend([links.get('href') for links in soup.find_all('a', class_="shelf-product-title")])
            quantity.extend([quantity.text for quantity in soup.find_all('span', class_="shelf-single-unit")])
            image.extend([image.get('src') for image in soup.find_all('img', class_="lazy-image") if "assets" not in image.get('src')])
            
            # Make the loop to check prices and separate them
        for k in range(len(details)):
            try:
                details[k]
            except:
                break
            
            if "Oferta" in details[k]:
                digits = re.findall("(\d+(?:\.\d{3})?)", details[k + 1])
                if "X" in details[k + 1]:
                    price.append(digits[0])
                    price_discount.append(None)
                    savings.append(digits[1] + "X" + digits[2])
                #print(digits)
                elif len(digits) == 5:
                    price.append(digits[4])
                    price_discount.append(digits[0])
                    savings.append(digits[3])
                elif len(digits) == 3 and (len(digits[0]) or len(digits[2])) != 1:
                    price.append(digits[2])
                    price_discount.append(digits[0])
                    savings.append(digits[1])
                elif len(digits) == 2 and (len(digits[0]) or len(digits[1])) != 1:
                    price.append(digits[1])
                    price_discount.append(digits[0])
                    savings.append(None)
                details.remove(details[k + 1])
            
            elif "Sin Stock" in details[k]:
                price.append(details[k])
                price_discount.append(None)
                savings.append(None)
            else:
                digits = re.findall("(\d+(?:\.\d{3})?)", details[k])
                print(digits)
                price.append(digits[0])
                price_discount.append(None)
                savings.append(None)
        details.clear()
    
    # Open DB with try/except/finally if something goes wrong
    try:
        db = sqlite3.connect('super.db') 
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS jumbo(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, supermercado TEXT, name TEXT, brand TEXT, price TEXT, price_discount TEXT, savings TEXT, link TEXT, quantity TEXT, image TEXT)")
       
        for i in range(len(names)):
            #print('JUMBO', names[i], brands[i], price[i], price_discount[i], savings[i], "www.jumbo.cl" + links[i], quantity[i], image[i])
            #print(details[i])
            cursor.execute('''INSERT INTO jumbo(supermercado, name, brand, price, price_discount, savings, link, quantity, image) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''', ('JUMBO', names[i], brands[i], price[i], price_discount[i], savings[i], "www.jumbo.cl" + links[i], quantity[i], image[i]))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
scrape('https://www.jumbo.cl/vinos-cervezas-y-licores')

#browser.close()