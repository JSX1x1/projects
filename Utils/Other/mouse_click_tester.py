import tkinter as tk
import time

"""
Mouse Click Tester Tool
------------------------
Purpose:
- Detects unwanted double clicks from a mouse.
- Helps users identify faulty mouse behavior, such as unintended double clicks.
- Provides an adjustable threshold to fine-tune double-click detection.
- Displays results in a simple and user-friendly GUI.

How It Works:
- The user clicks inside the test field.
- If the second click occurs within the threshold time, it's considered a double click.
- The threshold can be adjusted using a slider (0.05s – 0.5s).
- Results are displayed in real-time.

Use Case:
- Ideal for diagnosing **mouse switch issues** or **configuring gaming mice**.
"""

class MouseClickTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Click Tester")
        self.root.geometry("400x300")

        self.last_click_time = 0
        self.double_click_threshold = 0.2  # 200ms default threshold

        self.label = tk.Label(root, text="Click inside the field", font=("Arial", 14))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(root, width=350, height=200, bg="lightgray")
        self.canvas.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.result_label.pack()

        self.threshold_slider = tk.Scale(
            root, from_=0.05, to=0.5, resolution=0.01, orient="horizontal",
            label="Double-click threshold (seconds)", length=300
        )
        self.threshold_slider.set(self.double_click_threshold)
        self.threshold_slider.pack(pady=10)

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.double_click_threshold = self.threshold_slider.get()
        current_time = time.time()
        if current_time - self.last_click_time < self.double_click_threshold:
            self.result_label.config(text="⚠️ Unwanted double click detected!", fg="red")
        else:
            self.result_label.config(text="Single click detected", fg="green")
        self.last_click_time = current_time

# Run the GUI
root = tk.Tk()
app = MouseClickTester(root)
root.mainloop()
