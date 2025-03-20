# meshtastic2WU

Questo script Python decodifica i dati dei sensori meteo da un nodo Meshtastic e li pubblica sul servizio Weather Underground.

## Descrizione

`meshtastic2WU` è uno script Python che permette di integrare i dati meteo rilevati da un determinato nodo Meshtastic con il servizio Weather Underground. Questo consente di monitorare e condividere i dati meteo in tempo reale attraverso la piattaforma Weather Underground.

## Requisiti

* Python 3.x
* Libreria `meshtastic` (installabile con `pip install meshtastic`)
* Account Weather Underground con ID stazione e chiave API

## Installazione

1.  Installa le dipendenze:

    ```bash
    pip install meshtastic requests pyserial
    ```

2.  Configura i parametri:

        [WeatherUnderground]
        station_id = TUO_ID_STAZIONE
        api_key = TUA_CHIAVE_API

        [Meshtastic]
        node_shortname = NOME_BREVE_NODO
        serial_port = /dev/ttyUSB0 # esempio di porta seriale o COM1, COM2 a seconda del sistema operativo utilizzato.
        ```

    * Sostituisci i valori segnaposto con le tue credenziali.

