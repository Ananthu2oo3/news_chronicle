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

def startpy():
    prompt = input("Prompt: ")
    key = prompt.replace(" ", "%20")
    driver = webdriver.Chrome()

    processed_urls = set()  

    for i in range(1, 21):
        try:
            driver.get(f"https://constructafrica.com/search/node?keys={key}&page={i}%2C0%2C0")

            for j in range(1, 11):
                try:
                    link = driver.find_element(By.XPATH, f'//*[@id="block-mainpagecontent"]/div/ol/li[{j}]/h3/a')
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
