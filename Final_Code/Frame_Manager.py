import cv2
import zmq
import threading
import time
from .Thread_Frame import Thread_Frame

class Frame_Manager(threading.Thread):

    __IP__ = None
    __Username__ = None
    __Password__ = None

    __thread_frame__ = None

    __mycam__ = None
    __frame_rate__ = 1
    __BufferFrame__ = []
    __n_item_buffer__ = 0

    __frame_no_send__ = 0

    # Variabili Connessione Socket
    __context__ = None
    __socket__ = None

    __height_frame__ = 320
    __width_frame__ = 320

    __Attiva_Invio__ = True
    __Save_Frame__ = False

    def __init__(self, group=None, target=None, ip=None, username=None, password=None):
        super(Frame_Manager, self).__init__(group=group, target=target)
        # Se la connessione con la camera non è stata ancora avviata...
        if self.__mycam__ is None and ip is not None and username is not None and password is not None:
            try:
                self.__IP__ = ip
                self.__Username__ = username
                self.__Password__ = password

                self.Connessione_Camera()

                #self.__mycam__ = cv2.VideoCapture("/Users/cvprlabalfredopetrosino/Downloads/Video_Camera/quinto.mp4")
                self.set_FrameRate(6)

                # Creazione socket con Car Detection
                self.create_socket_connection()
            except:
                print("Streaming Invalid Username e Password!")
        else:
            raise ("You cannot create another Streaming_Video class")

    def Connessione_Camera(self):
        self.__mycam__ = cv2.VideoCapture("rtsp://" + self.__Username__ + ":" + self.__Password__ + "@" + self.__IP__ + "/")

    def create_socket_connection(self):

        if self.__context__ is None and self.__socket__ is None:
            # Creazione Socket Publisher
            self.__context__ = zmq.Context()
            self.__socket__ = self.__context__.socket(zmq.PUB)
            self.__socket__.bind('tcp://*:10000')

    def run(self):
        if self.__thread_frame__ is None:
            self.__thread_frame__ = Thread_Frame(obj_FrameManager=self)

            self.__thread_frame__.start()

        while True:
            pass

    def set_FrameRate(self,FrameRate):

        if FrameRate > 0 and FrameRate < 26:
            self.__frame_rate__ = FrameRate
            return True

        return False

    def set_Height(self, height):

        if height >= 320 and height <= 1520:
            self.__height_frame__ = height
            return True

        return False

    def set_Width(self, width):

        if width >= 320 and width <= 2688:
            self.__width_frame__ = width
            return True

        return False

    def set_Invio_Frame(self,Invio_Frame):

        self.__Attiva_Invio__ = Invio_Frame

    def set_Save_Frame(self, Esito):

        self.__Save_Frame__ = Esito


