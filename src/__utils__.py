import requests
import json
import numpy as np
import pandas as pd
import serpapi

import langchain
from newspaper import Article, ArticleException
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate, LLMChain, OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Class to remove the duplicate articles
def duplicate_check(new_article, articles):
    if not articles:
        # Check if the list is empty
        return True
    
    # Create a new TfidfVectorizer and transform the article texts into vectors
    vectorizer = TfidfVectorizer().fit([new_article] + articles)
    vectors = vectorizer.transform([new_article] + articles)

    # Calculate the cosine similarity of the new article to each of the existing articles
    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])

    # If the highest similarity score is above a threshold (for example, 0.8), return False (not unique), keep at around 0.6
    if np.max(similarity_scores) > 0.6:
        return False

    # Otherwise, return True (unique)
    return True


class Document:
    def __init__(self, title, text):
        self.title = title
        self.page_content = text
        self.metadata = {"stop": []} 
        
# Class to summarize the news articles with the function summarize_text

class SummarizeText:
    def __init__(self, parsed_texts, open_ai_api_key):
        self.parsed_texts = parsed_texts
        self.api_key = open_ai_api_key
        
    def summarize_text(parsed_texts, open_ai_api_key):
        
        summarized_texts_titles_urls = []
        model = OpenAI(openai_api_key= open_ai_api_key, temperature=0.8)
        
        summarizer = load_summarize_chain(model, chain_type = 'map_reduce')
        
        # Define prompt that generates titles for summarized text
        prompt = PromptTemplate(
                input_variables=["temperature","text"], 
                template="Write an appropriate, neutral news article title in less than 70 characters for this text: {text}"
            )
        
        for splitted_text, url in parsed_texts:
        # Convert each text string to a Document object
            parsed_texts = [Document('Dummy Title', text) for text in parsed_texts]
            if not parsed_texts:  # Check if list is empty before running the chain
                print(f"No text to summarize for URL: {url}")
                continue
        # Summarize chunks here
            summarized_text = summarizer.run(parsed_texts)

            # prompt template that generates unique titles
            chain_prompt = LLMChain(llm=model, prompt=prompt)
            clickbait_title = chain_prompt.run(summarized_text)

            summarized_texts_titles_urls.append((clickbait_title, summarized_text, url))
            
        return summarized_texts_titles_urls


# Class to Scrap the data from the Google
def get_data(query, api_key, news_count):        
    params = {
        "q": query,
        "location": "Recife,State of Pernambuco,Brazil",
        "hl": "pt-br",
        "gl": "br",
        "google_domain": "google.com",
        "api_key": api_key
    }

    response = requests.get("https://serpapi.com/search", params)
    results = json.loads(response.text)
    
    excluded_websites = ["ft.com", "cointelegraph.com", "cell.com", "futuretools.io"]
    
    urls = [r["link"] for r in results["organic_results"] if not any(excluded_site in r["link"] for excluded_site in excluded_websites)][:news_count]
    
    parsed_texts = [] #list to store parsed text and corresponding URL
    article_texts = []  # list to store original article texts for similarity comparison
    
    text_splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=200) 

    #iterate over each URL 
    for url in urls:
        try:
            #create an article object
            article = Article(url)

            #download the article 
            article.download()

            #parse the article 
            article.parse()

            # Check if the new article is unique
            if not duplicate_check(article.text, article_texts):
                continue  # If not unique, skip to the next article

            #split text into chunks of 4k tokens 
            splitted_texts = text_splitter.split_text(article.text)
            if not splitted_texts:
                print(article.text)
            
            #Append tuple of splitted text and URL to the list
            parsed_texts.append((splitted_texts, url))
            article_texts.append(article.text)  # Add the text of the new unique article to the list

        except ArticleException: 
            print(f"Failed to download and parse article: {url}")

    return parsed_texts
    
def send_email(subject, 
               body, 
               mail_target, 
               from_email, 
               mailgun_domain, 
               mailgun_api_key):
    
    response = requests.post(
        f'https://api.mailgun.net/v3/{mailgun_domain}/messages',
        auth=('api', mailgun_api_key),
        data={'from': from_email,
              'to': mail_target,
              'subject': subject,
              'text': body})
    
    print("Status code: ", response.status_code)
    print("Response data: ", response.text)
    
    return response 