# client.py - Sends periodic heartbeats to the server

import socket
import time
import random
import sys


def run_heartbeat_client(server_ip, client_id):
    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, 12345)

    print(f"Heartbeat client '{client_id}' starting. Sending pings to {server_address}")

    try:
        # Send heartbeats periodically
        while True:
            # Send heartbeat with client ID
            client_socket.sendto(client_id.encode('utf-8'), server_address)

            # Wait for acknowledgment (with timeout)
            client_socket.settimeout(2.0)
            try:
                data, _ = client_socket.recvfrom(1024)
                if data.decode('utf-8') == "ACK":
                    print(f"Server acknowledged heartbeat at {time.strftime('%H:%M:%S')}")
                else:
                    print(f"Unexpected response from server: {data.decode('utf-8')}")
            except socket.timeout:
                print("WARNING: No acknowledgment from server. It may be offline.")

            # Sleep for a random time between 3-7 seconds
            sleep_time = random.uniform(3, 7)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("Client shutting down")
    finally:
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py SERVER_IP CLIENT_ID")
        sys.exit(1)

    server_ip = sys.argv[1]
    client_id = sys.argv[2]
    run_heartbeat_client(server_ip, client_id)