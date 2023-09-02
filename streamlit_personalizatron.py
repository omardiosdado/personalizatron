import streamlit as st
import requests
import yaml
from yaml.loader import SafeLoader
from streamlit_lottie import st_lottie_spinner
import streamlit_authenticator as stauth
from langchain.document_loaders.base import Document
from langchain.utilities import ApifyWrapper
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from apify_client import ApifyClient


favicon = 'https://polimata.ai/wp-content/uploads/2023/07/favicon-32x32-1.png'
st.set_page_config(
    page_title="Personalizatrón 9000",
    page_icon=favicon,
    initial_sidebar_state="expanded"
)
st.title(":robot_face: Personalizatrón 9000")
st.caption(':turtle: V2.01')
st.subheader('Creador de correos presonalizados')
st.write('Ingresar prospecto, empresa y sitio web en el panel de la izquierda para emprezar la personalización')
st.divider()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'sidebar')


def mail_personalizado(emp1, pros1, url1):
    crawl_input={"crawlerType": "playwright:firefox",
                 "excludeUrlGlobs": [],
                 "maxCrawlDepth": 20,
                 "maxCrawlPages": 1,
                 "initialConcurrency": 0,
                 "maxConcurrency": 200,
                 "initialCookies": [],
                 "dynamicContentWaitSecs": 10,
                 "maxScrollHeightPixels": 5000,
                 "htmlTransformer": "readableText",
                 "readableTextCharThreshold": 100,
                 "maxResults": 9999999,
                 "startUrls": [{"url": url1}]
                 }
    
    loader = apify.call_actor(
        actor_id="apify/website-content-crawler",
        run_input=crawl_input,
        dataset_mapping_function=lambda item: Document(
            page_content=item["text"] or "", metadata={"source": item["url"]}
            ),)
    docs=loader.load()

    q='Formula un correo corto de 5-8 lineas para ' + pros1 + \
        ' ofreciendole el servicio de generación de leads para ' + emp1 + \
            '. El correo debe mencionar las soluciones de ' + emp1 + \
                ' y como se pueden beneficiar a traves de la generación de leads, además de hacerle a '+ pros1 + ' un cumplido.'
    email=chain.run(input_documents=docs, question=q)

    response = {'correo':email}
    return response

if authentication_status == False:
    st.error('Username o contraseña incorrectos')
if authentication_status == None:
    st.warning("Ingresa tu contraseña")
if authentication_status== True:
    authenticator.logout('Logout', "sidebar")
    st.sidebar.title(f'Hola {name}!')
    st.sidebar.header('Capturar datos')
    prospecto = st.sidebar.text_input('Nombre de prospecto', key='nombre_prospecto')
    empresa = st.sidebar.text_input('Nombre de la empresa', key='nombre_empresa')
    url = st.sidebar.text_input('Sitio web', key='sitio_web')

    if 'click' not in st.session_state:
        st.session_state.click = False

    def onClickFunction():
        st.session_state.click = True
        st.session_state.out1 = prospecto
        st.session_state.out2 = empresa
        st.session_state.out3 = url

    runButton = st.sidebar.button('Generar :email:',on_click=onClickFunction)


    def load_lottieurl(url2: str):
        r = requests.get(url2)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_url_hello = "https://lottie.host/57b82a4f-04ed-47c1-9be6-d9bdf4a4edf0/whycX7qYPw.json"
    lottie_url_download = "https://lottie.host/57b82a4f-04ed-47c1-9be6-d9bdf4a4edf0/whycX7qYPw.json"
    lottie_hello = load_lottieurl(lottie_url_hello)
    lottie_download = load_lottieurl(lottie_url_download)


    if st.session_state.click:
        with st_lottie_spinner(lottie_download, key="download", height=200, width=300):
            apify_client = ApifyClient(st.secrets["APIFY_API_TOKEN"])
            apify = ApifyWrapper()
            chat = ChatOpenAI(model_name="gpt-4",temperature=0.3,openai_api_key=st.secrets["OPENAI_API_KEY"])
            chain = load_qa_chain(chat, chain_type="stuff")

            response = mail_personalizado(empresa, prospecto, url)
        st.subheader('Correo para ' + prospecto + ' de ' + empresa + ':')
        st.info(response['correo'])
        st.balloons()
        
    st.sidebar.caption('Powered by Polímata.AI')
