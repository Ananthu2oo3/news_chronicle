
import openai
import requests
import os
import pandas as pd
import time
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    
    except requests.exceptions.RequestException as err:
        print(f"Error fetching content: {err}")
        return None

def extract_text_from_html(html_content):
    # Use BeautifulSoup to parse HTML and extract text content
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text_content

def truncate_text(text, max_tokens):
    # Truncate text to the specified maximum number of tokens
    tokens = text.split()
    return ' '.join(tokens[:max_tokens])

def get_chatgpt_summary(prompt):
    # Define your prompt for ChatGPT
    chatgpt_prompt = f"Rewrite this as a crisp and short news article with no subscribe ad but news alone, also the output must be just one para:\n{prompt}"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chatgpt_prompt,
        max_tokens=2000,  # Adjust the max tokens based on your desired summary length
        temperature=0.5,
        stop=None
    )

    # Extract and return the generated summary
    summary = response["choices"][0]["text"].strip()
    return summary


def process_links_in_batches(links, batch_size):
    summaries = []
    for i in range(0, len(links), batch_size):
        batch = links[i:i + batch_size]
        batch_summaries = process_batch(batch)
        summaries.extend(batch_summaries)
        
    return summaries

def process_batch(links):

    batch_summaries = []
    for url in links:
        html_content = get_website_content(url)
        if html_content:
            text_content = extract_text_from_html(html_content)
            truncated_content = truncate_text(text_content, 500)
            summary = get_chatgpt_summary(truncated_content)
            time.sleep(15)
            print("\n",summary)
            batch_summaries.append({'URL': url, 'Summary': summary})

    return batch_summaries


def main():

    # Read links from the input CSV file
    read = pd.read_csv('link.csv')
    data = read.head(10)

    # Processdef links in batches
    batch_size = 3
    summaries = process_links_in_batches(data['link'], batch_size)

    # Create a DataFrame with the links and summaries
    result_data = pd.DataFrame(summaries)

    # Save the DataFrame with summaries to a new CSV file
    result_data.to_csv('summaries.csv', index=False)


if __name__ == "__main__":
    main()

