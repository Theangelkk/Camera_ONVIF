from Camera_onvif import Camera
from Streaming_Video import Streaming_Video
from subprocess import call
import os
import Zeep_Framework
import zeep

cam = None
streaming = None

# define clear function
def clear():
    # check and make call for specific operating system
    _ = call('clear' if os.name =='posix' else 'cls')

def show_main_menu():

    clear()

    while True:
        ## ------------------- Show Main menu ---------------------- ##
        print(30 * '-')
        print("   M A I N - M E N U")
        print(30 * '-')
        print("1. Options Camera ONVIF")
        print("2. Streaming Camera")
        print("3. PTZ Setting")
        print("Press Q for exit...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-2]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            clear()
            show_menu_onvif()
        elif choice == '2':
            clear()
            show_menu_streaming()
        elif choice == '3':
            clear()
            show_ptz_setting()
        else:
            clear()
            print("Invalid number. Try again...")

# --------------------- Manu Onvif ------------------------------------
def show_menu_onvif():

    while True:
        ## ------------------- Show Onvif menu ---------------------- ##
        print(30 * '-')
        print("   O N V I F - M E N U")
        print(30 * '-')
        print("1. Camera Setting")
        print("2. Image Setting")
        print("Press Q for return in Main Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-2]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            clear()
            show_camera_setting()
        elif choice == '2':
            clear()
            show_image_setting()
        else:
            clear()
            print("Invalid number. Try again...")

    show_main_menu()

def show_ptz_setting():

    global cam

    while True:
        ## ------------------- Show Camera Setting ---------------------- ##
        print(30 * '-')
        print("  P T Z  S E T T I N G - M E N U")
        print(30 * '-')
        print("1. Print PTZ Service")
        print("2. ...")
        print("Press Q for return in Main Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-2]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            clear()
            cam.print_config_ptz()
            break
        elif choice == '2':
            clear()
            break
        else:
            clear()
            print("Invalid number. Try again...")

def show_camera_setting():

    global cam

    while True:
        ## ------------------- Show Camera Setting ---------------------- ##
        print(30 * '-')
        print("  C A M E R A  S E T T I N G - M E N U")
        print(30 * '-')
        print("1. Set Resolution")
        print("2. ...")
        print("3. Print Setting Camera")
        print("Press Q for return in Onvif Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-2]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            print("Resolution Available: ")
            print(cam.get_ResolutionAvailable())
            cam.set_Resolution(cam, 2)
            clear()
            break
        elif choice == '2':
            clear()
            break
        elif choice == '3':
            clear()
            cam.print_config_media()
            break
        else:
            clear()
            print("Invalid number. Try again...")

    show_menu_onvif()

def show_image_setting():
    global cam

    while True:
        ## ------------------- Show Image Setting ---------------------- ##
        print(30 * '-')
        print("  I M A G E  S E T T I N G - M E N U")
        print(30 * '-')
        print("1. Set Constrast")
        print("2. Set Brightness")
        print("3. Set Iris")
        print("4. Set AutoFocus")
        print("5. Print Image Setting")
        print("Press Q for return in Onvif Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-2]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            Esito = True
            value_contrast = 0
            while Esito:
                value_contrast = int(input("Value Contrast: "))

                if value_contrast < 0 or value_contrast > 100:
                    print("Please insert the value of contrast between 0 and 100")
                else:
                    Esito = False

            cam.set_Contrast(value_contrast)

            clear()
            break

        elif choice == '2':
            clear()
            Esito = True
            value_brightness = 0
            while Esito:
                value_brightness = int(input("Value Brightness: "))

                if value_brightness < 0 or value_brightness > 100:
                    print("Please insert the value of brightness between 0 and 100")
                else:
                    Esito = False

            cam.set_Brightness(value_brightness)
            break
        elif choice == '3':
            clear()
            Esito = True
            value_iris = 0.0
            while Esito:
                value_iris = float(input("Iris: "))

                if value_iris < 0.0 or value_iris > 1.0:
                    print("Please insert the value of gain between 0.0 and 1.0")
                else:
                    Esito = False

            cam.set_Iris(value_iris)
            break
        elif choice == '4':
            clear()
            cam.set_AutoFocus()
        elif choice == '5':
            clear()
            cam.print_config_image()
            break
        else:
            clear()
            print("Invalid number. Try again...")

    show_menu_onvif()

# --------------------- Manu Streaming ------------------------------------
def show_menu_streaming():

    global streaming

    while True:
        ## ------------------- Show Streaming menu ---------------------- ##
        print(30 * '-')
        print("   S T R E A M I N G - M E N U")
        print(30 * '-')
        print("1. View Video Live")
        print("2. Save Video Live")
        print("3. Set Frame Rate")
        print("4. View Buffer Frame")
        print("Press Q for return in Main Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-3]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            streaming.live_streaming()
            clear()
            break
        elif choice == '2':
            clear()
            streaming.save_Video()

            break
        elif choice == 3:
            Esito = True
            frame_rate = 0
            while Esito:
                frame_rate = int(input("Frame Rate: "))

                if frame_rate < 0 or frame_rate > 25:
                    print("Please insert the value of frame rate between 0 and 25")
                else:
                    Esito = False

            streaming.set_FrameRate(frame_rate)

            clear()
            break
        elif choice == 4:
            streaming.view_FrameBuffer()

            clear()
            break
        else:
            clear()
            print("Invalid number. Try again...")

    show_main_menu()

def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue

if __name__ == '__main__':

    zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue


    Camera.set_parameters('192.168.1.108', 80, 'project', 'ONVIFADMIN2020')
    cam = Camera.get_camera()

    # print(cv2.getBuildInformation())

    Streaming_Video.set_parameters('192.168.1.108', 'admin', 'ADMIN2020')
    streaming = Streaming_Video.get_Streaming_Video()

    show_main_menu()

    #Zeep_Framework.prova_zeep()

