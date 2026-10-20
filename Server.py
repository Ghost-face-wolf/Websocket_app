import asyncio
import json
import websockets

# keeping track of clients here
active_users = set()

async def broadcast_msg(msg):
    # just sending to everyone connected rn
    if len(active_users) > 0:
        
        coros = []
        for c in active_users:
            coros.append(c.send(msg))
        
        results = await asyncio.gather(*coros, return_exceptions=True)
        # checking errors silently lol
        for r in results:
            if isinstance(r, Exception):
                print("oops, error broadcasting:", r)

async def handle_client(websocket, path=None): # added path just in case older websockets lib complains, can't remember
    active_users.add(websocket)
    ip_addr = websocket.remote_address
    print("New connection from:", ip_addr)

    # welcome payload
    welcome_dict = {"sender": "Server", "text": "Welcome to the chat room!"}
    try:
        await websocket.send(json.dumps(welcome_dict))
    except Exception as e:
        print("Failed to send welcome:", e)

    try:
        async for message in websocket:
            print(f"Got message from {ip_addr}: {message}")
            # broadcast it out
            await broadcast_msg(message)
    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed abruptly with {ip_addr}")
    except Exception as ex:
        print("Some other error happened:", ex)
    finally:
        # cleanup
        if websocket in active_users:
            active_users.remove(websocket)
        print("Client left:", ip_addr)

async def main():
    HOST = '127.0.0.1' # changing to localhost IP string
    PORT = 8765
    
    print(f"Starting server on port {PORT}...")
    # using websockets.serve context manager
    async with websockets.serve(handle_client, HOST, PORT):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually by user.")


