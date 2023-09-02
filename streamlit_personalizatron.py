import streamlit as st
import requests
import yaml
from yaml.loader import SafeLoader
from streamlit_lottie import st_lottie_spinner
import streamlit_authenticator as stauth


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
            response = langchain_helper.mail_personalizado(empresa, prospecto, url)
        st.subheader('Correo para ' + prospecto + ' de ' + empresa + ':')
        st.info(response['correo'])
        st.balloons()
        
    st.sidebar.caption('Powered by Polímata.AI')
