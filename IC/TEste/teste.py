import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import calendar
from datetime import datetime


conn = sqlite3.connect("calendar.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    event TEXT NOT NULL
)
""")
conn.commit()


BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#cce5ff"
HEADER_COLOR = "#004085"
TEXT_COLOR = "#ffffff"


def add_event(date):
    def save_event():
        event_text = event_entry.get()
        if event_text:
            c.execute("INSERT INTO events (date, event) VALUES (?, ?)", (date, event_text))
            conn.commit()
            messagebox.showinfo("Sucesso", "Evento salvo com sucesso!")
            event_window.destroy()
            update_calendar()
    
    event_window = tk.Toplevel(root)
    event_window.title(f"Adicionar Evento - {date}")
    event_window.configure(bg=BG_COLOR)
    tk.Label(event_window, text=f"Evento para {date}:", bg=BG_COLOR).pack(pady=5)
    event_entry = tk.Entry(event_window, width=40)
    event_entry.pack(pady=5)
    tk.Button(event_window, text="Salvar", command=save_event, bg=BUTTON_COLOR).pack(pady=5)


def update_calendar():
    for widget in calendar_frame.winfo_children():
        widget.destroy()
    
    year, month = datetime.now().year, datetime.now().month
    cal = calendar.monthcalendar(year, month)
    
    
    headers = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    for i, day in enumerate(headers):
        label = tk.Label(calendar_frame, text=day, bg=HEADER_COLOR, fg=TEXT_COLOR, font=("Arial", 12, "bold"), width=10, height=2)
        label.grid(row=0, column=i, padx=2, pady=2)
    
    
    for row_idx, week in enumerate(cal, start=1):
        for col_idx, day in enumerate(week):
            if day == 0:
                label = tk.Label(calendar_frame, text="", width=10, height=4, bg=BG_COLOR)
                label.grid(row=row_idx, column=col_idx, padx=2, pady=2)
            else:
                date = f"{year}-{month:02d}-{day:02d}"
                btn = tk.Button(calendar_frame, text=str(day), command=lambda d=date: add_event(d), bg=BUTTON_COLOR, width=10, height=4)
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)

root = tk.Tk()
root.title("Calendário Interativo")
root.configure(bg=BG_COLOR)

calendar_frame = tk.Frame(root, bg=BG_COLOR)
calendar_frame.pack(pady=10)
update_calendar()

root.mainloop()

conn.close()
