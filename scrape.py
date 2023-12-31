import re
import csv
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


data    = []
header  = ['title', 'link', 'date']

def sort_csv_by_date(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Sort the data based on the 'date' field
    data.sort(key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'), reverse=True)

    # Write the sorted data back to the CSV file
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'date'])
        writer.writeheader()
        writer.writerows(data)

# def convert(date_str):
#     if isinstance(date_str, (str, int, float)):
#         # Corrected date pattern to capture various date formats
#         date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
#         dates = re.findall(date_pattern, str(date_str))

#         # Assuming that there can be multiple matches, convert each one
#         # converted_dates = [datetime.strptime(date, "%m/%d/%Y").strftime("%d/%m/%Y") for date in dates]
#         converted_dates = []
#         for date in dates:
#             try:
#                 # Try to convert using the specified format
#                 converted_date = datetime.strptime(date, "%m/%d/%Y").strftime("%d/%m/%Y")
#                 converted_dates.append(converted_date)
#             except ValueError:
#                 # Handle the case where the format doesn't match
#                 # You can add more formats or handle the error as needed
#                 pass

#         if converted_dates:
#             # Check if there is only one date, return it directly
#             if len(converted_dates) == 1:
#                 return converted_dates[0]
#             else:
#                 return converted_dates
#         else:
#             # Try to extract the date part using a specific pattern
#             date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', date_str)
#             if date_match:
#                 date_str = date_match.group(1)

#                 # Try to parse the date with the specific format
#                 try:
#                     date_obj = datetime.strptime(date_str, "%m/%d/%Y")
#                     return date_obj.strftime("%d/%m/%Y")
#                 except ValueError:
#                     pass

#             # Try to parse the date with multiple formats
#             formats_to_try = ["%B %d, %Y", "%m/%d/%Y - %H:%M", "%A, %B %d, %Y - %H:%M", "%B %d, %Y - %H:%M"]
#             for format_str in formats_to_try:
#                 try:
#                     date_obj = datetime.strptime(date_str, format_str)
#                     return date_obj.strftime("%d/%m/%Y")
#                 except ValueError:
#                     pass

#             # If none of the formats match or no valid date is found, return a placeholder date
#             return '01/01/2000'  # Adjust the placeholder date as needed


import re
from datetime import datetime

def convert(date_str):
    if isinstance(date_str, (str, int, float)):
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        dates = re.findall(date_pattern, str(date_str))

        converted_dates = []
        for date in dates:
            try:
                # Try to convert using the specified format
                converted_date = datetime.strptime(date, "%m/%d/%Y").strftime("%d/%m/%Y")
                converted_dates.append(converted_date)
            except ValueError:
                # Handle the case where the format doesn't match
                # You can add more formats or handle the error as needed
                pass

        if converted_dates:
            if len(converted_dates) == 1:
                return converted_dates[0]
            else:
                return converted_dates
        else:
            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', date_str)
            if date_match:
                date_str = date_match.group(1)

                for format_str in ["%B %d, %Y", "%m/%d/%Y - %H:%M", "%A, %B %d, %Y - %H:%M", "%B %d, %Y - %H:%M"]:
                    try:
                        date_obj = datetime.strptime(date_str, format_str)
                        return date_obj.strftime("%d/%m/%Y")
                    except ValueError:
                        pass

            return '01/01/2000'


def write_csv():

    for row in data:
        row['date'] = convert(row['date'])

    
    with open('link.csv', mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


def pyscrape(prompt):
    # prompt  = input("Prompt: ")
    key     = prompt.replace(" ", "%20")
    driver  = webdriver.Chrome()

    source  = pd.read_csv('source.csv')
    rows    = source.shape[0]
    
    processed_urls = set()  
    
    for i in range(rows):
        base_url = source.base_url[i]
        xpath    = source.title[i]
        basedate = source.date[i]

        for i in range(1,5):
            try:
                url = f"{base_url.format(key= key, page=i)}"
                driver.get(url)

                for j in range(1, 11):
                    try:
                        xp      = xpath.format(j)
                        date_xp = basedate.format(j)

                        date    = driver.find_element(By.XPATH, date_xp).text
                        link    = driver.find_element(By.XPATH, xp)
                        url     = link.get_attribute("href")
                        title   = link.text

                        if url not in processed_urls:

                            entry = {
                                "title" : title,
                                "link"  : url,
                                "date"  : date
                            }
                            
                            data.append(entry)
                            processed_urls.add(url)

                    except:
                        pass


            except:
                pass

    driver.quit() 
    write_csv()
    sort_csv_by_date('link.csv')

    
# if __name__ == '__main__':
#     prompt = input()
#     pyscrape(prompt)
# #     write_csv()
# #     sort_csv_by_date('link.csv')