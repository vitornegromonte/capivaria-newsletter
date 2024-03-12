import requests
import json
import numpy as np
import pandas as pd
import serpapi

import langchain
from openai import OpenAI
from newspaper import Article, ArticleException
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate, LLMChain
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


def scan_text(text, max_length=4000):
    words = text[0].split()

    if len(words) > max_length:
        words_limited = words[:max_length]
        new_text = " ".join(words_limited)
        return new_text
    else:
        return text[0]

# Class to summarize the news articles with the function summarize_text

class SummarizeText:
    def __init__(self, parsed_texts, open_ai_api_key):
        self.parsed_texts = parsed_texts
        self.api_key = open_ai_api_key

    def summarize_text(parsed_texts, open_ai_api_key):

        summarized_texts_titles_urls = []

        client = OpenAI(api_key=open_ai_api_key)

        print(len(parsed_texts))

        for splitted_text, url in parsed_texts:

            if not splitted_text:  # Check if list is empty before running the chain
                print(f"No text to summarize for URL: {url}")
                continue

            splitted_text_scanned = scan_text(splitted_text)

            prompt = f"Escreva um título e um texto de ao menos 60 caracteres de artigo de notícias adequado e neutro para este texto: {splitted_text_scanned}"

            response = client.chat.completions.create(
                model='gpt-3.5-turbo-1106',
                temperature=0.8,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                functions=[
                    {
                        "name": "cria_titulo_e_texto_resumido_de_noticia",
                        "description": "Cria um título e um texto resumido para newsletter a partir de um texto de notícia.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "texto": {
                                    "type": "string",
                                    "description": "Texto de notícia resumido com 60 caracteres, neutro e adequado."
                                },
                                "titulo": {
                                    "type": "string",
                                    "description": "Título de notícia a ser gerado."
                                },
                            }
                        },
                        "required": ["texto", "titulo"]
                    },
                ],
                function_call='auto'
            )

            fn_arguments = json.loads(response.choices[0].message.function_call.arguments)

            summarized_texts_titles_urls.append(
                (fn_arguments["titulo"],
                fn_arguments["texto"],
                url)
            )

        return summarized_texts_titles_urls


# Class to Scrap the data from the Google
def get_data(query, api_key, news_count):
    params = {
        "q": query,
        # "location": "Recife,State of Pernambuco,Brazil",
        "hl": "pt-br",
        "gl": "br",
        "google_domain": "google.com",
        "api_key": api_key,
        "num": 10,
    }

    response = requests.get("https://serpapi.com/search", params)
    results = json.loads(response.text)


    excluded_websites = ["ft.com", "cointelegraph.com", "cell.com", "futuretools.io"]

    urls = [r["link"] for r in results["organic_results"] if not any(excluded_site in r["link"] for excluded_site in excluded_websites)][:news_count]

    parsed_texts = [] #list to store parsed text and corresponding URL
    article_texts = []  # list to store original article texts for similarity comparison

    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10)

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
