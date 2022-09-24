# Import socket module
import socket
# import os module
import os

PORT = 2728
HOST = '127.0.0.1'

# create an INET(IPV4), Streaming (TCP) socket.
server_socket = socket.socket(socket.AddressFamily.AF_INET,socket.SocketKind.SOCK_STREAM)
# Bind socket with localhost, and port 2728.
server_socket.bind((HOST,PORT))
server_socket.listen()

# Function to get correct resource path.
def correct_resource_path(path: str):
    if path.endswith('/'):
        path = path[0:-1]
    path_segments = path.split('.')

    if not (path == ''):
        if len(path_segments) > 1:
            file_path = os.path.join(
                os.getcwd(),"htdocs",path[1:]
            )
        else:
            file_path = os.path.join(
                os.getcwd(),"htdocs",f"{path[1:]}.html"
            )
    else:
        file_path = os.path.join(os.getcwd(),"htdocs","index.html")

    return file_path


while True:
    # Accept connections from outside.
    client_socket,client_address = server_socket.accept()
    
    with client_socket:
        print(f"Connected by {client_address}")
        # Take the client message with the size 1024 bytes.
        client_raw_message = client_socket.recv(1024)
        # Convert into normal string.
        client_message = client_raw_message.decode()

        http_headers = client_message.split("\r\n")
        # get the path header.
        http_path_header = http_headers[0]

        try: 
            # get url path
            http_url_path = http_path_header.split(" ")[1]

            # Function call to get correct resource path according to the operating system and the directory path.
            resource_path = correct_resource_path(http_url_path)

            try:
                # Get resources from htdocs folder
                resource = open(resource_path,'r')
                # Read content
                file_content = resource.read();
                resource.close()

                http_response = f"HTTP/1.1 200 OK\r\n\n{file_content}";
                # Send http response
                client_socket.sendall(http_response.encode())
            except FileNotFoundError:
                # 404 not found message if requested file doesn't exist.
                client_socket.sendall("HTTP/1.1 404 Not Found".encode())
        except IndexError:
            # 400 bad request message if the server cannot process the request.
            client_socket.sendall("HTTP/1.1 400 Bad Request".encode())

        client_socket.close()
