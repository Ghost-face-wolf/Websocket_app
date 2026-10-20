import tkinter as tk
from tkinter import ttk, scrolledtext
import asyncio
import threading
import websockets

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WebSocket Chat Client")
        self.root.geometry("450x550")
        self.root.minsize(350, 400)

        self.ws = None
        self.loop = None

        self._build_ui()
        threading.Thread(target=self._start_network_thread, daemon=True).start()

    def _build_ui(self):
        # Top Bar
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = ttk.Entry(top_frame, width=12)
        self.username_entry.insert(0, "User1")
        self.username_entry.pack(side=tk.LEFT, padx=(5, 15))

        self.status_label = ttk.Label(top_frame, text="Connecting...", foreground="orange")
        self.status_label.pack(side=tk.RIGHT)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # Bottom Input
        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(fill=tk.X)

        self.msg_entry = ttk.Entry(bottom_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = ttk.Button(bottom_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

    def _start_network_thread(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._listen_to_server())

    async def _listen_to_server(self):
        uri = "ws://127.0.0.1:8765"
        try:
            async with websockets.connect(uri) as ws:
                self.ws = ws
                self.root.after(0, self._set_status, "Connected", "green")

                async for message in ws:
                    self.root.after(0, self._append_raw, f"{message}\n")

        except Exception as e:
            self.root.after(0, self._append_raw, f"[System Error]: {e}\n")
        finally:
            self.ws = None
            self.root.after(0,self._set_status,"Disconnected","red")
    def _set_status(self, text, color):
        self.status_label.config(text=text, foreground=color)

    def _append_raw(self, line):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, line)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self):
        text = self.msg_entry.get().strip()
        username = self.username_entry.get().strip() or "User"

        if text and self.ws and self.loop:
            # Plain string format: "Username: message"
            payload = f"{username}: {text}"
            asyncio.run_coroutine_threadsafe(self.ws.send(payload), self.loop)
            self.msg_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
