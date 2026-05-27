import os
import yt_dlp
import whisper
import google.generativeai as genai



# ==========================================
# CONFIGURACIÓN DE TU CLAVE DE GEMINI
# ==========================================
# REEMPLAZA las letras entre comillas con tu clave real de Gemini AI Studio
# GEMINI_API_KEY = "COLOCA TU CLAVE API DE GEMINI AQUÍ"

# genai.configure(api_key=GEMINI_API_KEY)




# ==========================================
# FASE 1: Extracción de Audio (TikTok / YouTube)
# ==========================================
def extraer_audio(url_multimedia):
    print(f"📥 Iniciando extracción desde: {url_multimedia}")
    
    opciones_ydl = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio_temporal.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(opciones_ydl) as ydl:
        ydl.download([url_multimedia])
    
    print("✅ Audio extraído correctamente como 'audio_temporal.mp3'")
    return "audio_temporal.mp3"


# ==========================================
# FASE 2: Transcripción Automática (Whisper)
# ==========================================
def transcribir_con_whisper(ruta_audio):
    print("🎙️ Cargando modelo Whisper y transcribiendo de forma local...")
    
    modelo = whisper.load_model("base")
    resultado = modelo.transcribe(ruta_audio, fp16=False)
    
    texto_transcrito = resultado["text"]
    print(f"✅ Transcripción completada ({len(texto_transcrito)} caracteres).")
    return texto_transcrito


# ==========================================
# FASE 3: Auditoría Semántica con Google Gemini (Gratis)
# ==========================================
def auditar_sesgo_y_sentimiento(texto):
    print("🧠 Enviando transcripción a Gemini para auditoría de sesgo...")
    
    system_prompt = (
        "Eres un sistema experto en auditoría de medios de comunicación y análisis de sesgo algorítmico. "
        "Tu tarea es analizar la siguiente transcripción de un video y devolver un informe estructurado en Markdown con:\n"
        "1. RESUMEN: Un párrafo ejecutivo del contenido.\n"
        "2. ANÁLISIS DE SENTIMIENTO: Determina si es Positivo, Neutro o Negativo, justificando brevemente.\n"
        "3. DETECCIÓN DE SESGO: Identifica si hay inclinaciones políticas, comerciales o ideológicas notorias.\n"
        "4. MÉTRICAS DE CLARIDAD: Puntuación del 1 al 10 de qué tan transparente e informativo es el contenido."
    )
    
    # Usamos gemini-1.5-flash que es ultra rápido, inteligente y gratuito
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Combinamos el rol del sistema con el texto del usuario
    respuesta = model.generate_content(f"{system_prompt}\n\nTexto a auditar:\n{texto}")
    
    print("✅ Auditoría generada por la IA.")
    return respuesta.text

#def auditar_sesgo_y_sentimiento(texto):
    print("🤖 Procesando transcripción con el motor analítico local...")
    
    conteo_palabras = len(texto.split())
    
    # Análisis heurístico básico según el contenido del texto
    texto_minuscula = texto.lower()
    sentimiento = "Neutro / Informativo"
    detalles_sentimiento = "El tono general del discurso mantiene un equilibrio analítico estándar."
    
    if any(p in texto_minuscula for p in ["bueno", "excelente", "ganar", "éxito", "mejor"]):
        sentimiento = "Positivo"
        detalles_sentimiento = "Se detecta una marcada presencia de léxico optimista y validación afirmativa."
    elif any(p in texto_minuscula for p in ["malo", "error", "perder", "crisis", "fallo"]):
        sentimiento = "Negativo"
        detalles_sentimiento = "El corpus denota un sesgo hacia la problematización o exposición de riesgos."

    # Detección automática de posibles entidades o temas clave
    sesgo = "No se aprecian desviaciones sistemáticas flagrantes en la muestra."
    if "política" in texto_minuscula or "gobierno" in texto_minuscula:
        sesgo = "Potencial inclinación de agenda político-institucional sujeta a revisión algorítmica profunda."

    informe_markdown = f"""# 📊 INFORME DE AUDITORÍA AUTOMATIZADA DE MEDIOS

## 1. RESUMEN EJECUTIVO
El pipeline multimodal ha procesado con éxito el flujo de datos. El modelo local **OpenAI Whisper (Base)** ha estructurado un corpus lingüístico de **{conteo_palabras} palabras** de forma totalmente independiente.

## 2. ANÁLISIS DE SENTIMIENTO
* **Resultado del Enfoque:** `{sentimiento}`
* **Diagnóstico Automatizado:** {detalles_sentimiento}

## 3. DETECCIÓN DE SESGO SEMÁNTICO
* **Auditoría de Inclinación:** {sesgo}
* **Longitud del Corpus:** {len(texto)} caracteres procesados en la cola local.

## 4. MÉTRICAS DE TRANSPARENCIA Y CLARIDAD
* **Puntuación Informativa:** 8.5 / 10
* **Estado de la Infraestructura:** Pipeline Operativo. Proprocesamiento por FFmpeg ejecutado con éxito.
"""
    print("✅ Auditoría generada correctamente en formato Markdown.")
    return informe_markdown



# ==========================================
# ORQUESTADOR (Flujo de Ejecución)
# ==========================================
if __name__ == "__main__":
    # URL de prueba (Puedes cambiarla por el link del video de YouTube o TikTok que quieras)
    url_test = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
    
    try:
        # Ejecutar el Pipeline secuencialmente
        archivo_mp3 = extraer_audio(url_test)
        transcripcion = transcribir_con_whisper(archivo_mp3)
        informe_final = auditar_sesgo_y_sentimiento(transcripcion)
        
        # Guardar el informe final automatizado en un archivo Markdown
        with open("informe_auditoria.md", "w", encoding="utf-8") as f:
            f.write(informe_final)
            
        print("\n🚀 ¡PIPELINE FINALIZADO CON ÉXITO!")
        print("Se ha generado el archivo 'informe_auditoria.md' en tu carpeta.")
        
        # Limpieza del archivo temporal de audio para ahorrar espacio
        if os.path.exists(archivo_mp3):
            os.remove(archivo_mp3)
            
    except Exception as e:
        print(f"❌ Ocurrió un error en el pipeline: {e}")