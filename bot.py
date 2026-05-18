import os
import time
import requests
from playwright.sync_api import sync_playwright


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URL principal de Fanki o la sección de deportes
URL_FANKI = 'https://fanki.com.mx/en/Cruz_Azul' 

def enviar_telegram(mensaje):
    """Envía un mensaje push a tu celular vía Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=payload)
        print("Notificación enviada a Telegram.")
    except Exception as e:
        print(f"Error enviando Telegram: {e}")

def monitorear_boletos():
    """Abre el navegador invisible y busca los boletos continuamente."""
    print("Iniciando monitoreo de Fanki...")
    
    with sync_playwright() as p:
        # Lanzamos el navegador en modo invisible (headless=True)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
    
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Revisando la página...")
            page.goto(URL_FANKI, timeout=60000)
            
            # Le damos 5 segundos a la página para cargar todo el JavaScript
            page.wait_for_timeout(5000) 
            
            contenido = page.locator("body").inner_text().lower()
            
            if "final" in contenido or "pumas" in contenido:
                mensaje = f"🚨 ¡ALERTA! Posible venta activa del Cruz Azul en Fanki. Revisa ya: {URL_FANKI}"
                enviar_telegram(mensaje)
                print("¡Coincidencia encontrada! ¡Mensaje enviado!")
            else:
                print("Aún no hay rastros del partido.")
                
        except Exception as e:
            print(f"Error de red o al cargar la página: {e}")
            
        browser.close()

if __name__ == "__main__":
    monitorear_boletos()