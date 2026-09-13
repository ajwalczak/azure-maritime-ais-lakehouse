import azure.functions as func
import logging
import os
import json
import time
import websocket
from azure.eventhub import EventHubProducerClient, EventData

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def timer_trigger_ingest(myTimer: func.TimerRequest) -> None:
    logging.info('Rozpoczynam cykl pobierania AIS...')
    
    # Automatyczne pobranie rozszyfrowanych kluczy ze zmiennych środowiskowych / Key Vault
    api_key = os.environ.get("AisstreamApiKey")
    eh_conn_str = os.environ.get("EVENT_HUB_CONNECTION_STRING")
    
    if not api_key or not eh_conn_str:
        logging.error("Brak kluczy dostępu w konfiguracji!")
        return

    producer = EventHubProducerClient.from_connection_string(
        conn_str=eh_conn_str, 
        eventhub_name="eh-ais-stream"
    )
    events_batch = []
    
    # Funkcja serwerless pobiera dane przez max 45 sekund, mieszcząc się w limitach timeoutu
    timeout = time.time() + 45 

    def on_message(ws, message):
        data = json.loads(message)
        mmsi = data.get('MetaData', {}).get('MMSI', 'Nieznany')
        logging.info(f"Złapano statek MMSI: {mmsi}")
        
        events_batch.append(EventData(message))
        
        if time.time() > timeout:
            ws.close()

    def on_open(ws):
        logging.info("Połączono z zewnętrznym API.")
        subscribe_message = {
            "APIKey": api_key,
            "BoundingBoxes": [[[54.0, 18.0], [55.0, 20.0]]],
            "FilterMessageTypes": ["PositionReport"]
        }
        ws.send(json.dumps(subscribe_message))
        
    def on_error(ws, error):
        logging.error(f"Błąd połączenia: {error}")
        
    def on_close(ws, close_status_code, close_msg):
        logging.info("Zamknięto strumień. Przechodzę do wysyłki.")

    # Nasłuch
    ws = websocket.WebSocketApp("wss://stream.aisstream.io/v0/stream",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
    
    # Masowa wysyłka do bufora Event Hubs
    if events_batch:
        logging.info(f"Wysyłam paczkę {len(events_batch)} zdarzeń do Event Hubs...")
        batch = producer.create_batch()
        for event in events_batch:
            try:
                batch.add(event)
            except ValueError:
                producer.send_batch(batch)
                batch = producer.create_batch()
                batch.add(event)
        producer.send_batch(batch)
        logging.info("Zakończono sukcesem!")
