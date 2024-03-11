import streamlit as st
from __utils__ import get_data, SummarizeText, send_email

with st.sidebar:
    st.title('CapivarIA')
    st.write('CapivarIA is a newsletter generator that uses AI to summarize news articles.')
    serpapi_key = st.text_input('Enter your Serp API Key', type = 'password')
    openai_api_key = st.text_input('Enter your OpenAI API Key', type = 'password')
    st.link_button('Get an OpenAI API key', 'https://platform.openai.com/account/api-keys')
    st.link_button('Get a Serp API key','https://serpapi.com/')
    st.link_button('Check the GitHub repository', 'https://github.com/vitornegromonte/newsletter')
    #st.image('../imgs/capivarias.png', 'powered by GERAIA', width=180)

user_query = st.text_input('What\'s your newsletter about?')
st.divider()
st.write('Optional settings')
col1, col2= st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
    
#with col2:
    #news_temperature = st.selectbox('Choose the style of the titles', ['neutral', 'clickbait', 'boring'])
with col3:
    sending_mail = st.text_input("Email from: ") #email you used to create a MailGun account
with col4:
    recipient_mail = st.text_input("Email To: ")

with col5:
    mailgun_domain = st.text_input("Enter your mailgun Domain here: ")
with col6:
    mailgun_key = st.text_input("Enter your mailgun API key here: ")
    
news_count = st.number_input('Number of news to be fetched', min_value=1, max_value=100, value=20)

if st.button('Submit'):
    st.session_state.serpapi_key = serpapi_key
    st.session_state.user_query = user_query
    st.session_state.news_count = news_count
    
    st.session_state.get_splitted_text = get_data(user_query, serpapi_key, news_count)
    
    if not st.session_state.get_splitted_text:
            st.write("No results found.")
    
    splitted_text = st.session_state.get_splitted_text
    
    debug_scrr = SummarizeText.summarize_text(splitted_text, openai_api_key)
    st.session_state.summarized_texts = debug_scrr
    print(debug_scrr)
    st.session_state.summarized_texts = SummarizeText.summarize_text(splitted_text, openai_api_key)
        
    for title, summarized_text, url in st.session_state.summarized_texts:
        st.title(title.replace('"', ''))
        # Add the emoji before the summarized text
        st.write(f"❇️ {summarized_text}")
        st.write(f"🔗 {url}")
        # Create an empty line for a gap
        st.markdown("\n\n")
    
    email_body = ''
    
    for title, summarized_text, url in st.session_state.summarized_texts:
        email_body += f"❇️{title}\n\n"
        email_body += f"💬 {summarized_text}\n\n"
        email_body += f"🔗 {url} \n\n"
    
    send_email(
        subject = '{user_query} Newsletter',
        body = email_body,
        mail_target = recipient_mail,
        from_email = sending_mail,
        mailgun_domain = mailgun_domain,
        mailgun_api_key = mailgun_key
    )