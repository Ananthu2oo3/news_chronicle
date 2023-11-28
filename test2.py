import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

data = []
header = ['title', 'link']

def write_csv():

    with open('link.csv', mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def startpy():
    prompt  = input("Prompt: ")
    key     = prompt.replace(" ", "%20")
    driver  = webdriver.Chrome()

    source  = pd.read_csv('source.csv')
    rows    = source.shape[0]
    
    processed_urls = set()  
    
    for i in range(rows):
        base_url = source.base_url[i]
        xpath    = source.xpath[i]
   
        for i in range(1,5):
            try:
                url = f"{base_url.format(key= key, page=i)}"
                driver.get(url)

                for j in range(1, 11):
                    try:
                        xp = xpath.format(i)
                        link = driver.find_element(By.XPATH, xp)
                        url = link.get_attribute("href")
                        title = link.text

                        if url not in processed_urls:
                            entry = {
                                "title": title,
                                "link": url
                            }
                            data.append(entry)
                            processed_urls.add(url)

                    except:
                        pass


            except:
                pass

    driver.quit() 

    
if __name__ == '__main__':
    startpy()
    write_csv()
