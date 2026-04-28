import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import io

def scarica_btp_alternativo():
    print("Avvio di Chrome in modalità Server (Headless)...\n")
    
    url = "https://www.qualebtp.it/"
    
    # Impostazioni fondamentali per far girare Chrome sui server di GitHub
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Modalità invisibile
    chrome_options.add_argument("--no-sandbox") # Necessario su Linux/Server
    chrome_options.add_argument("--disable-dev-shm-usage") # Evita crash per memoria
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    
    # Fingiamo di avere una finestra grande anche se siamo invisibili
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        print(f"Navigazione verso {url} ...")
        driver.get(url)
        
        # Aspettiamo 10 secondi per sicurezza, i server a volte sono un po' più lenti
        print("Attendo 10 secondi per il caricamento completo della pagina...")
        time.sleep(10)
        
        html_finito = driver.page_source
        print("Pagina caricata! Estrazione della tabella in corso...\n")
        
        tabelle = pd.read_html(io.StringIO(html_finito), flavor='html5lib')
        
        df_btp = tabelle[0]
        
        print("✅ SUCCESSO MAGNIFICO!")
        print(f"Trovati {len(df_btp)} BTP diversi!\n")

        nome_file = "dati_btp_completi.csv"
        df_btp.to_csv(nome_file, index=False)
        print(f"💾 File salvato con successo: '{nome_file}'")

    except ValueError:
        print("❌ Nessuna tabella trovata. Possibile blocco o struttura cambiata.")
    except Exception as e:
        print(f"❌ Si è verificato un errore: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Browser chiuso. Fine operazioni.")

if __name__ == "__main__":
    scarica_btp_alternativo()