import speech_recognition as sr
import requests

# Função para ouvir comando de voz
def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale o comando:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")
        return comando
    except sr.UnknownValueError:
        print("Não entendi o que você disse")
        return ""
    except sr.RequestError as e:
        print(f"Erro ao conectar ao serviço de reconhecimento: {e}")
        return ""

# URL da API Django
url = "http://127.0.0.1:8000/api/automacao/adicionar/"

# Token da usuária Carmen
headers = {
    "Authorization": "Token 85157d079b7778b54ddbcbef51216ea37a29394b",
    "Content-Type": "application/json"
}

# Captura e envia o comando
comando = ouvir_comando()
if comando:
    resposta = requests.post(url, json={"comando": comando}, headers=headers)
    print(resposta.json())
