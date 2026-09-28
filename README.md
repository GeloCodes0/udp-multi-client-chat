# UDP Multi-Client Chat

A multi-client chat application built with Python UDP sockets and threading.

The project demonstrates how multiple clients can communicate through a central UDP server. Clients register with a unique username, send messages to other connected users, view the list of active users, and disconnect from the chat using commands.

## Features

- UDP client-server communication
- Multiple simultaneous clients
- Unique username registration
- Username validation
- Join notifications
- Leave notifications
- Broadcast messaging
- `/users` command
- `/quit` command
- Background receiving thread
- Input validation
- Client connection tracking
- Server-side message formatting
- Concurrent message receiving and user input

## Technologies

- Python 3
- Python `socket` module
- Python `threading` module
- UDP
- IPv4
- Client-server architecture

## Project Structure

The project contains the following files:

- `client.py` - UDP chat client
- `server.py` - UDP chat server
- `README.md` - Project documentation
- `.gitignore` - Files excluded from version control

## Architecture

The application uses a central UDP server to manage communication between multiple clients.

The basic architecture is:

Client 1 (Angelo)
        |
        | UDP
        |
        v
UDP Chat Server
127.0.0.1:12345
        ^
        |
        | UDP
        |
Client 2 (John)

Each client communicates with the central UDP server.

The server tracks connected clients using their IP address and port number and associates each client address with a username.

When a client sends a normal chat message, the server broadcasts the message to all other connected clients.

## How It Works

### 1. Server Startup

The server creates a UDP socket using Python's `socket` module.

The socket uses:

- `AF_INET` for IPv4 communication
- `SOCK_DGRAM` for UDP communication

The server then binds the socket to:

- IP address: `127.0.0.1`
- Port: `12345`

The server continuously waits for incoming UDP datagrams using `recvfrom()`.

### 2. Client Connection

When a client starts, it creates a UDP socket and asks the user to provide a username.

The username is sent to the server.

The server validates the username before allowing the client to join.

The server checks that:

- The username is not empty.
- The username is not already in use.
- The username can be associated with the client's network address.

Once accepted, the client receives a welcome message.

Example:

    Enter your username: Angelo

The server records the client:

    Client joined: Angelo ('127.0.0.1', 63698)

The client then receives:

    Welcome to the chat, Angelo!

### 3. Username Registration

The server stores connected clients in a Python dictionary:

    clients = {}

The client's network address is used as the dictionary key and the username is stored as the value.

For example:

    ('127.0.0.1', 63698) -> Angelo
    ('127.0.0.1', 63604) -> John

This allows the server to determine which username belongs to each client.

The IP address and port combination uniquely identifies the UDP client during the current chat session.

### 4. Username Validation

The server prevents empty usernames from being registered.

If a client attempts to connect without providing a username, the server returns an error message.

The server also checks whether the username is already being used.

For example:

    ERROR: Username cannot be empty.

or:

    ERROR: Username already in use.

This prevents multiple clients from using the same username during the chat session.

### 5. Message Broadcasting

When a connected client sends a normal message, the server identifies the username associated with that client address.

The server then formats the message with the username.

For example:

    [Angelo]: Hello from angelo

The server broadcasts the formatted message to every other connected client.

The original sender is excluded from the broadcast because the sender already knows the message they sent.

This is handled by the server's `broadcast()` function.

### 6. Join Notifications

When a new client successfully joins the chat, the server notifies the existing users.

For example:

    [Server]: John joined the chat.

This allows existing clients to know when another user has connected.

### 7. Leave Notifications

When a client uses the `/quit` command, the server removes the client from the connected-client dictionary.

The remaining clients are then notified.

For example:

    [Server]: Angelo left the chat.

This keeps the active-user list accurate.

### 8. Viewing Connected Users

Clients can use the `/users` command to request a list of currently connected users.

Example:

    Message: /users

The server responds:

    Online users: Angelo, John

The response is generated using the usernames currently stored by the server.

### 9. Leaving the Chat

A client can leave the chat by entering:

    /quit

The server removes the client from its list of connected users.

The client then closes its UDP socket and exits.

Example:

    Message: /quit
    Disconnected from server.

## Client Threading

The client uses Python's `threading` module to handle incoming messages.

The client needs to perform two tasks at the same time:

1. Accept messages typed by the user.
2. Listen for messages arriving from the server.

A separate background thread continuously waits for incoming messages.

The main thread handles user input.

This allows the client to receive messages from other users without having to stop and wait for the user to type something.

The basic flow is:

    Main Thread
         |
         +----> User input
         |
         +----> Send message to server

    Receive Thread
         |
         +----> Wait for server messages
         |
         +----> Display received messages

Both threads use the same UDP socket.

The receiving thread is configured as a daemon thread so that it does not prevent the program from closing when the main client exits.

## Commands

### `/users`

Displays all currently connected usernames.

Example:

    Message: /users

    Online users: Angelo, John

### `/quit`

Disconnects the client from the chat.

Example:

    Message: /quit
    Disconnected from server.

## Running the Project

### Requirements

Python 3 must be installed.

No external Python packages are required.

The project only uses Python's standard library.

### Start the Server

Open a terminal in the project directory.

Run:

    python server.py

Expected output:

    UDP Chat Server listening on 127.0.0.1:12345
    Waiting for clients...

The server will then wait for UDP clients to connect.

### Start a Client

Open another terminal in the same project directory.

Run:

    python client.py

The client will ask for a username:

    UDP Chat Server: 127.0.0.1:12345
    Enter your username: Angelo

If the username is accepted:

    Welcome to the chat, Angelo!
    Type your messages below.
    Commands: /users or /quit

The client can now send messages to the server.

### Run Multiple Clients

To test multiple clients, open additional terminals and run:

    python client.py

For example:

    Client 1: Angelo
    Client 2: John

Both clients can then communicate through the same UDP server.

Additional clients can be started in the same way.

## Example Server Session

A typical server session may look like:

    UDP Chat Server listening on 127.0.0.1:12345
    Waiting for clients...

    Client joined: Angelo ('127.0.0.1', 63698)
    [Angelo]: Hello from angelo

    Client joined: John ('127.0.0.1', 63604)
    [John]: Hi from john in america

This demonstrates that the server can track multiple clients and associate received messages with the correct username.

## Example Client Session

A client session may look like:

    UDP Chat Server: 127.0.0.1:12345
    Enter your username: John
    Welcome to the chat, John!
    Type your messages below.
    Commands: /users or /quit

    Message: Hi from john in america
    Message: /users

    Online users: Angelo, John

    Message: /quit
    Disconnected from server.

## Testing

The application was tested using multiple clients running simultaneously against the same UDP server.

The following functionality was tested:

| Test | Result |
|---|---|
| Server startup | Passed |
| Client connection | Passed |
| Username registration | Passed |
| Empty username validation | Passed |
| Duplicate username validation | Passed |
| Multiple clients | Passed |
| Username identification | Passed |
| Message broadcasting | Passed |
| `/users` command | Passed |
| `/quit` command | Passed |
| Client disconnection | Passed |
| Join notifications | Passed |
| Leave notifications | Passed |
| Background message receiving | Passed |

The application was successfully tested with multiple clients communicating through the same UDP server.

Example multi-client server output:

    Client joined: Angelo ('127.0.0.1', 63698)
    [Angelo]: Hello from angelo
    Client joined: John ('127.0.0.1', 63604)
    [John]: Hi from john in america

## UDP vs TCP

This project uses UDP to demonstrate connectionless datagram communication.

### UDP

UDP does not establish a connection before sending data.

Instead, individual datagrams are sent between the client and server.

Advantages of UDP include:

- Low communication overhead
- No connection establishment
- Fast transmission for suitable applications
- Simple datagram-based communication
- Useful for applications where occasional packet loss may be acceptable

However, UDP does not guarantee:

- Delivery
- Ordering
- Duplicate protection
- Retransmission of lost packets

### TCP

TCP provides:

- Reliable delivery
- Ordered data
- Connection-oriented communication
- Retransmission of lost data
- Flow control

The TCP file-transfer project in this portfolio demonstrates TCP-based communication separately.

The comparison between the two projects demonstrates practical experience with both TCP and UDP socket programming.

## Networking Concepts Demonstrated

This project demonstrates practical understanding of:

- UDP sockets
- IPv4 addressing
- Port numbers
- Datagram communication
- Client-server architecture
- Socket creation
- Socket binding
- `sendto()`
- `recvfrom()`
- Multithreading
- Broadcast messaging
- Client tracking
- Username management
- Application-layer commands
- Input validation
- Client connection handling
- Client disconnection handling
- UDP and TCP differences

## Important UDP Concepts

Unlike TCP, UDP does not create a dedicated connection between the client and server.

The server receives each datagram together with the sender's network address.

The address contains:

- IP address
- Port number

For example:

    ('127.0.0.1', 63698)

This address allows the server to identify the client that sent the datagram and send a response back to the correct destination.

The server therefore maintains its own application-level list of active clients.

## Error Handling

The client and server include basic error handling for invalid input and socket shutdown.

The username system prevents:

- Empty usernames
- Duplicate usernames

The client also handles socket closure so that the receiving thread can exit when the client disconnects.

## Security Considerations

This project is primarily focused on networking and socket programming rather than production security.

The current implementation does not provide:

- Encryption
- User authentication
- Message integrity protection
- Secure identity verification

Messages are transmitted as normal UDP datagrams.

For a production messaging application, additional security controls would be required.

Possible security improvements include:

- Encrypted communication
- User authentication
- Message integrity protection
- Secure session management
- Input sanitisation
- Rate limiting
- Access control

## Limitations

This project is designed as a networking and socket-programming demonstration rather than a production chat application.

Current limitations include:

- UDP does not guarantee message delivery.
- UDP does not guarantee message ordering.
- Messages are not encrypted.
- There is no authentication beyond username registration.
- The server currently runs as a single process.
- The server is configured for local testing using `127.0.0.1`.
- There is no persistent message history.
- The application does not implement reliable message retransmission.
- The terminal interface is intentionally simple.
- There is no database for storing users or messages.

These limitations allow the project to focus on UDP networking, multi-client communication, socket programming, and threading.

## Future Improvements

Potential future improvements include:

- Reliable message delivery
- Message timestamps
- Private messaging
- User authentication
- Encrypted communication
- Persistent chat history
- Database integration
- Server administration commands
- Improved terminal interface
- Logging
- Rate limiting
- Running the server on a remote host
- Better handling of UDP packet loss
- Client reconnection handling
- Message sequence numbers
- Delivery acknowledgements

## Learning Objectives

This project was developed to demonstrate practical understanding of UDP networking and concurrent client communication.

Key learning outcomes include:

- Creating and managing UDP sockets in Python
- Understanding connectionless communication
- Managing multiple clients from a central server
- Tracking clients using IP addresses and ports
- Associating usernames with network addresses
- Broadcasting messages between clients
- Using threads for simultaneous input and message reception
- Designing simple application-layer commands
- Handling client connection and disconnection events
- Understanding the differences between UDP and TCP
- Understanding the limitations of connectionless communication
- Applying basic client and server error handling

## Conclusion

This project demonstrates a practical multi-client UDP chat system using Python's standard networking libraries.

The project combines UDP socket programming, client tracking, username management, message broadcasting, application-layer commands, and multithreading.

It forms part of a broader Python networking portfolio demonstrating practical experience with network communication, client-server architectures, TCP, UDP, APIs, automation, and security-focused programming.