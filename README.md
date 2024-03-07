# capivarIA newsletter

[![website](https://img.shields.io/badge/Check_the_website-0D1117?style=for-the-badge&logo=Streamlit&logoColor=FF4B4B)](https://geraianews.streamlit.app/)

## 🌱 About
CapivarIA is a newsletter generator that uses AI to summarize news articles. It is built using Python and leverages natural language processing techniques to extract key information from news articles and generate concise summaries. The project aims to provide a convenient way for users to stay updated with the latest news without having to read lengthy articles.

## 🔎 How to use

```
git clone https://github.com/vitornegromonte/newsletter
cd newsletter
pip install -r requirements.txt
cd src
streamlit run app.py
```
## 🛠️ Tech stack

- Front-end: 
    - Streamlit
- Back-end:
    - SerpAPI for Article Scraping
    - Scikit-learn for Data cleaning
    - Langchain for summarization

For more details, check ``requirements.txt``

## Contributors
- Vitor Negromonte (vnco)
- Maria Geizyani (mgss)
- Adna Farias (alfs2)
- Julia Nunes (jnas2)
- Talisson Mendes (tsms)
- Leandro Santos (jlsf)

## Repository structure

```
../capivaria-newsletter
|
|-README.md
|-setup.py
|-.gitignore
|-requirements.txt
|-src
    |-__pycache__
    |-__utils__.py
    |-app.py
    
```

## To do:
- Improve the prompt
- Teste with others LLMs