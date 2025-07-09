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

### 1. Windows .exe (for Users)

1. Download or clone the repo and navigate to the `dist/AutoClicker/` folder.
2. If you downloaded a ZIP, extract it to preserve the folder structure.
3. Double-click **AutoClicker.exe** (it lives inside `dist/AutoClicker/`).

> No Python or extra dependencies are required—just run the EXE.

### 2. From Source (for Developers)

1. Clone the repo:

   ```bash
   git clone https://github.com/vxnquish/AutoClicker.git
   cd AutoClicker
   ```
2. (Optional) Install custom fonts:

   * Place `GmarketSansTTFBold.ttf`, `GmarketSansTTFLight.ttf`, and `GmarketSansTTFMedium.ttf` into a local `fonts/` folder, or download them from [Google Fonts](https://fonts.google.com/).
3. Install Python dependencies:

   ```bash
   pip install pyautogui keyboard
   ```
4. Run the application:

   ```bash
   python main.py
   ```

---

## Usage

1. Launch the app (via `AutoClicker.exe` or `python main.py`).
2. Configure your desired:

   * **Base Interval** (seconds)
   * **Random Range** (± seconds)
   * **Click Count** (or check **Infinite Clicks**)
3. Click **▶️ Start Clicking** or press **F6** to begin.
4. Move your cursor anywhere: the app will click at the cursor's current position each interval.
5. Click **⏹️ Stop Clicking** or press **F6** again to stop.

---

## Packaging (for Developers)

To build your own standalone Windows EXE with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --clean --onedir --windowed --name AutoClicker \
  --add-data "fonts/GmarketSansTTFBold.ttf;fonts" \
  --add-data "fonts/GmarketSansTTFLight.ttf;fonts" \
  --add-data "fonts/GmarketSansTTFMedium.ttf;fonts" \
  --hidden-import keyboard \
  --hidden-import pyautogui \
  main.py
```

This will produce a **`dist/AutoClicker/AutoClicker.exe`** (with its `fonts/` subfolder) that users can run directly.

---

## License

MIT License. Feel free to fork and modify!
