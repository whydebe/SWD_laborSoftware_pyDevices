import requests
import os
import time

# Server URL
server_url = 'http://127.0.0.1:8000'

# Server status route
status_route = '/status'

# Server clear route
clear_route = '/clear'

# Prepare request route
prepare_route = '/prepare'

# Configuration request route
config_route = '/config'

# Start playback route
start_route = '/start'

# Stop playback route
stop_route = '/stop'

# Function to create the subfolder "data"
def create_data_folder():
    folder_name = 'data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f'Created "{folder_name}" folder')
    else:
        print(f'"{folder_name}" folder already exists')

# Function to download and save the test files
def download_files():
    urls = [
        'https://images.pexels.com/photos/1366957/pexels-photo-1366957.jpeg',
        'https://images.pexels.com/photos/2156881/pexels-photo-2156881.jpeg'
    ]

    folder_name = 'data'

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            file_path = os.path.join(folder_name, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f'Successfully downloaded and saved {filename}')
        else:
            print(f'Error downloading {url} (HTTP {response.status_code})')

# Check server status
response = requests.post(server_url + status_route)

if response.status_code == 200:
    print('Server is ready')
    print('Proceeding with further requests...\n')
else:
    print('Error: Server is not ready')
    exit()

# Clear all previous files
response = requests.post(server_url + clear_route)

if response.status_code == 200:
    print('All files cleared')
else:
    print('Error: Failed to clear files')
    exit()

# Set new configuration ("Device-Type") and supported file types
device_type = 'Monitor-Wall'
supported_file_types = ['.jpg', '.jpeg', '.png', '.mp4', '.mkv']

headers = {
    'Device-Type': device_type,
    'Supported-File-Types': ','.join(supported_file_types)
}

response = requests.post(server_url + config_route, headers=headers)

if response.status_code == 200:
    print(f'Configuration updated with Device-Type: {device_type}')
else:
    print('Error: Failed to update configuration')
    exit()

# Call of the function to create the subfolder "./data/"
create_data_folder()

# Call of the function to download and save the test files
download_files()

# Path to the directory with the files
filepath = './data/'

# List of files to upload (hardcoded)
files = [
    {
        'filename': 'pexels-photo-1366957.jpeg'
    },
    {
        'filename': 'pexels-photo-2156881.jpeg'
    }
]

# Iterate through the files and send them to the server
for file in files:
    filename = file['filename']

    # Read file content
    with open(filepath + filename, 'rb') as file:
        file_content = file.read()

    # Set HTTP headers
    headers = {
        'Filename': filename
    }

    # Send file to the server
    response = requests.post(server_url + prepare_route, headers=headers, data=file_content)

    # Print server response
    if response.status_code == 200:
        print(response.text)
    else:
        print(f'Error: Failed to transfer {filename} (HTTP {response.status_code})')
        exit()

# Start playback
response = requests.post(server_url + start_route)

if response.status_code == 200:
    print(response.text)
else:
    print('Error: Failed to start media playback')
    exit()

# Wait before stopping playback
time.sleep(20)

# Stop playback
response = requests.post(server_url + stop_route)

if response.status_code == 200:
    print(response.text)
else:
    print('Error: Failed to stop media playback')
    exit()
