import asyncio
import json
import websockets

async def listen_server(ws):
    try:
        async for incoming in ws:
            try:
                parsed = json.loads(incoming)
                sender_name = parsed.get("sender", "anon")
                msg_text = parsed.get("text", "")
                print(f"\n[{sender_name}]: {msg_text}\n> ", end="", flush=True)
            except json.JSONDecodeError:
                # if someone sends plain text by accident
                print(f"\n[Raw]: {incoming}\n> ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nServer dropped the connection.")

async def write_server(ws, my_name):
    loop = asyncio.get_running_loop()
    while True:
        # getting input via executor so it doesnt freeze things
        text_typed = await loop.run_in_executor(None, input, "> ")
        text_typed = text_typed.strip()
        
        if text_typed == "quit" or text_typed == "exit":
            print("Exiting chat...")
            break
            
        if len(text_typed) > 0:
            data_to_send = json.dumps({"sender": my_name, "text": text_typed})
            await ws.send(data_to_send)

async def run_client():
    server_uri = "ws://localhost:8765"
    my_name = input("Pick a username: ").strip()
    if not my_name:
        my_name = "Guest"

    print("Connecting to ws server...")
    async with websockets.connect(server_uri) as websocket:
        print("Connected successfully! Type 'exit' to leave.\n")
        
        # Fire both tasks up
        listener = asyncio.create_notes = asyncio.create_task(listen_server(websocket)) # wait, typo here, fixed to create_task
        listener = asyncio.create_task(listen_server(websocket))
        writer = asyncio.create_task(write_server(websocket, my_name))

        done, pending = await asyncio.wait(
            [listener, writer],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        for task in pending:
            task.cancel()

# To run the client instead of server, comment out the server main execution and uncomment below:
# if __name__ == "__main__":
#     try:
#         asyncio.run(run_client())
#     except KeyboardInterrupt:
#         print("Client closed.")