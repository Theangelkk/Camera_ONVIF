import zmq
import simplejson as json
from subprocess import call
import os

context = zmq.Context()

addr = '127.0.0.1'  # remote ip or localhost
req_port = "20000"  # same as in the pupil remote gui
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:{}".format(addr, req_port))

# define clear function
def clear():
    # check and make call for specific operating system
    _ = call('clear' if os.name =='posix' else 'cls')

def show_main_menu():

    global socket

    Esito = False
    Richiesta = {'accuracy': None, 'avg_fps': None}

    while True:
        #clear()

        ## ------------------- Show Main menu ---------------------- ##
        print(30 * '-')
        print("   M A I N - M E N U")
        print(30 * '-')
        print("1. Set accuracy")
        print("2. Set avg_fps")

        if Esito:
            print("S. Invia Richiesta")

        print("Press Q for exit...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-3]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            #clear()
            frame_rate = float(input("Value accuracy: "))

            Richiesta['accuracy'] = frame_rate

            Esito = True
        elif choice == '2':
            #clear()
            avg_fps = float(input("Value avg_fps: "))

            Richiesta['avg_fps'] = avg_fps
            Esito = True
        elif choice == 's' or choice == 'S':

            socket.send_string(json.dumps(Richiesta))
            Esito = False
            Richiesta = {'accuracy': None, 'avg_fps': None}

            msg = socket.recv()

            json_answer = json.loads(msg, encoding='utf-8')

            print(json_answer)

            input('Premi un Tasto per andare avanti...')
        else:
            #clear()
            print("Invalid number. Try again...")

if __name__ == '__main__':

    show_main_menu()