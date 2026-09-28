import socket
import threading


# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345


def receive_messages(client_socket):
    """Continuously receive messages from the server."""

    while True:

        try:

            message, _ = client_socket.recvfrom(1024)

            print(
                f"\n{message.decode()}"
            )

            print(
                "Message: ",
                end="",
                flush=True
            )

        except OSError:

            break


def start_client():

    # Create a UDP socket.
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    print(
        f"UDP Chat Server: "
        f"{SERVER_IP}:{SERVER_PORT}"
    )

    # Ask the user for a username.
    while True:

        username = input(
            "Enter your username: "
        ).strip()

        if not username:

            print(
                "Username cannot be empty."
            )

            continue

        # Send the username to the server.
        client_socket.sendto(
            username.encode(),
            (SERVER_IP, SERVER_PORT)
        )

        # Wait for the server's response.
        response, _ = client_socket.recvfrom(1024)

        response = response.decode()

        # Check whether the username was accepted.
        if response.startswith("Welcome"):

            print(response)

            break

        print(response)

    # Start the background thread that listens
    # for incoming chat messages.
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )

    receive_thread.start()

    print(
        "Type your messages below."
    )

    print(
        "Commands: /users or /quit"
    )

    while True:

        # Get a message from the user.
        message = input(
            "Message: "
        )

        # Send the message to the server.
        client_socket.sendto(
            message.encode(),
            (SERVER_IP, SERVER_PORT)
        )

        # Leave the chat.
        if message.lower() == "/quit":

            break

    # Close the socket.
    client_socket.close()

    print(
        "Disconnected from server."
    )


if __name__ == "__main__":
    start_client()