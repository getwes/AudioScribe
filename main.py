# Importando as bibliotecas necessárias
import yt_dlp
import os
from pydub import AudioSegment
import speech_recognition as sr

# URL do vídeo do YouTube
video_url = "https://www.youtube.com/watch?v=ZPcG9PCfagM&list=RDmV4cWyl7zYU&index=4"  # Substitua pelo ID do seu vídeo

# Opções para o yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',  # Baixar o melhor áudio disponível
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',  # Usar FFmpeg para extrair o áudio
        'preferredcodec': 'mp3',  # Formato de saída
        'preferredquality': '192',  # Qualidade do áudio
    }],
    'outtmpl': 'audio.%(ext)s',  # Nome do arquivo de saída
}

# Baixar o vídeo e extrair o áudio
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("Áudio baixado e convertido com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro ao baixar o vídeo: {e}")

#####################################################################################

# Converte MP3 para WAV (se necessário)
audio_file = "audio.webm"
audio = AudioSegment.from_mp3(audio_file)
audio.export("audio.wav", format="wav")

# Cria um reconhecedor
recognizer = sr.Recognizer()

# Transcreve o áudio
with sr.AudioFile("audio.wav") as source:
    audio_data = recognizer.record(source)
    try:
        # Use o Google Web Speech API
        text = recognizer.recognize_google(audio_data, language='pt-BR')
        print("Transcrição:", text)
    except sr.UnknownValueError:
        print("Não consegui entender o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço de reconhecimento; {e}")