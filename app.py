import streamlit as st
import requests
import base64

def translate(text, target_language, api_key):
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}&q={text}&target={target_language}'
    response = requests.get(url)
    translated_text = response.json()['data']['translations'][0]['translatedText']
    return translated_text

def app():
    st.set_page_config(page_title="Dinolingo", page_icon=":books:", layout="wide")
    st.title('Dinolingo')
    st.image('https://i.ibb.co/8s4HkLc/dinolingo-logo.png', use_column_width=True)
    st.markdown('---')
    text = st.text_input('Enter text to translate')
    target_language = st.selectbox('Select target language', ['French', 'Spanish', 'German'])
    api_key = 'your_api_key_here'
    if st.button('Translate'):
        translated_text = translate(text, target_language.lower(), api_key)
        st.success(translated_text)
    st.markdown('---')
    st.subheader('About Dinolingo')
    st.markdown('Dinolingo is a fun and interactive language learning platform for kids. It provides a wide range of language courses that are designed to be engaging and effective. With Dinolingo, kids can learn new languages through games, videos, songs, and stories. The platform offers courses in French, Spanish, German, and many other languages. Dinolingo is a great way for kids to learn new languages and explore new cultures.')
    st.markdown('---')
    st.subheader('Contact Us')
    st.markdown('Email: info@dinolingo.com')
    st.markdown('Phone: +1 (123) 456-7890')
    st.markdown('Address: 123 Main Street, Anytown USA')

def get_base64_of_app():
    return base64.b64encode(app().to_bytes()).decode("utf-8")

if __name__ == '__main__':
    st.markdown(f'<iframe src="data:text/html;base64,{get_base64_of_app()}" width="700" height="600"></iframe>', unsafe_allow_html=True)
