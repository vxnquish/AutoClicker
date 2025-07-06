import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import random
import keyboard
import sys

class AutoClickerApp:
    """
    A modern GUI application for automated clicking with customizable intervals and counts.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker by @vxnquish")
        self.root.geometry("500x750")
        self.root.resizable(False, False)

        # Color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'surface': '#2d2d2d',
            'primary': '#007acc',
            'primary_hover': '#005a9e',
            'secondary': '#4a4a4a',
            'success': '#28a745',
            'success_hover': '#218838',
            'danger': '#dc3545',
            'danger_hover': '#c82333',
            'text': '#ffffff',
            'text_secondary': '#b0b0b0',
            'accent': '#ffd700',
            'border': '#404040'
        }

        self.clicking = False
        self.click_thread = None

        self._configure_styles()
        self._build_gui()
        self._setup_hotkeys()
        self._center_window()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _configure_styles(self):
        """Configure the visual styles for the application."""
        self.root.configure(bg=self.colors['bg'])

    def _create_section_frame(self, parent, title, icon=""):
        """Create a styled section frame with centered title."""
        section_frame = tk.Frame(parent, bg=self.colors['surface'], relief='solid', bd=1)
        section_frame.pack(fill='x', pady=15, padx=30)
        title_frame = tk.Frame(section_frame, bg=self.colors['surface'], height=50)
        title_frame.pack(fill='x', pady=(15, 10))
        title_frame.pack_propagate(False)
        title_label = tk.Label(title_frame,
                              text=f"{icon} {title}",
                              font=('Segoe UI', 14, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['surface'])
        title_label.pack(anchor='center')
        content_frame = tk.Frame(section_frame, bg=self.colors['surface'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        return content_frame

    def _build_gui(self):
        """Build the main GUI with improved centering and styling."""
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill='both', expand=True)

        header = tk.Frame(main, bg=self.colors['bg'], height=120)
        header.pack(fill='x', pady=(30, 20))
        header.pack_propagate(False)
        title_label = tk.Label(header,
                              text="🖱️ AutoClicker",
                              font=('Segoe UI', 26, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(anchor='center', pady=(15, 5))
        subtitle_label = tk.Label(header,
                                 text="by @vxnquish",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(anchor='center')

        config_frame = self._create_section_frame(main, "Configuration", "⚙️")
        input_container = tk.Frame(config_frame, bg=self.colors['surface'])
        input_container.pack(anchor='center', pady=10)

        tk.Label(input_container,
                text="Base Interval (s):",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['surface']).grid(row=0, column=0, sticky='w', padx=(0, 20), pady=(0, 5))
        self.interval_var = tk.StringVar(value="1.0")
        interval_entry = tk.Entry(input_container,
                                  textvariable=self.interval_var,
                                  font=('Segoe UI', 11),
                                  bg=self.colors['secondary'],
                                  fg=self.colors['text'],
                                  insertbackground=self.colors['text'],
                                  relief='flat', bd=0, width=15)
        interval_entry.grid(row=1, column=0, sticky='w', padx=(0, 20), pady=(0, 15))

        tk.Label(input_container,
                text="Random Range ± (s):",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['surface']).grid(row=0, column=1, sticky='w', pady=(0, 5))
        self.range_var = tk.StringVar(value="0.2")
        range_entry = tk.Entry(input_container,
                                textvariable=self.range_var,
                                font=('Segoe UI', 11),
                                bg=self.colors['secondary'],
                                fg=self.colors['text'],
                                insertbackground=self.colors['text'],
                                relief='flat', bd=0, width=15)
        range_entry.grid(row=1, column=1, sticky='w', pady=(0, 15))

        count_container = tk.Frame(config_frame, bg=self.colors['surface'])
        count_container.pack(anchor='center', pady=10)
        tk.Label(count_container,
                text="Click Count:",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['surface']).pack(anchor='center', pady=(0, 5))
        count_input_frame = tk.Frame(count_container, bg=self.colors['surface'])
        count_input_frame.pack(anchor='center')

        self.count_var = tk.StringVar(value="10")
        count_entry = tk.Entry(count_input_frame,
                                textvariable=self.count_var,
                                font=('Segoe UI', 11),
                                bg=self.colors['secondary'],
                                fg=self.colors['text'],
                                insertbackground=self.colors['text'],
                                relief='flat', bd=0, width=15)
        count_entry.pack(side='left', padx=(0, 15))

        self.infinite_var = tk.BooleanVar()
        infinite_check = tk.Checkbutton(count_input_frame,
                                        text="Infinite Clicks",
                                        variable=self.infinite_var,
                                        font=('Segoe UI', 11),
                                        fg=self.colors['text'],
                                        bg=self.colors['surface'],
                                        selectcolor=self.colors['secondary'],
                                        activebackground=self.colors['surface'],
                                        activeforeground=self.colors['text'])
        infinite_check.pack(side='left')

        self.interval_info = tk.Label(config_frame,
                                      text="",
                                      font=('Segoe UI', 9, 'italic'),
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['surface'])
        self.interval_info.pack(anchor='center', pady=(15, 0))
        self.interval_var.trace('w', self._update_interval_info)
        self.range_var.trace('w', self._update_interval_info)
        self._update_interval_info()

        controls_frame = self._create_section_frame(main, "Controls", "🎮")
        btn_container = tk.Frame(controls_frame, bg=self.colors['surface'])
        btn_container.pack(anchor='center', pady=20)

        self.start_btn = tk.Button(btn_container,
                                   text="▶️ Start Clicking",
                                   command=self._start_clicking,
                                   font=('Segoe UI', 12, 'bold'),
                                   fg=self.colors['text'],
                                   bg=self.colors['success'],
                                   activebackground=self.colors['success_hover'],
                                   activeforeground=self.colors['text'],
                                   relief='flat', bd=0, cursor='hand2',
                                   width=18, height=2)
        self.start_btn.pack(side='left', padx=(0, 15))

        self.stop_btn = tk.Button(btn_container,
                                  text="⏹️ Stop Clicking",
                                  command=self._stop_clicking,
                                  font=('Segoe UI', 12, 'bold'),
                                  fg=self.colors['text'],
                                  bg=self.colors['danger'],
                                  activebackground=self.colors['danger_hover'],
                                  activeforeground=self.colors['text'],
                                  relief='flat', bd=0, cursor='hand2',
                                  width=18, height=2, state='disabled')
        self.stop_btn.pack(side='left')

        hotkey_label = tk.Label(controls_frame,
                                 text="💡 Press F6 to toggle start/stop",
                                 font=('Segoe UI', 10, 'italic'),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['surface'])
        hotkey_label.pack(anchor='center', pady=(10, 0))

    def _setup_hotkeys(self):
        """Register F6 hotkey for start/stop toggle."""
        try:
            keyboard.add_hotkey('f6', self._toggle_clicking)
        except Exception:
            messagebox.showwarning("Hotkey Warning", "Could not register F6 hotkey. Try running as administrator if needed.")

    def _center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _update_interval_info(self, *args):
        """Update the interval information display."""
        try:
            base = float(self.interval_var.get())
            rng = float(self.range_var.get())
            min_interval = max(0.1, base - rng)
            max_interval = base + rng
            self.interval_info.config(text=f"⏱️ Clicks will occur between {min_interval:.2f}s and {max_interval:.2f}s intervals")
        except ValueError:
            self.interval_info.config(text="⚠️ Please enter valid numeric values")

    def _toggle_clicking(self):
        """Toggle between start and stop clicking."""
        if not self.clicking:
            self._start_clicking()
        else:
            self._stop_clicking()

    def _start_clicking(self):
        """Start the clicking process."""
        try:
            base = float(self.interval_var.get())
            rng = float(self.range_var.get())
            if not self.infinite_var.get():
                count = int(self.count_var.get())
                if count <= 0:
                    raise ValueError("Click count must be positive")
            if base <= 0:
                raise ValueError("Base interval must be positive")
            if rng < 0:
                raise ValueError("Random range cannot be negative")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your inputs:\n{str(e)}")
            return

        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        self.clicking = True
        self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
        self.click_thread.start()

    def _click_loop(self):
        """Main clicking loop that runs in a separate thread."""
        try:
            base = float(self.interval_var.get())
            rng = float(self.range_var.get())
            max_clicks = int(self.count_var.get()) if not self.infinite_var.get() else float('inf')
        except ValueError:
            self.root.after(0, self._stop_clicking)
            return

        count = 0
        while self.clicking and count < max_clicks:
            try:
                # Click at current mouse position
                pyautogui.click()
                count += 1

                min_interval = max(0.1, base - rng)
                max_interval = base + rng
                interval = random.uniform(min_interval, max_interval)
                time.sleep(interval)

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Click Error", f"Error performing click: {str(e)}"))
                break

        self.root.after(0, self._stop_clicking)

    def _stop_clicking(self):
        """Stop the clicking process."""
        self.clicking = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def _on_closing(self):
        """Handle application closing."""
        self.clicking = False
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AutoClickerApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)
