from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

hostName = 'localhost'
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        # Сохраняем только путь без параметров
        path = urlparse(self.path).path
        if path == '/':
            path = '/index.html'
        file_to_open = path[1:]
        try:
            with open(file_to_open, "r") as f:
                page_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(page_content, "utf-8"))
        except Exception as e:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/button-click':
            content_length = int(self.headers['Content-Length'])  # Получение размера данных
            post_data = self.rfile.read(content_length)  # Чтение данных
            print(post_data.decode('utf-8'))  # Вывод в консоль

            # Отправка подтверждения обратно в браузер
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'success',
                'message': 'Button was clicked!'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # Любой другой POST-запрос приводит к ошибке 404
            self.send_error(404, "File Not Found")


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")