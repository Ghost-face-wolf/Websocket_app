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
