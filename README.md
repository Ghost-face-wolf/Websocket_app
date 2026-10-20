# Real-Time Python WebSocket Chat Application

A lightweight, full-duplex real-time chat application built in Python using WebSockets. It features a central broadcast server, an asynchronous terminal client, and a desktop GUI client that can interact with each other in real time.

---

## 🚀 Features

- **Central Broadcast Server:** Manages multiple connected clients and instantly broadcasts messages to everyone in the room.
- **Tkinter Desktop GUI Client:** Clean desktop interface running non-blocking WebSocket networking via background threads.
- **Asynchronous Terminal Client:** Fast, non-blocking CLI chat client running concurrently on `asyncio`.
- **Cross-Client Interaction:** Terminal clients and GUI clients can connect simultaneously and chat seamlessly with one another.
- **Zero Heavy Dependencies:** Built on Python's standard libraries (`asyncio`, `tkinter`, `threading`) and requires only the core `websockets` package.

---
   ## Setup
   pip install -r requirements.txt

   ## Run
   1. python server.py
   2. python client.py        (terminal client)
   3. python gui_client.py    (GUI client)

## 📁 Project Structure

```text
Websocket app/
├── server.py           # WebSocket broadcasting server
├── client.py           # Terminal/CLI-based client
├── gui_client.py       # Desktop Tkinter GUI client
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
## Known Limitations

This project is an exercise, so some things are intentionally simple:

- **No authentication:** Anyone who can reach the server's port can join the chat.
- **Usernames are not verified:** Each client chooses its own name and the server relays it as-is, so one user can pretend to be another.
- **No encryption:** Messages travel over plain `ws://`, not `wss://`, so they are not private on an untrusted network.
- **Local use only:** The server binds to `127.0.0.1` and the clients connect to the same hardcoded address. Chatting across machines requires changing the address.
- **No message history:** Messages are not saved. A client that joins late sees only new messages.
- **No automatic reconnect:** If the server goes down, clients must be restarted manually.
- **Single chat room:** All connected clients share one room, with no private messages or channels.
- **Basic input checks only:** Empty and oversized messages are filtered, but there is no rate limiting, so one client could still flood the chat.
- **Terminal prompt display:** In the terminal client, an incoming message can interrupt text you are typing.

## Possible Future Improvements

- Have the server assign and attach usernames instead of trusting the client
- Use JSON messages instead of plain `"name: text"` strings
- Add TLS (`wss://`) and a simple login or token
- Add reconnect logic, message history, and private messages
- Add rate limiting and logging
