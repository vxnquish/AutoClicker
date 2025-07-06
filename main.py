import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import random
import keyboard
import sys

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Auto Clicker")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Variables
        self.clicking = False
        self.click_thread = None
        
        # Setup GUI
        self.setup_gui()
        
        # Setup hotkeys
        self.setup_hotkeys()
        
        # Center window
        self.center_window()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Auto Clicker", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Interval settings
        ttk.Label(main_frame, text="Base Interval (seconds):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.StringVar(value="1.0")
        self.interval_entry = ttk.Entry(main_frame, textvariable=self.interval_var, width=10)
        self.interval_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Range settings
        ttk.Label(main_frame, text="± Range (seconds):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.range_var = tk.StringVar(value="0.2")
        self.range_entry = ttk.Entry(main_frame, textvariable=self.range_var, width=10)
        self.range_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        # Info label for interval
        self.interval_info = ttk.Label(main_frame, text="", font=('Arial', 8), foreground='gray')
        self.interval_info.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Update interval info when values change
        self.interval_var.trace('w', self.update_interval_info)
        self.range_var.trace('w', self.update_interval_info)
        
        # Number of clicks
        ttk.Label(main_frame, text="Number of Clicks:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.StringVar(value="10")
        self.count_entry = ttk.Entry(main_frame, textvariable=self.count_var, width=10)
        self.count_entry.grid(row=4, column=1, padx=(10, 0), pady=5)
        
        # Infinite clicks checkbox
        self.infinite_var = tk.BooleanVar()
        self.infinite_check = ttk.Checkbutton(main_frame, text="Infinite clicks", variable=self.infinite_var)
        self.infinite_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start (F6)", command=self.toggle_clicking, width=12)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop (F6)", command=self.stop_clicking, width=12, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready to start", font=('Arial', 10))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.click_counter = ttk.Label(status_frame, text="Clicks: 0", font=('Arial', 10))
        self.click_counter.grid(row=1, column=0, sticky=tk.W)
        
        # Hotkey info
        hotkey_label = ttk.Label(main_frame, text="Hotkey: F6 (Start/Stop)", font=('Arial', 8), foreground='blue')
        hotkey_label.grid(row=9, column=0, columnspan=3, pady=(10, 0))
        
        # Initial interval info update
        self.update_interval_info()

    def setup_hotkeys(self):
        try:
            keyboard.add_hotkey('f6', self.toggle_clicking)
        except:
            messagebox.showwarning("Hotkey Warning", "Could not register F6 hotkey. You may need to run as administrator.")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def update_interval_info(self, *args):
        try:
            base_interval = float(self.interval_var.get())
            range_val = float(self.range_var.get())
            min_interval = base_interval - range_val
            max_interval = base_interval + range_val
            
            if min_interval < 0:
                min_interval = 0
            
            self.interval_info.config(text=f"Random interval: {min_interval:.1f}s - {max_interval:.1f}s")
        except ValueError:
            self.interval_info.config(text="Invalid interval values")

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if self.clicking:
            return
        
        try:
            base_interval = float(self.interval_var.get())
            range_val = float(self.range_var.get())
            count = int(self.count_var.get()) if not self.infinite_var.get() else float('inf')
            
            if base_interval <= 0:
                messagebox.showerror("Error", "Base interval must be greater than 0")
                return
            
            if count <= 0 and not self.infinite_var.get():
                messagebox.showerror("Error", "Number of clicks must be greater than 0")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
            return
        
        self.clicking = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # Start countdown
        self.status_label.config(text="Starting in 3 seconds...")
        self.root.after(1000, lambda: self.status_label.config(text="Starting in 2 seconds..."))
        self.root.after(2000, lambda: self.status_label.config(text="Starting in 1 second..."))
        self.root.after(3000, self.begin_clicking)

    def begin_clicking(self):
        if not self.clicking:
            return
        
        self.click_thread = threading.Thread(target=self.click_worker, daemon=True)
        self.click_thread.start()

    def click_worker(self):
        base_interval = float(self.interval_var.get())
        range_val = float(self.range_var.get())
        count = int(self.count_var.get()) if not self.infinite_var.get() else float('inf')
        
        clicks_made = 0
        
        while self.clicking and clicks_made < count:
            try:
                pyautogui.click()
                clicks_made += 1
                
                # Update GUI in main thread
                self.root.after(0, self.update_status, clicks_made, count)
                
                if clicks_made >= count:
                    break
                
                # Calculate random interval
                min_interval = max(0, base_interval - range_val)
                max_interval = base_interval + range_val
                sleep_time = random.uniform(min_interval, max_interval)
                
                time.sleep(sleep_time)
                
            except Exception as e:
                self.root.after(0, self.show_error, f"Error during clicking: {str(e)}")
                break
        
        # Finish
        self.root.after(0, self.clicking_finished)

    def update_status(self, clicks_made, total_clicks):
        if total_clicks == float('inf'):
            self.status_label.config(text="Clicking... (Infinite mode)")
            self.click_counter.config(text=f"Clicks: {clicks_made}")
        else:
            self.status_label.config(text=f"Clicking... ({clicks_made}/{int(total_clicks)})")
            self.click_counter.config(text=f"Clicks: {clicks_made}")

    def clicking_finished(self):
        self.clicking = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Clicking completed!")

    def stop_clicking(self):
        self.clicking = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Clicking stopped")

    def show_error(self, error_msg):
        messagebox.showerror("Error", error_msg)
        self.stop_clicking()

    def on_closing(self):
        self.clicking = False
        try:
            keyboard.unhook_all()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AutoClickerApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)