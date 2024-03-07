import streamlit as st
from __utils__ import GoogleScrapper, SummarizeText

st.title('CapivarIA')

serpapi_key = st.text_input('Enter your Serp API Key', type = 'password')
openai_api_key = st.text_input('Enter your OpenAI API Key', type = 'password')

news_count = st.number_input('Number of news to be fetched', min_value=1, max_value=100, value=20)

user_query = st.text_input('What\'s your newsletter about?')


if st.button('Submit'):
    st.session_state.serpapi_key = serpapi_key
    st.session_state.user_query = user_query
    st.session_state.news_count = news_count
    
    google_scrapper = GoogleScrapper(serpapi_key, news_count)
    st.session_state.get_text = google_scrapper.get_data(user_query, serpapi_key, news_count)
    
    if not st.session_state.get_text:
            st.write("No results found.")
    
    splitted_text = st.session_state.get_splitted_text
    st.session_state.summarized_texts = SummarizeText.summarize_text(splitted_text, openai_api_key)
        
    for title, summarized_text, url in st.session_state.summarized_texts:
          st.title(title)
          # Add the emoji before the summarized text
          st.write(f"❇️ {summarized_text}")
          st.write(f"🔗 {url}")
          # Create an empty line for a gap
          st.markdown("\n\n")
    
