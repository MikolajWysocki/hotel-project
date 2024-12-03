import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == 'C:/Users/mikol/Desktop/hotel-project/frontend/data': # tutaj to /data zmienić na nazwę pliku ("data" to placeholder)
            # Ustawienia nagłówków odpowiedzi
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Dane, które zwraca backend
            response = {'message': 'Hello from Python backend!', 'data': [1, 2, 3]}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, 'Endpoint not found')

    def do_POST(self):
        if self.path == 'C:/Users/mikol/Desktop/hotel-project/frontend/data': # tutaj to /data zmienić na nazwę pliku ("data" to placeholder)
            # Pobieranie długości danych z nagłówków
            content_length = int(self.headers['Content-Length'])
            # Wczytywanie i dekodowanie JSON-a
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Obsługa danych z frontendu
            print("Received data:", data)

            # Odpowiedź do klienta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success', 'received': data}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, 'Endpoint not found')


# Uruchamianie serwera HTTP
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=7000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
