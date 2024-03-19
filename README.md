# capivarIA newsletter

[![website](https://img.shields.io/badge/Check_the_website-0D1117?style=for-the-badge&logo=Streamlit&logoColor=FF4B4B)](https://geraianews.streamlit.app/)

## 🌱 About
CapivarIA is a newsletter generator that uses AI to summarize news articles. It is built using Python and leverages natural language processing techniques to extract key information from news articles and generate concise summaries. The project aims to provide a convenient way for users to stay updated with the latest news without having to read lengthy articles.

## 🔎 How to use

1. Clone this repository to your machine using `https://github.com/vitornegromonte/newsletter`
2. Install dependencies using `pip install -r requirements.txt`
3. Run the Streamlit application using `streamlit run app.py`
4. In the application, the user must choose a topic that interests them.
5. Enter the keys of the requested APIs - SerpAPI and OpenAI.
6. The application will generate articles related to the chosen topic, showing the title and a brief description.

## 🛠️ Tech stack

- Front-end: 
    - Streamlit
- Back-end:
    - SerpAPI for Article Scraping
    - Scikit-learn for Data cleaning
    - LangChain for summarization

For more details, check ``requirements.txt``

## Contributors
- Vitor Negromonte (vnco)
- Maria Geyzianny (mgss)
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
