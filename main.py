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
        # Initialize main window
        self.root = root
        self.root.title("AutoClicker by @vxnquish")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        
        # Set modern color scheme
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

        # Internal state flag for clicking
        self.clicking = False
        self.click_thread = None

        # Apply visual styles
        self._configure_styles()
        # Build and layout all widgets
        self._build_gui()
        # Setup global hotkey for start/stop
        self._setup_hotkeys()
        # Center the window on screen
        self._center_window()
        # Ensure clean shutdown
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _configure_styles(self):
        """
        Define modern dark theme styles.
        """
        # Base window background
        self.root.configure(bg=self.colors['bg'])
        
        style = ttk.Style()
        style.theme_use('clam')

        # Configure all styles with proper backgrounds
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       foreground=self.colors['text'],
                       background=self.colors['bg'])
        
        style.configure('Subtitle.TLabel', 
                       font=('Segoe UI', 11), 
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg'])
        
        style.configure('SectionTitle.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['accent'],
                       background=self.colors['surface'])
        
        style.configure('Info.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['text'],
                       background=self.colors['surface'])

        # Frames
        style.configure('Card.TFrame', 
                       background=self.colors['surface'], 
                       relief='flat', 
                       borderwidth=0)
        
        style.configure('Main.TFrame', 
                       background=self.colors['bg'], 
                       relief='flat', 
                       borderwidth=0)

        # Entries
        style.configure('Modern.TEntry', 
                       fieldbackground=self.colors['secondary'], 
                       borderwidth=2, 
                       relief='flat',
                       foreground=self.colors['text'],
                       insertcolor=self.colors['text'])
        
        style.map('Modern.TEntry',
                 focuscolor=[('!focus', self.colors['border']), ('focus', self.colors['primary'])])

        # Buttons
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['text'], 
                       background=self.colors['primary'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Primary.TButton', 
                 background=[('active', self.colors['primary_hover'])])
        
        style.configure('Success.TButton', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['text'], 
                       background=self.colors['success'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Success.TButton', 
                 background=[('active', self.colors['success_hover'])])
        
        style.configure('Danger.TButton', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['text'], 
                       background=self.colors['danger'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Danger.TButton', 
                 background=[('active', self.colors['danger_hover'])])

        # Checkbutton
        style.configure('Modern.TCheckbutton',
                       foreground=self.colors['text'],
                       background=self.colors['surface'],
                       focuscolor='none')

    def _create_section_frame(self, parent, title, icon=""):
        """
        Create a modern section frame with title.
        """
        frame = tk.Frame(parent, bg=self.colors['surface'], relief='flat', bd=0)
        frame.pack(fill='x', pady=(10, 5), padx=20)
        
        # Add subtle border
        border_frame = tk.Frame(frame, bg=self.colors['border'], height=1)
        border_frame.pack(fill='x', side='top')
        
        # Title with icon
        title_frame = tk.Frame(frame, bg=self.colors['surface'], height=40)
        title_frame.pack(fill='x', pady=(15, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text=f"{icon} {title}", 
                              font=('Segoe UI', 12, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['surface'])
        title_label.pack(side='left', pady=5)
        
        # Content frame
        content_frame = tk.Frame(frame, bg=self.colors['surface'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        return content_frame

    def _build_gui(self):
        """
        Construct and arrange all GUI components with modern design.
        """
        # Main container
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill='both', expand=True)

        # Header section
        header = tk.Frame(main, bg=self.colors['bg'], height=100)
        header.pack(fill='x', pady=(20, 10))
        header.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header, 
                              text="🖱️", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(header, 
                                 text="Customizable Auto Clicker", 
                                 font=('Segoe UI', 11),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg'])
        subtitle_label.pack()

        # Configuration section
        config_frame = self._create_section_frame(main, "Configuration", "⚙️")
        
        # Create grid for inputs
        input_grid = tk.Frame(config_frame, bg=self.colors['surface'])
        input_grid.pack(fill='x', pady=10)
        
        # Base interval
        tk.Label(input_grid, text="Base Interval (s)", 
                font=('Segoe UI', 10), fg=self.colors['text'],
                bg=self.colors['surface']).grid(row=0, column=0, sticky='w', padx=(0, 20), pady=(0, 5))
        
        self.interval_var = tk.StringVar(value="1.0")
        interval_entry = tk.Entry(input_grid, textvariable=self.interval_var, 
                                 font=('Segoe UI', 11), width=12,
                                 bg=self.colors['secondary'], fg=self.colors['text'],
                                 insertbackground=self.colors['text'], relief='flat', bd=2)
        interval_entry.grid(row=1, column=0, sticky='w', padx=(0, 20), pady=(0, 15))
        
        # Random range
        tk.Label(input_grid, text="Random Range ± (s)", 
                font=('Segoe UI', 10), fg=self.colors['text'],
                bg=self.colors['surface']).grid(row=0, column=1, sticky='w', padx=(0, 20), pady=(0, 5))
        
        self.range_var = tk.StringVar(value="0.2")
        range_entry = tk.Entry(input_grid, textvariable=self.range_var, 
                              font=('Segoe UI', 11), width=12,
                              bg=self.colors['secondary'], fg=self.colors['text'],
                              insertbackground=self.colors['text'], relief='flat', bd=2)
        range_entry.grid(row=1, column=1, sticky='w', pady=(0, 15))
        
        # Click count
        tk.Label(config_frame, text="Click Count", 
                font=('Segoe UI', 10), fg=self.colors['text'],
                bg=self.colors['surface']).pack(anchor='w', pady=(10, 5))
        
        count_frame = tk.Frame(config_frame, bg=self.colors['surface'])
        count_frame.pack(fill='x', pady=(0, 10))
        
        self.count_var = tk.StringVar(value="10")
        count_entry = tk.Entry(count_frame, textvariable=self.count_var, 
                              font=('Segoe UI', 11), width=15,
                              bg=self.colors['secondary'], fg=self.colors['text'],
                              insertbackground=self.colors['text'], relief='flat', bd=2)
        count_entry.pack(side='left', padx=(0, 15))
        
        self.infinite_var = tk.BooleanVar()
        infinite_check = tk.Checkbutton(count_frame, text="Infinite Clicks",
                                       variable=self.infinite_var, 
                                       font=('Segoe UI', 10),
                                       fg=self.colors['text'],
                                       bg=self.colors['surface'],
                                       selectcolor=self.colors['secondary'],
                                       activebackground=self.colors['surface'],
                                       activeforeground=self.colors['text'])
        infinite_check.pack(side='left')
        
        # Interval info
        self.interval_info = tk.Label(config_frame, text="", 
                                     font=('Segoe UI', 9, 'italic'),
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['surface'])
        self.interval_info.pack(pady=(10, 0))
        
        self.interval_var.trace('w', self._update_interval_info)
        self.range_var.trace('w', self._update_interval_info)
        self._update_interval_info()

        # Controls section
        controls_frame = self._create_section_frame(main, "Controls", "🎮")
        
        btn_container = tk.Frame(controls_frame, bg=self.colors['surface'])
        btn_container.pack(pady=20)
        
        # Start button
        start_btn = tk.Button(btn_container, text="▶️ Start Clicking", 
                             command=self._toggle_clicking,
                             font=('Segoe UI', 12, 'bold'),
                             fg=self.colors['text'],
                             bg=self.colors['success'],
                             activebackground=self.colors['success_hover'],
                             activeforeground=self.colors['text'],
                             relief='flat', bd=0, cursor='hand2',
                             width=15, height=2)
        start_btn.pack(side='left', padx=(0, 15))
        
        # Stop button
        stop_btn = tk.Button(btn_container, text="⏹️ Stop Clicking", 
                            command=self._stop_clicking,
                            font=('Segoe UI', 12, 'bold'),
                            fg=self.colors['text'],
                            bg=self.colors['danger'],
                            activebackground=self.colors['danger_hover'],
                            activeforeground=self.colors['text'],
                            relief='flat', bd=0, cursor='hand2',
                            width=15, height=2)
        stop_btn.pack(side='left')
        
        # Hotkey info
        hotkey_label = tk.Label(controls_frame, text="💡 Press F6 to toggle start/stop", 
                               font=('Segoe UI', 9, 'italic'),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['surface'])
        hotkey_label.pack(pady=(10, 0))

    def _setup_hotkeys(self):
        """
        Register F6 hotkey for start/stop.
        """
        try:
            keyboard.add_hotkey('f6', self._toggle_clicking)
        except Exception:
            messagebox.showwarning("Hotkey Warning", "Could not register F6 hotkey. Try running as administrator if needed.")

    def _center_window(self):
        """
        Center the window on screen.
        """
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _update_interval_info(self, *args):
        """
        Show min/max click interval.
        """
        try:
            base = float(self.interval_var.get())
            rng = float(self.range_var.get())
            min_interval = max(0.1, base - rng)
            max_interval = base + rng
            self.interval_info.config(text=f"⏱️ Clicks will occur between {min_interval:.2f}s and {max_interval:.2f}s intervals")
        except ValueError:
            self.interval_info.config(text="⚠️ Please enter valid numeric values")

    def _toggle_clicking(self):
        """
        Toggle clicking process.
        """
        if self.clicking:
            self._stop_clicking()
        else:
            self._start_clicking()

    def _start_clicking(self):
        """
        Validate inputs and start clicking.
        """
        try:
            base = float(self.interval_var.get())
            rng = float(self.range_var.get())
            total = int(self.count_var.get()) if not self.infinite_var.get() else float('inf')
            
            if base <= 0:
                raise ValueError("Base interval must be positive")
            if rng < 0:
                raise ValueError("Random range cannot be negative")
            if total <= 0 and total != float('inf'):
                raise ValueError("Click count must be positive")
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your inputs:\n{str(e)}")
            return
            
        self.clicking = True
        self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
        self.click_thread.start()

    def _click_loop(self):
        """
        Perform clicks at random intervals until done.
        """
        base = float(self.interval_var.get())
        rng = float(self.range_var.get())
        max_clicks = int(self.count_var.get()) if not self.infinite_var.get() else float('inf')
        count = 0
        
        while self.clicking and count < max_clicks:
            try:
                pyautogui.click()
                count += 1
                
                # Calculate random interval
                min_interval = max(0.1, base - rng)
                max_interval = base + rng
                interval = random.uniform(min_interval, max_interval)
                
                time.sleep(interval)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Click Error", f"Error performing click: {str(e)}"))
                break
        
        self.clicking = False

    def _stop_clicking(self):
        """
        Stop clicking immediately.
        """
        self.clicking = False

    def _on_closing(self):
        """
        Cleanup and exit.
        """
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