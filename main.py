from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import Desktop
from pywinauto.timings import Timings
import time

Timings.after_clickinput_wait = 0
Timings.after_setfocus_wait = 0

start_time = time.time()
app = Application(backend="win32").start(r"..\escape32.exe")
app = Application(backend="win32").connect(title_re="Welcome to Escape !")

mainWin = app.window(title="Welcome to Escape !")

try:
    configBtn = mainWin.child_window(title="Configure ", class_name="TButton")
    if configBtn.exists(timeout=5):
        print("Configure button found. Clicking...")
        configBtn.click()
        conWin = Desktop(backend="win32").window(title_re=".*[Cc]onfiguration.*")
        conWin.menu_select("File->Open File...")
        file_dlg = app.window(title_re=".*Load Configuration.*")  # Adjust title if needed

        # Type the file path into the filename input
        file_dlg["Edit"].set_edit_text(r"..\zak_simple\soi.ecf")

        # Click the "Open" button
        file_dlg["Open"].click()
        conWin.close()
        end_time = time.time()
        print(f"Configuration loaded in {end_time - start_time:.2f} seconds.")

        try:
            time_start = time.time()
            MABtn = mainWin.child_window(title="Microprogrammed Architecture", class_name="TButton")
            MABtn.click()
            MAWindow = Desktop(backend="win32").window(title_re=".*Microprogrammed Architecture.*")
            MAWindow.menu_select("File->Open Project")
            file_dlg = app.window(title_re=".*Load Microcode Project.*")  # Adjust title if needed
            file_dlg["Edit"].set_edit_text(r"..\zak_simple\soi.mpr")
            file_dlg["Open"].click()
            MAWindow.print_control_identifiers(depth=3)
            time_end = time.time()
            print(f"Microprogrammed Architecture loaded in {time_end - time_start:.2f} seconds.")


        except ElementNotFoundError:
            print("Microprogrammed Architecture button not found (exception).")

        
        
    else:
        print("Configure button not found.")
except ElementNotFoundError:
    print("Configure button not found (exception).")

# win.print_control_identifiers(depth=3)

