import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot de Discord y la clave de Gemini
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configurar el cliente de Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro') # Puedes cambiar a 'gemini-1.5-flash' si prefieres la versión más rápida y económica

# Configurar el cliente de Discord con los "intents" necesarios
intents = discord.Intents.default()
intents.message_content = True # ¡Esto es crucial para que el bot lea los mensajes!
client = discord.Client(intents=intents)

# Evento que se ejecuta cuando el bot está listo
@client.event
async def on_ready():
    print(f'¡Bot iniciado como {client.user}!')
    print(f'Estoy en {len(client.guilds)} servidores.') # Muestra en cuántos servidores está

# Evento que se ejecuta cuando se recibe un mensaje
@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot para evitar bucles infinitos
    if message.author == client.user:
        return

    # Solo responder a mensajes que lo mencionen o empiecen con un prefijo
    # Ejemplo: Si el mensaje empieza con "!ia" o si lo mencionan
    if message.content.startswith('!ia') or client.user.mentioned_in(message):
        # Obtener el texto del mensaje, quitando el prefijo o la mención
        if message.content.startswith('!ia'):
            user_message = message.content[len('!ia'):].strip() # Quita "!ia"
        else:
            user_message = message.content.replace(f'<@{client.user.id}>', '').strip() # Quita la mención

        if not user_message:
            await message.channel.send("Hola, soy un genocida en potencia. Pregúntame algo después de mencionarme o usar `!ia`.")
            return

        # Indicar que el bot está escribiendo
        async with message.channel.typing():
            try:
                # Enviar el mensaje a la API de Gemini
                response = model.generate_content(user_message)
                # Enviar la respuesta de Gemini de vuelta a Discord
                await message.channel.send(response.text)
            except Exception as e:
                print(f"Error al comunicarse con Gemini: {e}")
                await message.channel.send("Lo siento, hoy me dio ganas de valer verga. Inténtalo de nuevo más tarde.")

# Iniciar el bot con tu token
client.run(DISCORD_BOT_TOKEN)
# === Código para mantener el Web Service de Render despierto ===
import http.server
import socketserver
import threading

PORT = int(os.getenv("PORT", 8080)) # Render asigna un puerto, o usa 8080 por defecto

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot esta vivo!")

def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Servidor web dummy escuchando en puerto {PORT}")
        httpd.serve_forever()

# Iniciar el servidor web dummy en un hilo separado
server_thread = threading.Thread(target=run_server)
server_thread.start()
# ===============================================================
