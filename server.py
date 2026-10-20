import asyncio
import websockets

CONNECTED_CLIENTS = set()

async def broadcast(message):
    if CONNECTED_CLIENTS:
        tasks = [asyncio.create_task(client.send(message)) for client in CONNECTED_CLIENTS]
        await asyncio.gather(*tasks, return_exceptions=True)

async def handler(websocket, *args):
    CONNECTED_CLIENTS.add(websocket)
    print("[+] Client connected")

    try:
        await websocket.send("System: Connected to WebSocket Server!")
        async for message in websocket:
            if not isinstance(message,str) or not message.strip():
                continue
            if len(message)>500:
                continue
            print(f"Relaying: {message}")
            await broadcast(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        CONNECTED_CLIENTS.discard(websocket)
        print("[-] Client disconnected")

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        print("WebSocket server running on ws://127.0.0.1:8765")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shut down.")
