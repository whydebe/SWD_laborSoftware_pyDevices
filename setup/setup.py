import os
import sys
import time
import subprocess
import requests
import winshell # + pip install pywin32
from colorama import Fore


source_urls = [
    'https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices_Server/main/dist/server.exe',
    'https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices_Server/main/server.py',
    'https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices_Server/main/config/config.json'
]

paths = [
    os.path.join(os.getcwd(), 'pyDeviceServer'),
    os.path.join(os.getcwd(), 'pyDeviceServer', 'config')
]

def print_ascii_art():
    print(f'''
    {Fore.BLUE}██████  ██    ██ ██████  ███████ ██    ██ ██  ██████ ███████     ███████ ███████ ████████ ██    ██ ██████  {Fore.RESET}
    {Fore.CYAN}██   ██  ██  ██  ██   ██ ██      ██    ██ ██ ██      ██          ██      ██         ██    ██    ██ ██   ██ {Fore.RESET}
    {Fore.WHITE}██████    ████   ██   ██ █████   ██    ██ ██ ██      █████       ███████ █████      ██    ██    ██ ██████  {Fore.RESET}
    {Fore.LIGHTRED_EX}██         ██    ██   ██ ██       ██  ██  ██ ██      ██               ██ ██         ██    ██    ██ ██  {Fore.RESET}
    {Fore.RED}██         ██    ██████  ███████   ████   ██  ██████ ███████     ███████ ███████    ██     ██████  ██  {Fore.RESET}
    ''')

    print(f'{Fore.LIGHTBLACK_EX}    Made by: {Fore.RESET}{Fore.LIGHTMAGENTA_EX}whydebe{Fore.RESET}')


def menu_main():
    operation = input(f'''
            {Fore.RED}What do you want to do? - Choose the option by entering the specific number{Fore.RESET}
            {Fore.BLUE}[1] Auto-Setup (Chocolatey, VLC + Setup of server.exe) + Start
            {Fore.LIGHTBLACK_EX}[2] Manual Setup (WIP){Fore.BLUE}
            {Fore.LIGHTBLACK_EX}[3] Set config.json manually (WIP){Fore.BLUE}
            {Fore.LIGHTBLACK_EX}[4] Uninstall (but not the setup.exe) (WIP){Fore.BLUE}
            {Fore.LIGHTRED_EX}[5] Exit
            {Fore.RESET}
    > ''')

    if str(operation) == "1":
        clear_console()
        print_ascii_art()
        print('\n')
        install_chocolatey_with_elevation()
        install_required_software_with_elevation()
        create_folder(paths[0])
        create_folder(paths[1])
        download_file(source_urls[0], paths[0])
        download_file(source_urls[2], paths[1])
        add_to_autostart(source_urls[0], paths[0])
        show_ip()
        start_server_exe(source_urls[0], paths[0])
        # return_to_menu_main()
    elif str(operation) == "2":
        clear_console()
        print_ascii_art()
        menu_install() # WIP (not to be used yet)
        print('\n')
    elif str(operation) == "3":
        clear_console()
        print_ascii_art()
        set_config_manually()
        print('\n') 
    elif str(operation) == "4":
        return_to_menu_main()
    elif str(operation) == "5":
        exit_program()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\n{Fore.LIGHTRED_EX}[ERROR]{Fore.RESET} {Fore.YELLOW}Incorrect option ... returning back to main menu{Fore.RESET}')
        time.sleep(2)
        return_to_menu_main()


# Menu for the installation options
def menu_install():
    operation = input(f'''
            {Fore.RED}
            Choose your preferred install way (both work without any further adjustments needed):
            {Fore.RESET}

            {Fore.LIGHTBLACK_EX}[1] Install via {Fore.LIGHTCYAN_EX}server.exe{Fore.LIGHTBLACK_EX} (+ add shortcut to Win-Autostart)
            {Fore.LIGHTBLACK_EX}[2] Install via {Fore.LIGHTCYAN_EX}server.py{Fore.LIGHTBLACK_EX} (+ add .bat shortcut to Win-Autostart)
            {Fore.BLUE}[3] Return to main menu
            {Fore.LIGHTRED_EX}[4] Exit{Fore.RESET}
    > ''')

    if str(operation) == "1":
        clear_console()
        print_ascii_art()
        menu_install()
        print('\n')
    elif str(operation) == "2":
        clear_console()
        print_ascii_art()
        menu_install()
        print('\n')
    elif str(operation) == "3":
        clear_console()
        print_ascii_art()
        menu_main()
        print('\n')  
    elif str(operation) == "4":
        exit_program()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\n{Fore.LIGHTRED_EX}[ERROR]{Fore.RESET} {Fore.YELLOW}Incorrect option ... returning back to main menu{Fore.RESET}')
        time.sleep(2)
        return_to_menu_main()


# Menu for the manual config.json editing/adding
def menu_manual_config():
    operation = input(f'''
            {Fore.RED}
            Choose a device name and add/change the supported file-types (e.g.: .jpg, .png, ...):
            {Fore.RESET}

            {Fore.BLUE}[1] Change {Fore.LIGHTCYAN_EX}device name{Fore.RESET}
            {Fore.BLUE}[2] Install via {Fore.LIGHTCYAN_EX}file-types{Fore.RESET}
            {Fore.BLUE}[3] Return to main menu{Fore.RESET}
            {Fore.LIGHTRED_EX}[4] Exit{Fore.RESET}
    > ''')

    if str(operation) == "1":
        clear_console()
        print_ascii_art()
        menu_manual_config()
        print('\n')
    elif str(operation) == "2":
        clear_console()
        print_ascii_art()
        menu_manual_config()
        print('\n')
    elif str(operation) == "3":
        clear_console()
        print_ascii_art()
        menu_main()
        print('\n')
    elif str(operation) == "4":
        exit_program()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\n{Fore.LIGHTRED_EX}[ERROR]{Fore.RESET} {Fore.YELLOW}Incorrect option ... returning back to main menu{Fore.RESET}')
        time.sleep(2)
        return_to_menu_main()



# --------------- INSTALLATION ---------------

# Install Chocolatey with elevated command shell/admin rights
def install_chocolatey_with_elevation():
    # Check if Chocolatey is already installed
    if not is_chocolatey_installed():
        # Download and run the Chocolatey installation script with elevation
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Downloading Chocolatey installation script...')
        subprocess.call(["powershell", "-Command", "Start-Process", "powershell", "-Verb", "RunAs", "-ArgumentList", "'-NoProfile -ExecutionPolicy Bypass -Command iex ((New-Object System.Net.WebClient).DownloadString(''https://chocolatey.org/install.ps1''))'"])

        # Verify installation
        if is_chocolatey_installed():
            print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Chocolatey installed successfully!')
        else:
            print(f'[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to install Chocolatey.')
    else:
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Chocolatey is already installed on your system.')

# Install required programs with elevated command shell/admin rights
def install_required_software_with_elevation():
    # Check if Chocolatey is installed
    if is_chocolatey_installed():
        # Use Chocolatey to install VLC Media Player with elevation
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Installing VLC Media Player via Chocolatey...')
        subprocess.call(["powershell", "-Command", "Start-Process", "choco", "-Verb", "RunAs", "-ArgumentList", "'install vlc -y'"])

        # Verify installation of all required software
        if is_required_software_installed():
            print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] VLC Media Player installed successfully!')
        else:
            print(f'[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to install VLC Media Player.')
    else:
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Chocolatey is not installed on your system. Please install Chocolatey first.')

# Check if chocolatey is already installed
def is_chocolatey_installed():
    # Check if Chocolatey is in the PATH environment variable
    return any(os.access(os.path.join(path, 'choco.exe'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))

# Check if all required software is installed (VLC only at the moment)
def is_required_software_installed():
    # Check if VLC Media Player is in the PATH environment variable
    return any(os.access(os.path.join(path, 'vlc.exe'), os.X_OK) for path in os.environ["PATH"].split(os.pathsep))



# ---- FOLDER, DOWNLOAD, CONFIG & SHORTCUT ---

# Create a folder-path
def create_folder(path):
    try:
        os.makedirs(path)
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Folder created successfully at path: {path}')
    except FileExistsError:
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Folder already exists at path: {path}. Continuing...')
    except Exception as e:
        print(f'[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to create folder at path: {path}. Error: {str(e)}')

# Download file from url and save it to a specific path
def download_file(url, path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = url.split('/')[-1]
            file_path = os.path.join(path, file_name)
            # print(f'-----> URL: {filename} / PATH: {file_path} / STATUS: {response.status_code}')
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] File downloaded successfully from URL: {url} and saved at path: {path}')
        else:
            print(f'Error downloading {url} (HTTP {response.status_code})')
    except Exception as e:
        print(f'[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to download file from URL: {url} and&/or save at path: {path}. Error: {str(e)}')

# Add file path to autostart in Windows
def add_to_autostart(url, path):
    file_name = url.split('/')[-1]
    file_path = os.path.join(path, file_name)
    try:
        startup_folder = winshell.startup()
        shortcut_path = os.path.join(startup_folder, f'{file_name}.lnk')
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = file_path
            shortcut.write()
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] File added to Windows Autostart successfully!')
    except Exception as e:
        print(f'[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to add file to Windows Autostart. Error: {str(e)}')

# Start server.exe
def start_server_exe(url, path):
    file_name = url.split('/')[-1]
    file_path = os.path.join(path, file_name)
    try:
        subprocess.Popen(file_path)
        print(f'[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Executable file started successfully: {file_path}')
    except Exception as e:
        print(f'[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to start executable file: {file_path}. Error: {str(e)}')
    

# Show IP-Adress of the Device (local + public)
def show_ip():
    os.system('ipconfig') # Not IDEAL -> TBC
    time.sleep(20)



# -------------- MANUALLY CONFIG --------------

def set_config_manually():
    return

def save_config_manually():
    return

def read_config_manually():
    return


# --------------- OTHER FUNCTIONS ---------------

# Clear console output
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Return to main menu
def return_to_menu_main():
    # operation = input(f'{Fore.LIGHTGREEN_EX}Press any key to return to the main menu...{Fore.RESET}')
    print_ascii_art()
    menu_main()
    print('\n')

# Exit the program
def exit_program():
    print('\n')
    print(f'{Fore.LIGHTGREEN_EX}Exiting the program...{Fore.RESET}')
    time.sleep(3)
    sys.exit()


# --------------- MAIN PROGRAM ---------------

def main():
    clear_console()
    print_ascii_art()
    menu_main()


if __name__ == "__main__":
    main()
