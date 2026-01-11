import tkinter as tk
from tkinter import ttk
import time

# ---------- Main Window ----------
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="#f4f6f8")

# ---------- Variables ----------
sample_sentence = "Python is an easy and powerful programming language."
start_time = None
timer_running = False

# ---------- Functions ----------
def start_timer(event=None):
    global start_time, timer_running
    if start_time is None:
        start_time = time.time()
        timer_running = True
        update_timer()

def update_timer():
    if timer_running:
        elapsed = round(time.time() - start_time, 2)
        timer_label.config(text=f"Time Elapsed: {elapsed} sec")
        update_live_stats()
        root.after(100, update_timer)

def highlight_errors():
    typed = text_box.get("1.0", "end-1c")
    text_box.tag_remove("mistake", "1.0", "end")
    for i in range(min(len(typed), len(sample_sentence))):
        if typed[i] != sample_sentence[i]:
            idx = f"1.{i}"
            text_box.tag_add("mistake", idx, f"{idx}+1c")
    text_box.tag_config("mistake", foreground="red")

def calculate_stats():
    typed_text = text_box.get("1.0", "end-1c")
    if start_time is None or len(typed_text.strip()) == 0:
        return 0, 0
    time_taken = max(time.time() - start_time, 1e-5)
    words = typed_text.split()
    wpm = round((len(words) / time_taken) * 60)
    correct_chars = sum(1 for i in range(min(len(typed_text), len(sample_sentence)))
                        if typed_text[i] == sample_sentence[i])
    accuracy = round((correct_chars / len(sample_sentence)) * 100)
    return wpm, accuracy

def update_live_stats(event=None):
    wpm, accuracy = calculate_stats()
    live_label.config(text=f"Live WPM: {wpm} | Accuracy: {accuracy}%")

def submit_test():
    global timer_running
    timer_running = False
    wpm, accuracy = calculate_stats()
    time_taken = round(time.time() - start_time, 2)
    result_label.config(
        text=f"WPM: {wpm} | Accuracy: {accuracy}% | Time Taken: {time_taken} sec"
    )

def reset_test():
    global start_time, timer_running
    start_time = None
    timer_running = False
    text_box.delete("1.0", "end")
    result_label.config(text="WPM: 0 | Accuracy: 0% | Time Taken: 0 sec")
    live_label.config(text="Live WPM: 0 | Accuracy: 0%")
    timer_label.config(text="Time Elapsed: 0 sec")

# ---------- Styles ----------
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=8)

# ---------- Header ----------
header = tk.Label(
    root,
    text="Typing Speed Test Application",
    font=("Segoe UI", 18, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=15
)
header.pack(fill="x")

# ---------- Card ----------
card = tk.Frame(root, bg="white", bd=1, relief="solid")
card.place(relx=0.5, rely=0.55, anchor="center", width=600, height=450)

# ---------- Timer ----------
timer_label = tk.Label(
    card,
    text="Time Elapsed: 0 sec",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#2980b9"
)
timer_label.pack(pady=5)

# ---------- Sample Text ----------
sample_label = tk.Label(
    card,
    text=sample_sentence,
    wraplength=500,
    font=("Segoe UI", 11),
    bg="#ecf0f1",
    fg="#2c3e50",
    padx=15,
    pady=10
)
sample_label.pack(pady=10)

# ---------- Text Box ----------
text_box = tk.Text(
    card,
    height=4,
    font=("Segoe UI", 11),
    wrap="word",
    bd=1,
    relief="solid"
)
text_box.pack(padx=20, pady=10, fill="x")
text_box.bind("<KeyPress>", start_timer)
text_box.bind("<KeyRelease>", lambda e: [highlight_errors(), update_live_stats()])

# ---------- Buttons ----------
btn_frame = tk.Frame(card, bg="white")
btn_frame.pack(pady=10)

submit_btn = ttk.Button(btn_frame, text="Submit", command=submit_test, cursor="hand2")
submit_btn.grid(row=0, column=0, padx=10)

reset_btn = ttk.Button(btn_frame, text="Reset", command=reset_test, cursor="hand2")
reset_btn.grid(row=0, column=1, padx=10)

# ---------- Live Stats ----------
live_label = tk.Label(
    card,
    text="Live WPM: 0 | Accuracy: 0%",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#c0392b"
)
live_label.pack(pady=5)

# ---------- Result ----------
result_label = tk.Label(
    card,
    text="WPM: 0 | Accuracy: 0% | Time Taken: 0 sec",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#27ae60",
    wraplength=550
)
result_label.pack(pady=10)

# ---------- Footer ----------
footer = tk.Label(
    root,
    text="Developed using Python & Tkinter",
    font=("Segoe UI", 9),
    bg="#f4f6f8",
    fg="#777"
)
footer.pack(side="bottom", pady=10)

root.mainloop()
