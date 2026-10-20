import asyncio
import json
import websockets

async def receive_messages(websocket):
    """Continuously listens for incoming messages from the server."""
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                sender = data.get("sender", "Unknown")
                text = data.get("text", "")
                print(f"\n[{sender}]: {text}\n> ", end="", flush=True)
            except json.JSONDecodeError:
                print(f"\n[Raw Message]: {message}\n> ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection to server was closed.")

async def send_messages(websocket, username):
    """Asynchronously reads input from the terminal and sends it to the server."""
    loop = asyncio.get_running_loop()
    while True:
        # Run standard input() in an executor thread so it doesn't block the event loop
        user_input = await loop.run_in_executor(None, input, "> ")
        user_input = user_input.strip()

        if user_input.lower() == "exit":
            break

        if user_input:
            payload = json.dumps({"sender": username, "text": user_input})
            await websocket.send(payload)

async def main():
    uri = "ws://localhost:8765"
    username = input("Enter your username: ").strip() or "User"

    print(f"Connecting to {uri}...")
    async with websockets.connect(uri) as websocket:
        print(f"Connected! (Type 'exit' to quit)\n")

        # Run listener and sender concurrently
        receiver_task = asyncio.create_task(receive_messages(websocket))
        sender_task = asyncio.create_task(send_messages(websocket, username))

        done, pending = await asyncio.wait(
            [receiver_task, sender_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExited.")