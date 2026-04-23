import json
import asyncio
import websockets
import os
from dotenv import load_dotenv

load_dotenv()

class PocketOptionWebSocket:
    def __init__(self):
        # Your specific credentials
        self.uri = "wss://api-eu.po.market/socket.io/?EIO=4&transport=websocket"
        self.auth_msg = f'42["auth",{{ "sessionToken": "{os.getenv("PO_SESSION_TOKEN")}", "uid": "{os.getenv("PO_UID")}", "lang": "en", "isChart": 1 }}]'
        self.is_running = False

    async def connect(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.is_running = True
                print("🔗 Connected to Pocket Option WebSocket")
                
                # Step 1: Send Authentication
                await websocket.send(self.auth_msg)
                print("🔑 Authentication sent")

                # Step 2: Continuous listening
                while self.is_running:
                    response = await websocket.recv()
                    
                    # Pocket Option uses Engine.io (heartbeats start with '2' or '3')
                    if response.startswith('2'):
                        await websocket.send('3') # Heartbeat pong
                    
                    # Real-time price data typically starts with '42["updateStream"'
                    elif response.startswith('42["updateStream"'):
                        data = json.loads(response[2:])
                        print(f"📈 Price Update: {data}")
                        
        except Exception as e:
            print(f"❌ WebSocket Error: {e}")

if __name__ == "__main__":
    client = PocketOptionWebSocket()
    asyncio.get_event_loop().run_until_complete(client.connect())
