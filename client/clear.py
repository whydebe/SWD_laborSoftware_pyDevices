import requests

server_url = 'http://localhost:8000'
clear_route = '/clear'
response = requests.post(server_url + clear_route)