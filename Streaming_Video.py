import cv2
import asyncio
import time

class Streaming_Video:

    IP = None
    Username = None
    Password = None
    Setting_Par = False

    __process_streaming__ = None
    __thread_save_frame__ = None

    __shared_object__ = type('', (), {})()
    __shared_object__.__mycam__ = None

    def __init__(self):
        if self.__shared_object__.__mycam__ is None:
            try:
                #pipe_GStreamer = "rtspsrc location=rtsp://" + Streaming_Video.Username + ":" + Streaming_Video.Password + "@" + Streaming_Video.IP + "/ latency=200 ! queue ! rtph264depay ! appsink"
                self.__shared_object__.__mycam__ = cv2.VideoCapture("rtsp://" + Streaming_Video.Username + ":" + Streaming_Video.Password + "@" + Streaming_Video.IP + "/")
                #Streaming_Video.__mycam__ = cv2.VideoCapture(pipe_GStreamer,cv2.CAP_GSTREAMER)

                self.__shared_object__.__frame_rate__ = 1
                self.__shared_object__.__BufferFrame__ = []
                self.__shared_object__.__n_item_buffer__ = 0

                self.set_FrameRate(10)
                self.__thread_save_frame__ = asyncio.gather(self.__saving_frame_thread(self.__shared_object__))
            except:
                Streaming_Video.reset_parameters()
                print("Streaming Invalid Username e Password!")
        else:
            raise ("You cannot create another Streaming_Video class")

    @staticmethod
    def reset_parameters():
        Streaming_Video.IP = None
        Streaming_Video.Username = None
        Streaming_Video.Password = None
        Streaming_Video.Setting_Par = False

    def live_streaming(self):
        print("pippo")
        if self.__process_streaming__ is None:
            self.__process_streaming__ = asyncio.gather(self.__live_streaming_thread(self,self.__shared_object__))
        else:
            if self.__process_streaming__.done() == True:
                self.__process_streaming__ = asyncio.gather(self.__live_streaming_thread(self,self.__shared_object__))
            else:
                print("Thread Streaming gia' in esecuzione!")

    async def __live_streaming_thread(self,__shared_object__):
        print("Sono partito")
        print(len(__shared_object__.__BufferFrame__))
        while __shared_object__.__mycam__.isOpened():
            ret, frame = __shared_object__.__mycam__.read()

            cv2.imshow("Live Streaming Camera", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                return 0

    async def __saving_frame_thread(self,__shared_object__):
        __time_prev_frame__ = 0.0
        while __shared_object__.__mycam__.isOpened():
            ret, frame = __shared_object__.__mycam__.read()

            time_frame = time.time() - __time_prev_frame__

            # Salvataggio Frame
            if time_frame > 1./__shared_object__.__frame_rate__:

                #print(self.__frame_rate__)

                __time_prev_frame__ = time.time()

                named_tuple = time.localtime()  # get struct_time
                time_string = time.strftime("%H:%M:%S", named_tuple)

                #print(time_string)

                item = {'Image':frame, 'Time':time_string, 'ID':__shared_object__.__n_item_buffer__}
                __shared_object__.__BufferFrame__.append(item)

                __shared_object__.__n_item_buffer__ += 1

                #print(__shared_object__.__n_item_buffer__)

            if __shared_object__.__n_item_buffer__ > 5:
                print("Sono morto")
                return 0

    #----------------- Metodi Get --------------------------
    @staticmethod
    def get_Streaming_Video():
        if Streaming_Video.__shared_object__.__mycam__ is None and Streaming_Video.Setting_Par:
            Streaming_Video()
        return Streaming_Video

    def get_FrameRate(self):
        return self.__shared_object__.__frame_rate__

    def get_itemBuffer(self):
        print(self.__shared_object__.__frame_rate__)

    #----------------- Metodi Set --------------------------
    @staticmethod
    def set_parameters(_IP, _Username, _Password):
        if Streaming_Video.__shared_object__.__mycam__ is None:
            Streaming_Video.IP = _IP
            Streaming_Video.Username = _Username
            Streaming_Video.Password = _Password
            Streaming_Video.Setting_Par = True

    def set_FrameRate(self,FrameRate):
        self.__shared_object__.__frame_rate__ = FrameRate

        #print(self.__frame_rate__)

