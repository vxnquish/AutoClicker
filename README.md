# AutoClicker by @vxnquish

A simple, modern GUI application for automated mouse clicking with configurable intervals, randomization, and click counts.

---

## Features

* **Custom Interval**: Set a base interval (in seconds) and a random ± range.
* **Click Count**: Specify the number of clicks or enable infinite clicking.
* **Hotkey Toggle**: Press **F6** to start/stop without focusing the window.
* **Sleek UI**: Dark-themed, responsive layout built with Tkinter.

---

## Installation

### 1. Windows .exe (for Users)

1. Download `main.exe` from the dist folder.
2. Unzip (if zipped) and double-click **main.exe**.

> No Python or extra dependencies are required—just run the EXE.

### 2. From Source (for Developers)

1. Clone the repo:

   ```bash
   git clone https://github.com/vxnquish/AutoClicker.git
   cd AutoClicker
   ```
2. (Optional) Install custom fonts:

   * Download from [Google Fonts](https://fonts.google.com/)
3. Install Python dependencies:

   ```bash
   pip install pyautogui keyboard
   ```
4. Run the application:

   ```bash
   python autoclicker_app.py
   ```

---

## Usage

1. Launch the app (by the `.exe` or `python main.py`).
2. Configure your desired:

   * **Base Interval** (seconds)
   * **Random Range** (± seconds)
   * **Click Count** (or check **Infinite Clicks**)
3. Click **▶️ Start Clicking** or press **F6** to begin.
4. Move your cursor anywhere: the app will click at the cursor's current position each interval.
5. Click **⏹️ Stop Clicking** or press **F6** again to stop.

---

## Packaging (for developers)

To create a standalone Windows EXE:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The generated **main.exe** will appear in the `dist/` folder. Users can run it directly—no Python needed.

---

## License

MIT License. Feel free to fork and modify! -@vxnquish
