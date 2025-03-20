import serial
import requests
import time

# Configurazione utente
STATION_ID = "XXXXXXX"           # ID stazione Weather Underground
API_KEY = "XXXXXXXX"             # Station KEY Weather Underground
MESHTASTIC_NODE_ID = "AB12"      # ID del nodo Meshtastic da monitorare (utilizzare lo shortname)
SERIAL_PORT = "COM3"             # Porta seriale del dispositivo Meshtastic (verificare la porta in base al proprio OS)
BAUD_RATE = 115200               # Baud rate (modifica se necessario)

# URL API Weather Underground
WU_URL = f"https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

def celsius_to_fahrenheit(celsius):
    return round(((celsius * 9/5) + 32), 2)

def hpa_to_inches_mercury(hpa):
    return round((hpa * 0.02953), 2)

def relative_humidity(humidity_value):
    return  int(round(humidity_value))

def send_to_weather_underground(data):
    try:
        payload = {
            "ID": STATION_ID,
            "PASSWORD": API_KEY,
            "dateutc": "now",
            "tempf": celsius_to_fahrenheit(data['temperature']),
            "humidity": relative_humidity(data['relative_humidity']),
            "baromin": hpa_to_inches_mercury(data['barometric_pressure']),
            "action": "updateraw"
        }
        
        response = requests.get(WU_URL, params=payload)
        response.raise_for_status()  # Solleva un'eccezione se la richiesta fallisce

        # Stampa il risultato
        print(f"Dati inviati con successo! Risposta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante l'invio dei dati: {e}")

def parse_weather_data(line):
    """
    Estrae i dati meteorologici da una riga di testo.
    Esempio di input: "INFO  | 18:02:38 1298 [Router] (Received from AB12): barometric_pressure=953.846008, relative_humidity=60.970181, temperature=14.290808"
    """
    try:
        # Verifica che la riga provenga dal nodo corretto
        if f"(Received from {MESHTASTIC_NODE_ID})" not in line:
            return None
        
        # Estrai i valori dei parametri
        data = {}
        for part in line.split(": ")[-1].split(", "):  # Prendi tutto dopo ": "
            key, value = part.split("=")
            data[key.strip()] = float(value.strip())
        
        # Verifica che ci siano tutti i campi richiesti
        required_fields = ["temperature", "relative_humidity", "barometric_pressure"]
        if all(field in data for field in required_fields):
            return data
        else:
            print("Mancano alcuni campi richiesti nei dati.")
            return None
    except Exception as e:
        print(f"Errore durante il parsing dei dati: {e}")
        return None

def read_meshtastic_serial():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()  # Legge una riga di testo
                print(f"Dati grezzi: {line}")  # Debug: Stampa i dati grezzi ricevuti
                
                # Prova a estrarre i dati meteorologici
                weather_data = parse_weather_data(line)
                if weather_data:
                    send_to_weather_underground(weather_data)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script interrotto dall'utente")
    finally:
        ser.close()

if __name__ == "__main__":
    print(f"Monitoraggio porta seriale {SERIAL_PORT} per il nodo {MESHTASTIC_NODE_ID}...")
    read_meshtastic_serial()