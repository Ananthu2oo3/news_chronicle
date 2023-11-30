import openai
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set your OpenAI API key
openai.api_key = "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"

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
    chatgpt_prompt = f"Summarize the following text:\n{prompt}"

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

def main():
    # Example URL
    # url = "https://constructafrica.com/projects-and-tenders/drc-invites-bids-build-primary-schools"
    data = pd.
    # Fetch content from the website
    html_content = get_website_content(url)

    if html_content:
        # Extract text content from HTML
        text_content = extract_text_from_html(html_content)

        # Truncate content to fit within the model's maximum context length
        truncated_content = truncate_text(text_content, 500)

        # Get a summary from ChatGPT
        summary = get_chatgpt_summary(truncated_content)

        # Print the results
        print(f"Original URL: {url}")
        print("\nChatGPT Summary:")
        print(summary)

if __name__ == "__main__":
    main()
