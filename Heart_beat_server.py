# UDP Heartbeat Monitor
# server.py - Listens for heartbeats and logs client status

import socket
import datetime
import time


def run_heartbeat_server():
    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 12345))  # Listen on all interfaces, port 12345

    print("Heartbeat server running. Listening for client pings...")
    clients = {}  # Dictionary to track clients and their last heartbeat

    try:
        while True:
            # Receive data (non-blocking with timeout)
            server_socket.settimeout(1.0)
            try:
                data, addr = server_socket.recvfrom(1024)
                current_time = datetime.datetime.now()

                # Process the heartbeat
                client_id = data.decode('utf-8')
                clients[addr] = {
                    'client_id': client_id,
                    'last_seen': current_time
                }

                # Send acknowledgment
                server_socket.sendto(b"ACK", addr)
                print(f"Heartbeat from {client_id} at {addr} received at {current_time}")
            except socket.timeout:
                # No data received, check for stale clients
                pass

            # Check for clients that haven't sent a heartbeat recently
            current_time = datetime.datetime.now()
            stale_threshold = datetime.timedelta(seconds=10)

            for client_addr, client_info in list(clients.items()):
                time_since_last = current_time - client_info['last_seen']
                if time_since_last > stale_threshold:
                    print(
                        f"WARNING: Client {client_info['client_id']} at {client_addr} may be offline. Last seen {time_since_last.seconds} seconds ago")
                    # Could remove from active clients list or trigger alerts here

            time.sleep(1)  # Pause to reduce CPU usage

    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()


if __name__ == "__main__":
    run_heartbeat_server()