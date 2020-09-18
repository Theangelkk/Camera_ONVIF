import cv2
import _thread

class Streaming_Video:

    __mycam__ = None

    IP = None
    Username = None
    Password = None
    Setting_Par = False

    __thread_streaming__ = None

    def __init__(self):
        if Streaming_Video.__mycam__ is None:
            try:
                Streaming_Video.__mycam__ = cv2.VideoCapture("rtsp://" + Streaming_Video.Username + ":" + Streaming_Video.Password + "@" + Streaming_Video.IP + "/")
            except:
                Streaming_Video.reset_parameters()
                print("Invalid Username e Password!")
        else:
            raise ("You cannot create another Streaming_Video class")

    @staticmethod
    def set_parameters(_IP, _Username, _Password):
        if Streaming_Video.__mycam__ is None:
            Streaming_Video.IP = _IP
            Streaming_Video.Username = _Username
            Streaming_Video.Password = _Password
            Streaming_Video.Setting_Par = True

    @staticmethod
    def reset_parameters():
        Streaming_Video.IP = None
        Streaming_Video.Username = None
        Streaming_Video.Password = None
        Streaming_Video.Setting_Par = False

    @staticmethod
    def get_Streaming_Video():
        if Streaming_Video.__mycam__ is None and Streaming_Video.Setting_Par:
            Streaming_Video()
        return Streaming_Video

    def live_streaming(self):

        if self.__thread_streaming__ is None:
            self.__thread_streaming__ = _thread.start_new_thread(self.__live_streaming_thread(self))
        else:
            if self.__thread_streaming__.isAlive() == False:
                self.__thread_streaming__ = _thread.start_new_thread(self.__live_streaming_thread(self))

    def __live_streaming_thread(self):
        while True:
            ret, frame = self.__mycam__.read()

            cv2.imshow("Live Streaming Camera", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break
