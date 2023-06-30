import http.server
import socketserver
import socket
import json
import os
# import re
import hashlib
import time
import subprocess

class PostRequestHandler(http.server.BaseHTTPRequestHandler):
    # Directory to store uploaded files
    filepath = './data/'
    # Directory to store server configuration
    configpath = './config/'
    # Name of the server configuration file
    configfile = 'config.json'
    # Command to start media playback using VLC player
    player_command = 'start vlc {path} --fullscreen --loop --quiet --no-video-title'
    # Check if files got cleared before preparing
    is_cleared = False

    def do_POST(self):
        # Handle POST requests based on the requested path
        if self.path == '/status':
            # Return server status
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Server is ready'.encode())
        elif self.path == '/prepare':
            # Receive files from the client and prepare the server with them
            self.prepare_request()
        elif self.path == '/start':
            # Start media playback
            self.start_media()
        elif self.path == '/stop':
            # Stop media playback
            self.stop_all()
        elif self.path == '/clear':
            # Clear all files on the server
            self.clear_files()
        elif self.path == '/config':
            # Update server configuration
            self.update_config()
        else:
            # Invalid route
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Invalid route'.encode())

    def prepare_request(self):
        # Clear files before preparing
        if PostRequestHandler.is_cleared == False:
            self.clear_files()
            PostRequestHandler.is_cleared == True
        
        # Check if the data folder exists, create it if it doesn't
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

        # Prepare file upload request
        filename = self.headers.get('Filename')
        if not filename:
            filename = 'uploaded_file.unknown'

        content_length = int(self.headers.get('Content-Length'))
        file_content = self.rfile.read(content_length)

        file_path = self.filepath + filename
        with open(file_path, 'wb') as file:
            file.write(file_content)

        file_hash = self.generate_file_hash(file_path)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(f'Transfer of {filename} was successful'.encode())

        file_info = {
            'timecode': self.get_timecode(),
            'filename': filename,
            'path': file_path,
            'hash': file_hash
        }
        self.write_to_json(file_info)

    def generate_file_hash(self, file_path):
        # Generate SHA-256 hash for a file
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def get_timecode(self):
        # Get current time in a specific format
        return time.strftime('%Y%m%d-%H%M%S')

    def write_to_json(self, file_info):
        # Write file information to a JSON file
        file_list = []
        if os.path.exists('files.json'):
            with open('files.json', 'r') as json_file:
                file_list = json.load(json_file)

        file_list.insert(0, file_info)

        with open('files.json', 'w') as json_file:
            json.dump(file_list, json_file, indent=4)
            
    def reset_is_cleared(self):
        # Re-Activate clear at prepare statup
        if PostRequestHandler.is_cleared == True:
            PostRequestHandler.is_cleared = False

    def clear_files(self):
        # Check if the data folder exists, create it if it doesn't
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        
        # Clear all files on the server
        if os.listdir(self.filepath):
            for file_name in os.listdir(self.filepath):
                file_path = os.path.join(self.filepath, file_name)
                os.remove(file_path)

        if os.path.exists('files.json') and os.path.getsize('files.json') > 0:
            with open('files.json', 'w') as json_file:
                json_file.write('[]')

        self.send_response(200)
        self.end_headers()
        self.wfile.write('All files cleared'.encode())

    def update_config(self):
        # Re-Activate clear at prepare statup
        self.reset_is_cleared()
        
        # Update server configuration
        device_type = self.headers.get('Device-Type')
        supported_file_types = self.headers.get('Supported-File-Types')

        if device_type and supported_file_types:
            if not os.path.exists(self.configpath):
                os.makedirs(self.configpath)

            config_file_path = os.path.join(self.configpath, self.configfile)
            if not os.path.exists(config_file_path) or os.path.getsize(config_file_path) == 0:
                with open(config_file_path, 'w') as json_file:
                    json_file.write('{}')

            config_data = {
                'device_type': device_type,
                'supported_file_types': supported_file_types.split(',')
            }

            with open(config_file_path, 'w') as json_file:
                json.dump(config_data, json_file, indent=4)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'Config updated with device type: {device_type}'.encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Device type or supported file types not provided'.encode())

    def start_media(self):
        # Re-Activate clear at prepare statup
        self.reset_is_cleared()
        
        # Start media playback using VLC player
        config_file_path = os.path.join(self.configpath, self.configfile)
        files_json_path = 'files.json'

        if os.path.exists(config_file_path) and os.path.exists(files_json_path):
            with open(config_file_path, 'r') as json_file:
                config_data = json.load(json_file)

            with open(files_json_path, 'r') as json_file:
                files_data = json.load(json_file)

            supported_file_types = config_data.get('supported_file_types', [])
            file_paths = [file['path'] for file in files_data if file['filename'].endswith(tuple(supported_file_types))]

            if len(file_paths) > 0:
                command = self.player_command.format(path=' '.join(file_paths))
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write('Media playback started successfully'.encode())
                else:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f'Failed to start media playback: {result.stderr}'.encode())
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write('No files with supported file types found'.encode())
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write('Configuration file or files JSON file not found'.encode())

    def stop_all(self):
        # Re-Activate clear at prepare statup
        self.reset_is_cleared()
        
        # Stop media playback by killing the VLC process
        command = 'taskkill /im vlc.exe /f'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            self.send_response(200)
            self.end_headers()
            self.wfile.write('Media playback stopped successfully'.encode())
        else:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Failed to stop media playback: {result.stderr}'.encode())



# Server configuration
config_file_path = './config/config.json'
default_host = '127.0.0.1'
host = ''
port = 8000

# Check if the config file exists and has the "ipv4_address" entry
# if os.path.exists(config_file_path):
#     with open(config_file_path, 'r') as json_file:
#         config_data = json.load(json_file)
#         ipv4_address = config_data.get('ipv4_address')
# 
#         if ipv4_address and isinstance(ipv4_address, str) and len(ipv4_address) > 0:
#             # Check if the "ipv4_address" has a valid IPv4 format
#             import re
#             ipv4_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
#             if re.match(ipv4_pattern, ipv4_address):s
#                 host = ipv4_address
#             else:
#                 host = '127.0.0.1'
#         else:
#             host = '127.0.0.1'
# else:
#     host = '127.0.0.1'

# Get the IPv4 address
try:
    hostname = socket.getfqdn()
    ip_address = socket.gethostbyname_ex(hostname)[2][1]
    host = f'{ip_address}'
except Exception as e:
    print(f"Failed to retrieve IPv4 address: {str(e)}")
    host = f'{default_host}'

# Create the server
server = socketserver.TCPServer((host, port), PostRequestHandler)

# Check and update the JSON file
if not os.path.exists('files.json') or os.path.getsize('files.json') == 0:
    with open('files.json', 'w') as json_file:
        json_file.write('[]')

# Start the server
print(f'Server running on http://{host}:{port}')
server.serve_forever()