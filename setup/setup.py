import os
import sys
import time
import json
import socket
import platform
import subprocess
import requests
import winshell # + pip install pywin32
from colorama import Fore


source_urls = [
    'https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices/main/server/dist/server.exe',
    'https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices/main/server/server.py',
    'https://raw.githubusercontent.com/whydebe/SWD_laborSoftware_pyDevices/main/server/config/config.json'
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
            {Fore.BLUE}[1] Auto-Setup (Chocolatey, VLC + Setup of server.exe) + Start{Fore.RESET}
            {Fore.BLUE}[2] Set config.json manually{Fore.RESET}
            {Fore.LIGHTBLACK_EX}[3] Uninstall (but not the setup.exe) (WIP){Fore.RESET}
            {Fore.LIGHTRED_EX}[4] Exit{Fore.RESET}
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
        get_ipv4_address(paths[1])
        start_server_exe(source_urls[0], paths[0])
        # return_to_menu_main()
    elif str(operation) == "2":
        clear_console()
        print_ascii_art()
        menu_manual_config()
        print('\n')
    elif str(operation) == "3":
        return_to_menu_main()
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
            {Fore.RED}Choose a device name and add/change the supported file-types (e.g.: .jpg, .png, ...):{Fore.RESET}
            {Fore.BLUE}[1] Change {Fore.LIGHTCYAN_EX}device name & supported file types{Fore.RESET}
            {Fore.BLUE}[2] Return to main menu{Fore.RESET}
            {Fore.LIGHTRED_EX}[3] Exit{Fore.RESET}
    > ''')

    if str(operation) == "1":
        clear_console()
        print_ascii_art()
        check_config_file(paths[1])
        set_config_manually(paths[1])
        format_json(paths[1] + "config.json")
        menu_manual_config()
        print('\n')
    elif str(operation) == "2":
        clear_console()
        print_ascii_art()
        menu_main()
        print('\n')
    elif str(operation) == "3":
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

# Get local IPv4-Adress of the device
def get_ipv4_address(path):
    # Check if the directory structure exists, create if it doesn't
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Check if config.json file exists, create if it doesn't
    config_file = os.path.join(path, 'config.json')
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump({}, f, indent=4)
    
    # Get the IPv4 address
    try:
        hostname = socket.getfqdn()
        ip_address = socket.gethostbyname_ex(hostname)[2][1]
    except Exception as e:
        print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to retrieve IPv4 address: {str(e)}")
        return
    
    # Update config.json with the IPv4 address
    try:
        with open(config_file, 'r+') as f:
            config_data = json.load(f)
            config_data['ipv4_address'] = ip_address
            f.seek(0)
            json.dump(config_data, f, indent=4)
            f.truncate()
            print(f"[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] IPv4 address added to config.json: {ip_address}")
    except Exception as e:
        print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to update config.json with IPv4 address: {str(e)}")

# Start server.exe
def start_server_exe(url, path):
    file_name = url.split('/')[-1]
    file_path = os.path.join(path, file_name)
    
    if platform.system() == 'Windows':
        try:
            subprocess.call([f'{file_path}'])
            # subprocess.Popen(['start', file_path], shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # subprocess.run([sys.executable, "-c"], capture_output=True, text=True)
            # subprocess.Popen(['start', file_name], shell=True, cwd=path)
            print(f"[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Executable file started successfully: {file_path}")
        except Exception as e:
            print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to start executable file: {file_path}. Error: {str(e)}")
    else:
        print("[ERROR] This function is only supported on Windows devices.")


# -------------- MANUALLY CONFIG --------------

def check_config_file(path):
    config_file = os.path.join(path, 'config.json')
    
    if not os.path.exists(config_file):
        print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] config.json file not found in the specified directory: {path}")
    else:
        with open(config_file, 'r') as f:
            try:
                config_data = json.load(f)
                if 'device_type' not in config_data or 'supported_file_types' not in config_data:
                    create_config_manually(path)
                else:
                    print(f"[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] config.json file exists and contains required entries.")
            except Exception as e:
                print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to read config.json file: {str(e)}")

def create_config_manually(path):
    config_file = os.path.join(path, 'config.json')
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    if not os.path.exists(config_file):
        config_data = {
            'device_type': '',
            'supported_file_types': []
        }
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Created config.json file with empty entries.")
    else:
        with open(config_file, 'r+') as f:
            try:
                config_data = json.load(f)
                config_data['device_type'] = ''
                config_data['supported_file_types'] = []
                f.seek(0)
                f.truncate()
                json.dump(config_data, f, indent=4)
                print(f"[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Cleared existing entries in config.json file.")
            except Exception as e:
                print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to modify config.json file: {str(e)}")

def set_config_manually(path):
    config_path = os.path.join(path, 'config.json')
    try:
        with open(config_path, 'r+') as f:
            config_data = json.load(f)
            device_type = input("Enter the device type: ")
            config_data['device_type'] = device_type
            supported_file_types = input("Enter supported file types (space-separated): ").split()
            config_data['supported_file_types'] = supported_file_types
            f.seek(0)
            f.truncate()
            json.dump(config_data, f)
            print(f"[{Fore.LIGHTGREEN_EX}SYSTEM{Fore.RESET}] Updated config.json file with user input.")
            time.sleep(2)
    except Exception as e:
        print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] Failed to update config.json file: {str(e)}")
        time.sleep(2)

def format_json(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return
    
    # Check if the file is a JSON file
    if not file_path.endswith('.json'):
        print(f"[ERROR] Invalid file type. Expected JSON file: {file_path}")
        return
    
    try:
        # Open and load the JSON file
        with open(file_path) as f:
            json_data = json.load(f)
        
        # Format the JSON data
        formatted_json = json.dumps(json_data, indent=4)
        return formatted_json
    except Exception as e:
        print(f"[ERROR] Failed to format JSON file: {str(e)}")
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
    time.sleep(2)
    sys.exit()


# --------------- MAIN PROGRAM ---------------

def main():
    clear_console()
    print_ascii_art()
    menu_main()


if __name__ == "__main__":
    main()
