import asyncio
import websockets

async def receive_messages(websocket):
    """Listens for messages from the server and prints them."""
    try:
        async for message in websocket:
            print(f"\n{message}\n> ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection to server was closed.")

async def send_messages(websocket, username):
    """Reads terminal input and sends it to the server."""
    loop = asyncio.get_running_loop()
    while True:
        # Non-blocking terminal input
        user_input = await loop.run_in_executor(None, input, "> ")
        user_input = user_input.strip()

        if user_input.lower() == "exit":
            break

        if user_input:
            # Plain string format matching the GUI client
            payload = f"{username}: {user_input}"
            await websocket.send(payload)

async def main():
    uri = "ws://127.0.0.1:8765"
    username = input("Enter your username: ").strip() or "TerminalUser"

    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected! (Type 'exit' to quit)\n")

            receiver_task = asyncio.create_task(receive_messages(websocket))
            sender_task = asyncio.create_task(send_messages(websocket, username))

            done, pending = await asyncio.wait(
                [receiver_task, sender_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()
    except Exception as e:
        print(f"Could not connect: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExited.")
