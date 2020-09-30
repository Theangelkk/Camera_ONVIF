from Camera_onvif import Camera
from Streaming_Video import Streaming_Video
from subprocess import call
import os
import cv2
import Zeep_Framework
import zeep

cam = None
streaming = None

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

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
        choice = input('Enter your choice [1-3]: ')

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

    clear()

    while True:
        ## ------------------- Show Onvif menu ---------------------- ##
        print(30 * '-')
        print("   O N V I F - M E N U")
        print(30 * '-')
        print("1. Camera Setting")
        print("2. Image Setting")
        print("3. Device Managment Setting")
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
        elif choice == '3':
            clear()
            show_devicemgmt_setting()
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
        print("1. Get Resolution")
        print("2. Get Quality Range")
        print("3. Get GovLengthRange")
        print("4. Get Frame Rate")
        print("5. Set Resolution")
        print("6. Set Quality Range")
        print("7. Set GovLengthRange")
        print("8. Set Frame Rate")
        print("9. Print Setting Camera")
        print("10. Print Options Setting Camera")
        print("11. Print Setting Metadata")
        print("12. Print Options Setting Metadata")
        print("13. Print Setting VideoSources")
        print("14. Print Options Setting VideoSources")
        print("15. Print Option Media Capabilities")
        print("16. Print Setting VideoSources Mode")
        print("17. Print All Profiles")
        print("18. Print Main Profile")
        print("Press Q for return in Onvif Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-18]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            clear()
            print("Actual Resolution: " + str(cam.get_Resolution()))
            input("Press a key to continue...")
            clear()
            break
        if choice == '2':
            clear()
            print("Actual Quality Range: " + str(cam.get_QualityRange()))
            input("Press a key to continue...")
            clear()
            break
        if choice == '3':
            clear()
            print("Actual GovLengthRange: " + str(cam.get_GovLengthRange()))
            input("Press a key to continue...")
            clear()
            break
        if choice == '4':
            clear()
            print("Actual Frame Rate: " + str(cam.get_FrameRate()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '5':
            print("Resolution Available: ")
            print(cam.get_ResolutionAvailable())
            number_of_res = len(cam.get_ResolutionAvailable())

            Esito = True
            value_resolution = 0
            while Esito:
                value_resolution = int(input("Value Resolution: "))

                if value_resolution < 0 or value_resolution >= number_of_res:
                    print("Please insert the value of resolution between 0 and " + str(number_of_res-1))
                else:
                    Esito = False

            cam.set_Resolution(value_resolution)
            clear()
            break
        elif choice == '6':
            clear()
            min,max = cam.get_Options_QualityRange()
            print("Quality Range Available: [" + str(min) + "," + str(max) + "]")

            Esito = True
            value_quality_range = 0
            while Esito:
                value_quality_range = int(input("Value Quality Range: "))

                if value_quality_range < min or value_quality_range > max:
                    print("Please insert the value of resolution between " + min + " and " + str(max))
                else:
                    Esito = False

            cam.set_QualityRange(value_quality_range)
            clear()
            break
        elif choice == '7':
            clear()
            min,max = cam.get_Options_GovLengthRange()
            print("GovLengthRange Available: [" + str(min) + "," + str(max) + "]")

            Esito = True
            value_GovLengthRange = 0
            while Esito:
                value_GovLengthRange = int(input("Value GovLengthRange: "))

                if value_GovLengthRange < min or value_GovLengthRange > max:
                    print("Please insert the value of GovLengthRange between " + min + " and " + str(max))
                else:
                    Esito = False

            cam.set_GovLengthRange(value_GovLengthRange)
            clear()
            break
        elif choice == '8':
            clear()
            min,max = cam.get_Options_FrameRate()
            print("Frame Rate Available: [" + str(min) + "," + str(max) + "]")

            Esito = True
            value_FrameRate = 0
            while Esito:
                value_FrameRate = int(input("Value Frame Rate: "))

                if value_FrameRate < min or value_FrameRate > max:
                    print("Please insert the value of Frame Rate between " + min + " and " + str(max))
                else:
                    Esito = False

            cam.set_GovLengthRange(value_FrameRate)
            clear()
            break
        elif choice == '9':
            clear()
            cam.print_config_media()
            input("Press a key to continue...")
            break
        elif choice == '10':
            clear()
            cam.print_options_config_media()
            input("Press a key to continue...")
            break
        elif choice == '11':
            clear()
            cam.print_config_metadata()
            input("Press a key to continue...")
            break
        elif choice == '12':
            clear()
            cam.print_options_config_metadata()
            input("Press a key to continue...")
            break
        elif choice == '13':
            clear()
            cam.print_config_videosources()
            input("Press a key to continue...")
            break
        elif choice == '14':
            clear()
            cam.print_options_config_videosources()
            input("Press a key to continue...")
            break
        elif choice == '15':
            clear()
            cam.print_option_media_capabilities__()
            input("Press a key to continue...")
            break
        elif choice == '16':
            clear()
            cam.print_config_videosources_modes()
            input("Press a key to continue...")
            break
        elif choice == '17':
            clear()
            cam.print_all_profiles()
            input("Press a key to continue...")
            break
        elif choice == '18':
            clear()
            cam.print_main_profile()
            input("Press a key to continue...")
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
        print("1. Get Contrast")
        print("2. Get Brightness")
        print("3. Get Sharpness")
        print("4. Get Saturation")
        print("5. Get Iris")
        print("6. Get Position Focus")
        print("7. Set Contrast")
        print("8. Set Brightness")
        print("9. Set Sharpness")
        print("10. Set Saturation")
        print("11. Set Iris")
        print("12. Set Position Focus")
        print("13. Print Image Setting")
        print("14. Print Options Image Setting")
        print("15. Print Status Move")
        print("16. Print Options Move")
        print("17. Print Options Capabilities")
        print("Press Q for return in Onvif Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-17]: ')

        if choice == 'q' or choice == 'Q':
            break

        ### Take action as per selected menu-option ###
        if choice == '1':
            clear()
            print("Actual Contrast: " + str(cam.get_Contrast()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '2':
            clear()
            print("Actual Brightness: " + str(cam.get_Brightness()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '3':
            clear()
            print("Actual Sharpness: " + str(cam.get_Sharpness()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '4':
            clear()
            print("Actual Saturation: " + str(cam.get_Saturation()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '5':
            clear()
            print("Actual Iris: " + str(cam.get_Iris()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '6':
            clear()
            print("Actual Position Focus: " + str(cam.get_Focus_Position()))
            input("Press a key to continue...")
            clear()
            break
        elif choice == '7':
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
        elif choice == '8':
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
        elif choice == '9':
            clear()
            Esito = True
            value_sharpness = 0
            while Esito:
                value_sharpness = int(input("Value Sharpness: "))

                if value_sharpness < 0 or value_sharpness > 100:
                    print("Please insert the value of sharpness between 0 and 100")
                else:
                    Esito = False

            cam.set_Sharpness(value_sharpness)
            break
        elif choice == '10':
            clear()
            Esito = True
            value_saturation = 0
            while Esito:
                value_saturation = int(input("Value Saturation: "))

                if value_saturation < 0 or value_saturation > 100:
                    print("Please insert the value of value_saturation between 0 and 100")
                else:
                    Esito = False

            cam.set_Saturation(value_saturation)
            break
        elif choice == '11':
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
        elif choice == '12':
            clear()
            Esito = True
            value_position_focus = 0.0
            while Esito:
                value_position_focus = float(input("Focus Position: "))

                if value_position_focus < 0.0 or value_position_focus > 1.0:
                    print("Please insert the value of position focus between 0.0 and 1.0")
                else:
                    Esito = False

            cam.set_Focus_Move(value_position_focus)
            input("Press a key to continue...")
            break
        elif choice == '13':
            clear()
            cam.print_config_image()
            input("Press a key to continue...")
            break
        elif choice == '14':
            clear()
            cam.print_options_image__()
            input("Press a key to continue...")
            break
        elif choice == '15':
            clear()
            cam.print_config_move()
            input("Press a key to continue...")
            break
        elif choice == '16':
            clear()
            cam.print_options_move__()
            input("Press a key to continue...")
            break
        elif choice == '17':
            clear()
            cam.print_option_media_capabilities__()
            input("Press a key to continue...")
            break
        else:
            clear()
            print("Invalid number. Try again...")

    show_menu_onvif()

def show_devicemgmt_setting():

    global cam

    while True:
        ## ------------------- Show Device Managment Setting ---------------------- ##
        print(30 * '-')
        print("  D E V I C E  M G M T  S E T T I N G - M E N U")
        print(30 * '-')
        print("1. Print Hostname")
        print("2. Print All Information Device")
        print("3. Print Time and Date Device")
        print("4. Set Hostname")
        print("5. Update Time and Date Device")
        print("R. Reboot Device")
        print("R. Soft Factory Reset Device")
        print("Z. Soft Factory Reset Device")
        print("X. Hard Factory Reset Device")
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
            print("Hostname: " + str(cam.get_Hostname()))
            input("Press a key to continue...")
            break
        elif choice == '2':
            clear()
            print("All Information Device " + str(cam.get_Hostname()))
            print(str(cam.get_all_information_device()))
            input("Press a key to continue...")
            break
        elif choice == '3':
            clear()
            print("System URIs Device " + str(cam.get_Hostname()))
            print(str(cam.get_system_Date_Time()))
            input("Press a key to continue...")
            break
        elif choice == '4':
            clear()
            Esito = True
            name_hostname = ""
            while Esito:
                name_hostname = input("Insert new Hostname: ")

                if len(name_hostname) < 2:
                    print("Hostname too short, minimum 2 or more characters")
                else:
                    Esito = False

            cam.set_Hostname(name_hostname)
            input("Press a key to continue...")
            break
        elif choice == '5':
            clear()
            print("Update Time and Date Device " + str(cam.get_Hostname()))
            cam.update_system_Date_Time()
            input("Press a key to continue...")
            break
        elif choice == 'r' or choice == 'R':
            clear()
            print("Reboot Device " + str(cam.get_Hostname()))
            cam.reboot()
            input("Press a key to continue...")
            break
        elif choice == 'z' or choice == 'Z':
            clear()
            print("Are you sure you want to soft reset of devive " + str(cam.get_Hostname()) + "? [Yes/No]")
            Esito = True
            answer = ""
            while Esito:
                answer = input("")

                if answer == 'Yes':
                    cam.soft_factory_reset()
                    Esito = False
                elif answer == 'No':
                    Esito = False
                else:
                    print("Invalid input. Try again...")

            input("Press a key to continue...")
            break
        elif choice == 'x' or choice == 'X':
            clear()
            print("Are you sure you want to hard reset of devive " + str(cam.get_Hostname()) + "? [Yes/No]")
            Esito = True
            answer = ""
            while Esito:
                answer = input("")

                if answer == 'Yes':
                    cam.hard_factory_reset()
                    Esito = False
                elif answer == 'No':
                    Esito = False
                else:
                    print("Invalid input. Try again...")

            input("Press a key to continue...")
            break
        else:
            clear()
            print("Invalid number. Try again...")

    show_menu_onvif()

# --------------------- Manu Streaming ------------------------------------
def show_menu_streaming():

    global streaming

    clear()

    while True:
        ## ------------------- Show Streaming menu ---------------------- ##
        print(30 * '-')
        print("   S T R E A M I N G - M E N U")
        print(30 * '-')
        print("1. View Video Live")
        print("2. Save Video Live")
        print("3. Set Frame Rate")
        print("4. View Buffer Frame")

        if streaming.state_save_video() == False:
            print("S. For stopping Save Video Live")

        print("Press Q for return in Main Menu...")
        print("")
        print(30 * '-')

        ## Get input ###
        choice = input('Enter your choice [1-4]: ')

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
        elif choice == '3':
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
        elif choice == '4':
            streaming.view_FrameBuffer()

            clear()
            break
        elif choice == 's' or choice == 'S':
            streaming.stop_save()

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

    #print(cv2.getBuildInformation())

    Streaming_Video.set_parameters('192.168.1.108', 'admin', 'ADMIN2020')
    streaming = Streaming_Video.get_Streaming_Video()

    show_main_menu()

    #Zeep_Framework.prova_zeep()

