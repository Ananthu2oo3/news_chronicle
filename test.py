from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

data = []
header = ['title', 'link']

def write_csv():

    with open('link.csv', mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def scrape(url,xpath):
    
    driver = webdriver.Chrome()
    processed_urls = set()
    for i in range(1, 21):
        
        try:
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


def startpy():
    prompt = input("Prompt: ")
    key = prompt.replace(" ", "%20")
    
    with open('source.csv', 'r') as csv_file:
        
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            
            xpath       = row['xpath']
            url    = row['base_url']
            
            scrape(url,xpath)
              

    
if __name__ == '__main__':
    startpy()

