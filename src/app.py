import streamlit as st
from __utils__ import get_data, SummarizeText

with st.sidebar:
    st.title('CapivarIA')
    st.write('O CapivarIA é um gerador de newsletter que usa IA para resumir artigos de notícias.')
    serpapi_key = st.text_input('Digite sua chave de API da Serp', type = 'password')
    openai_api_key = st.text_input('Digite sua chave de API da OpenAI', type = 'password')
    st.link_button('Obter uma chave de API da OpenAI', 'https://platform.openai.com/account/api-keys')
    st.link_button('Obter uma chave de API da Serp','https://serpapi.com/')
    # st.link_button('Check the GitHub repository', 'https://github.com/vitornegromonte/newsletter')
    # st.image('../imgs/capivarias.png', 'powered by GERAIA', width=180)

user_query = st.text_input('Qual é o tema de sua newsletter?')

news_count = 10

if st.button('Gerar newsletter'):
    st.session_state.serpapi_key = serpapi_key
    st.session_state.user_query = user_query
    st.session_state.news_count = news_count

    st.session_state.get_splitted_text = get_data(user_query, serpapi_key, news_count)

    if not st.session_state.get_splitted_text:
            st.write("Não foram encontrados resultados.")

    splitted_text = st.session_state.get_splitted_text
    st.session_state.summarized_texts = SummarizeText.summarize_text(splitted_text, openai_api_key)

    for title, summarized_text, url in st.session_state.summarized_texts:
        st.title(title.replace('"', ''))
        # Add the emoji before the summarized text
        st.write(f"❇️ {summarized_text}")
        st.write(f"🔗 {url}")
        # Create an empty line for a gap
        st.markdown("\n\n")
