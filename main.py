import socket


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 80


def handling_get(request):
    # Parse HTTP headers
    headers = request.split('\n')
    filename = headers[0].split()[1]

    # Find file
    if filename == '/':
        filename = '/index.html'
    elif filename == '/home':
        filename = '/home.html'
    try:
        fin = open('.' + filename)
        content = fin.read()
        fin.close()

        # Response headers
        response_headers = "HTTP/1.1 200 OK\r\n"
        response_headers += "Content-Type: text/html\r\n"
        response_headers += "Content-Encoding: utf8\r\n"
        response_headers += "Connection: keep-alive\r\n"
        response_headers += "\r\n"

        response_content = content

        # Combine headers and content into a single response
        response = response_headers + response_content
        return response
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
        return response


def handling_post(request):
    # Parse HTTP headers
    headers = request.split('\n')
    filename = headers[0].split()[1]

    # Find file
    if filename == '/':
        json_res = {
            "message": "You are on homepage",
            "status": "OK"
        }

        try:
            # Response headers
            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type: text/html\r\n"
            response_headers += "Content-Encoding: utf8\r\n"
            response_headers += "Connection: keep-alive\r\n"
            response_headers += "\r\n"

            response_content = json_res

            # Combine headers and content into a single response
            response = response_headers + str(json_res)
            return response
        except FileNotFoundError:
            response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
            return response


def server_loop(server_socket):
    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        print("HTTP REQUEST", request)

        lines = request.split('\r\n')
        req_line = lines[0]
        req_method = req_line.split()[0]

        if req_method == 'GET':
            response = handling_get(request)
        else:
            response = handling_post(request)

        # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()

    # Close socket
    server_socket.close()


def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(2)

    print('Listening on port %s ...' % SERVER_PORT)

    return server_socket


def main():
    server_socket = create_server()
    server_loop(server_socket)


if __name__ == "__main__":
    main()
