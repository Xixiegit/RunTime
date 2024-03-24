import socket
import json
import threading
import time

test = True
finding = True
rec = True
host = "192.168.1.106"
port = 21043
clients = {}

    
    
    



def connections():
    while True:
        print("connections started")
        s = socket.socket()
        s.bind((host, port))
        s.listen(2)
        c, address = s.accept()
        print(f"Connected to: {address}")
        clients =  {address}
        
        
        for clients in clients:
            find(c)


def find(c):
    global finding  # Declare 'finding' as global
    while finding:
        print("find start")
        data = c.recv(1024)
        if not data:  # Check if data is empty
            print("No data received")
            return  # Exit the function if no data is received
        print(data)

        # Respond to the client with a config
        configed = '200'
        c.send(configed.encode('utf-8'))

        confirmation(c)


def confirmation(c):
    global finding  # Declare 'finding' as global
    finding = False  # Stop the 'find' loop
    print("confirmation start ")
    data2 = c.recv(1024)
    if not data2:  # Check if data is empty
        print("No data received")
        return  # Exit the function if no data is received
    print(data2)
    data2_dec = data2.decode().strip()  # Strip any leading or trailing whitespaces
    if data2_dec == '400':
        time.sleep(1)
        print("400 received: No connection and No Tracking")
    elif data2_dec == '300':
        time.sleep(1)
        print("300 received: No connection and No Tracking until further notice")
    elif data2_dec == '200':
        time.sleep(1)
        print("200 received: Tracking and sending")
        server()
    elif data2_dec == '350':
        time.sleep(1)
        print("350 received: Tracking started ")
    else:
        print("Invalid value received")




def server():
    while True:
        HOST = "192.168.1.106"  # Standard loopback interface address (localhost)
        PORT = 21041  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                # Create a byte string to store received data
                received_data = b""
                try:
                    while True:
                        data = conn.recv(4096)  # Increase buffer size to receive larger chunks of data
                        if not data:
                            break
                        received_data += data  # Append received data
                    # Save received data to a JSON file
                    with open("User_data.json", "wb") as file:
                        file.write(received_data)
                except Exception as e:
                    print(f"Error occurred: {e}")




def save_messages_to_json(messages):
    # Write received messages to a JSON file
    file_name = "User_data.json"
    with open(file_name, "w") as file:
        json.dump(messages, file, indent=4)



threading.Thread(target=connections).start()