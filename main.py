import os
import time
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto import Desktop
from pywinauto.timings import Timings
from pywinauto.application import WindowSpecification
from fileHandler import copy_dat_file, clean_dat_file, compare_dat_to_expected

def init_escape(escape_path:str) -> Application:
    """
    Initialize the Escape application. Run the Escape.exe and connect to the main window.
    Args:
        EscapePath (str): Path to the Escape executable. Could be a relative or absolute path.
    Returns:
        Application: The initialized Escape application.
    """
    # Check if the path is valid
    if not os.path.exists(escape_path):
        raise FileNotFoundError(f"Escape executable not found at {escape_path}")
    # Start the application

    try:
        app = Application(backend="win32").start(r"..\escape32.exe")
        app = Application(backend="win32").connect(title_re="Welcome to Escape !")
        
    except Exception as e:
        print(f"Error initializing AutoIt: {e}")
        return None
    return app

def load_config_file(config_file_path:str, _mainWin: WindowSpecification, _app: Application ) -> None:
    """
    Load a configuration file into the Escape application from .ecf file.
    Args:
        file_path (str): Path to the configuration file. Could be a relative or absolute path.
    """
    # Set default timeouts for this function
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found at {config_file_path}")
    
    # Load the configuration file
    try:
        configBtn = _mainWin.child_window(title="Configure ", class_name="TButton")
        configBtn.click()
        conWin = Desktop(backend="win32").window(title_re=".*[Cc]onfiguration.*")
        conWin.menu_select("File->Open File...")
        file_dlg = _app.window(title_re=".*Load Configuration.*")  # Adjust title if needed
        file_dlg["Edit"].set_edit_text(config_file_path)
        file_dlg["Open"].click()
        conWin.close()
    except ElementNotFoundError:
        print("Configuration button not found (exception).")
    except Exception as e:
        print(f"Error loading configuration file: {e}")

def load_project_file(project_file_path:str, _MAWin: WindowSpecification) -> None:
    """
    Load a project file into the Escape application from .mpr file.
    Perquisite: The Escape application must be running and the Microprogrammed Architecture window must be open.
    Args:
        file_path (str): Path to the project file. Could be a relative or absolute path.
    """
    try:
        MAWindow.menu_select("File->Open Project")
        file_dlg = app.window(title_re=".*Load Microcode Project.*")  # Adjust title if needed
        file_dlg["Edit"].set_edit_text(r"..\zak_simple\soi.mpr")
        file_dlg["Open"].click()
    except ElementNotFoundError:
        print("Project button not found (exception).")
    except Exception as e:
        print(f"Error loading project file: {e}")

def set_breakpoint(_MAWin: WindowSpecification, breakpoint_addr:hex=0x000001FC) -> None:
    """
    Set a breakpoint in the Escape application.
    By default, it sets a breakpoint at address 0x000001FC, because this is the last possible address according to .ecf file.
    This function assumes that the Escape application is already running and the Microprogrammed Architecture window is open.
    It also assumes that the user has already loaded a project file.
    Args:
        _MAWin (WindowSpecification): The Microprogrammed Architecture window.
        breakpoint_addr (hex): The address to set the breakpoint at. Default is 0x000001FC.
    """
    try:
        _MAWin.menu_select("View->Breakpoints...")
        breakWin = Desktop(backend="win32").window(title_re=".*[Bb]reakpoints.*")
        # Select Organizational registers element
        org_reg = breakWin.child_window(title="Organisational Registers", class_name="TGroupBox")
        #select first TPanel of the group and list its children
        org_reg_panels = org_reg.children(class_name="TPanel")
        org_reg_panel = org_reg_panels[0] # TPanel 0 is set to PC by default, found by trial and error


        org_reg_panel.children(class_name="TEdit")[0].set_edit_text(f"0x{breakpoint_addr:08X}")  # Set the breakpoint address
        org_reg_panel.children(class_name="TCheckBox")[0].click()  # Click the "Set" button
        # Save with ctrl+S
        breakWin.type_keys('^s')  # Ctrl + S to save
        # Close the breakpoints window
        breakWin.close()

    except ElementNotFoundError:
        print("Breakpoints button not found (exception).")
    except Exception as e:
        print(f"Error opening breakpoints window: {e}")
        return

def set_cycles_options(_MAWin: WindowSpecification, cycles:int=100_000) -> None:
    """
    Set the number of cycles in the Escape application.
    By default, it sets the number of cycles to 100 000.
    This function assumes that the Escape application is already running and the Microprogrammed Architecture window is open.
    It also assumes that the user has already loaded a project file.
    Args:
        _MAWin (WindowSpecification): The Microprogrammed Architecture window.
        cycles (int): The number of cycles to set. Default is 1000.
    """
    try:
        _MAWin.child_window(class_name="TSpinEdit").set_edit_text(str(cycles))  # Set the number of cycles
        _MAWin.child_window(class_name="TCheckBox").click()  # Click the "Multiple Cycles" checkbox
    except ElementNotFoundError:
        print("Cycles options button not found (exception).")
  
def close_escape_popups() -> None:
    """
    Close any popups that may appear in the Escape application.
    This function assumes that the Escape application is already running.
    """
    try:
        # Retrieve all open windows
        windows = Desktop(backend="win32").windows()

        for win in windows:
            try:
                # Check if the window title contains "note"
                if "note" in win.window_text().lower():
                    child_windows = win.children()
                    for child in child_windows:
                        if child.window_text() == "Breakpoint condition met":
                            win.close()
                            break

            except Exception as e:
                print(f"Error while handling window: {e}")
                continue  # Proceed to the next window if an error occurs

    except Exception as e:
        print(f"Error retrieving windows: {e}")

def run_simulation(_MAWin: WindowSpecification, index:int) -> None:
    """
    Run the simulation in the Escape application.
    This function assumes that the Escape application is already running and the Microprogrammed Architecture window is open.
    It also assumes that the user has already loaded a project file and set the number of cycles.
    Args:
        _MAWin (WindowSpecification): The Microprogrammed Architecture window.
    """
    try:
        _MAWin.child_window(title="Reset", class_name="TButton").click()  # Click the "Run" button
        _MAWin.child_window(title="&Clock").click()  # Click the "Run" button
        # Wait for the simulation to finish, check if time field is set to 100_000
        time_field = _MAWin.child_window(class_name="TEditInteger")
        while True:
            time_field = _MAWin.child_window(class_name="TEditInteger")
            if int(time_field.window_text()) <= 100_000:
                break
            else:
                print("Waiting for simulation to finish...")
                close_escape_popups()
                time.sleep(0.1)
        #Type 
        close_escape_popups()
        _MAWin.type_keys('^s')  # Ctrl + S to save

        copy_dat_file(r"..\zak_simple\soi.dat", r"..\results\\" + f"result{index}.dat")
        # Compare the .dat file with the expected .dat file
        if compare_dat_to_expected(r"..\zak_simple\soi.dat", r"..\zak_simple\result.dat"):
            print("Simulation successful, .dat file matches expected result.")
        else:
            print("Simulation failed, .dat file does not match expected result.")

        # Clean the .dat file
        clean_dat_file(r"..\zak_simple\soi.dat", r"..\zak_simple\clean.dat")


    except ElementNotFoundError:
        print("Run button not found (exception).")
        return
Timings.after_clickinput_wait = 0
Timings.after_setfocus_wait = 0

start_tme = time.time()
app = init_escape(r"..\escape32.exe")
mainWin= app.window(title="Welcome to Escape !")
load_config_file(r"..\zak_simple\soi.ecf", mainWin, app)
mainWin.child_window(title="Microprogrammed Architecture", class_name="TButton").click()
MAWindow = Desktop(backend="win32").window(title_re=".*Microprogrammed Architecture.*")

load_project_file(r"..\zak_simple\soi.mpr", MAWindow)
set_breakpoint(MAWindow)
set_cycles_options(MAWindow)

run_simulation(MAWindow, 0)

# for i in range(1, 6):
#     run_simulation(MAWindow, i)
#     load_project_file(r"..\zak_simple\soi.mpr", MAWindow)
    
