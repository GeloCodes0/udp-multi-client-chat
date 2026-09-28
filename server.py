import socket

# Server configuration
HOST = "127.0.0.1"
PORT = 12345

# Create a UDP socket.
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

# Bind the socket to the server address.
server_socket.bind((HOST, PORT))

# Store connected clients.
# Each client address is linked to a username.
clients = {}

print(f"UDP Chat Server listening on {HOST}:{PORT}")
print("Waiting for clients...")


def broadcast(message, exclude=None):
    """Send a message to all connected clients except one if specified."""

    for client_address in clients:

        if client_address != exclude:

            server_socket.sendto(
                message.encode(),
                client_address
            )


while True:

    # Receive a message from a client.
    data, client_address = server_socket.recvfrom(1024)

    message = data.decode().strip()

    # --------------------------------------------------
    # New client joining
    # --------------------------------------------------

    if client_address not in clients:

        username = message

        # Prevent empty usernames.
        if not username:

            server_socket.sendto(
                "ERROR: Username cannot be empty.".encode(),
                client_address
            )

            continue

        # Check whether the username is already being used.
        if username in clients.values():

            server_socket.sendto(
                "ERROR: Username already in use.".encode(),
                client_address
            )

            continue

        # Store the client address and username.
        clients[client_address] = username

        print(
            f"Client joined: {username} "
            f"{client_address}"
        )

        # Confirm the connection to the new client.
        server_socket.sendto(
            f"Welcome to the chat, {username}!".encode(),
            client_address
        )

        # Notify everyone else.
        broadcast(
            f"[Server]: {username} joined the chat.",
            exclude=client_address
        )

        continue

    # --------------------------------------------------
    # Existing client commands
    # --------------------------------------------------

    username = clients[client_address]

    # Client leaving the chat.
    if message.lower() == "/quit":

        print(
            f"Client left: {username} "
            f"{client_address}"
        )

        # Remove the client from the connected clients.
        del clients[client_address]

        # Notify the remaining clients.
        broadcast(
            f"[Server]: {username} left the chat."
        )

        continue

    # --------------------------------------------------
    # List connected users
    # --------------------------------------------------

    if message.lower() == "/users":

        if clients:

            usernames = ", ".join(
                clients.values()
            )

            response = (
                f"Online users: {usernames}"
            )

        else:

            response = "No users currently connected."

        server_socket.sendto(
            response.encode(),
            client_address
        )

        continue

    # --------------------------------------------------
    # Normal chat message
    # --------------------------------------------------

    formatted_message = (
        f"[{username}]: {message}"
    )

    print(formatted_message)

    # Send the message to every other client.
    broadcast(
        formatted_message,
        exclude=client_address
    )