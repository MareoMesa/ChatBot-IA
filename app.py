import streamlit as st #Aviso del uso de la libreria
from groq import Groq #importar la libreria

#Configuracion de la ventana de la web
st.set_page_config(page_title="Mi chat de IA", page_icon="🚗")

st.title("Mi primera aplicacion con Streamlit")

nombre = st.text_input("¿Cual es tu nombre?")


if st.button("entrar!"):
    st.write(f"Hola {nombre}. Gracias por venir a Talento Tech")





MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']



#Nos conecta con la API, creando un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta) #Conectamos a la API

#Selecciona el modelo de IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #Selecciona el modelo de la IA
        messages = [{"role":"user", "content":mensajeDeEntrada}], 
        stream = True #la funcionalidad para que la IA responda en tiempo real
    )
#Historial de mensaje
def inicializar_estado():
    #si no existe "mensajes" entonces creamos un historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #El historial estando vacío

def configurar_pagina():
    st.title("Mi chat de IA") #Titulo
    st.sidebar.title("Configuración") #Titulo
    opcion = st.sidebar.selectbox(
         "Elegí modelo", #titulo
          options = MODELOS, #las opciones deben estar en una lista
          index = 0 #valorPorDefecto
    )
    return opcion #AGREGAMOS ESTO PARA OBTENER EL NOMBRE DEL MODELO
    
def actualizar_historial(rol, contenido, avatar):
    #El append(dato) agrega datos a la lista
                     #  si es la ia o el usuario              el mensaje       icono/imagen
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar })
  
def mostrar_historial(): #guarda la estructura visual del mensaje
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = "" #La variable esta vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content: #Se saca el dato NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa
            
def main():
    # INVOCACION DE LAS FUNCIONES CREADAS
    modelo = configurar_pagina() #agarramos el modelo seleccionado
    clienteUsuario = crear_usuario_groq() #Se conecta con la API de GROQ
    inicializar_estado() #se crea un historial vacio
    area_chat() #Se crea el contenedor de los mensajes

    mensaje = st.chat_input("Escribí un mensaje...")
    #Verificar que la variable mensaje tenga contenido
    if mensaje:
        actualizar_historial("user", mensaje, "🌚") #Mostramos el mensaje en le chat del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #Obtenemos la respuesta de la ia
        if chat_completo: #Se verifica que la variable tenga contenido y si no tiene, no se hace nada
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "⛄")
                st.rerun() #actualizar
            
if __name__ == "__main__":
    main()
