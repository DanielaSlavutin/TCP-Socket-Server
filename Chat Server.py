import socket
import threading

class ServerManager:
    def set_up_server(self):
        """
        This method setd up the server:
            - Inititalizes the socket.
            - Binds it to a specific host and post
            - Listens for incoming connections.
            - Handles multiple incoming connections.
        """

        host = '127.0.0.1' # Local host address
        port = 9559 # Port for the server to listen on
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creation of a TCP socket
        self.server_socket.bind((host, port)) # Bind the socket to the host and port
        self.clients=[] # List to store connected client sockets
        self.server_socket.listen(5) # Starts listening for incoming connections (maximum 5 in queue)
        print(f"Listening on {host}:{port}")

        while True:
            # Accept an incoming connection
            client_socket, address=self.server_socket.accept()
            print(f"Connection from {address}")

            # Receive the username from the client (expected as the first message)
            username=client_socket.recv(1024) # Receive username maximum 1024 bytes
            print(f'Connected username: {username.decode()}')

            # Add the new client to the list of connected clients
            self.clients.append(client_socket)

            # Create a new thread to handle communication with this client
            client_thread=threading.Thread(target=self.handle_client, args=(client_socket, username.decode()))
            client_thread.start() # Start the thread


    def handle_client(self, client_socket, username):
        """
        This method handles communication with a single client:
            - Receives messages from the client.
            - Broadcasts the messages to all other connected clients.
            - Handles disconnection of the client gracefully.
        """

        try:
            while True:
                # Wait for a message from the client
                data=client_socket.recv(1024)
                if not data: # If no data is received, the client has disconnected
                    break
                print(f"{username}: {data.decode()}") # Print the message on the server console
                for sock in self.clients:
                    if sock == client_socket: # skip the sender
                        continue
                    # Send the message to the other clients
                    sock.send(f'\n{username}:\n  '.encode('utf-8')+data)
        except ConnectionResetError:
            # Handle cases where the client disconnects abruptly
            pass
        finally:
            # Cleanup after the client disconnects
            client_socket.close() # Close the socket
            print(f'{username} disconnected') # notify server of disconnection
            self.clients.remove(client_socket) # Remove the client from the list


if __name__ == "__main__":
    # Entry point of the script
    server_manager=ServerManager() # Create an instance of ServerManager
    server_manager.set_up_server()  # Start the server