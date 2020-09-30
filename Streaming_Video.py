import cv2
import time
import threading
import os

import select
import sys

class Streaming_Video:

    instance = None

    IP = None
    Username = None
    Password = None
    Setting_Par = False

    __thread_streaming__ = None
    __thread_save_frame__ = None
    __thread_save_video__ = None

    #__shared_object__ = type('', (), {})()
    __mycam__ = None
    __frame_rate__ = 1
    __BufferFrame__ = []
    __n_item_buffer__ = 0
    __Can_Save__ = True

    def __init__(self):
        if self.__mycam__ is None:
            try:
                uri_rtsp = "" + Streaming_Video.Username + ":" + Streaming_Video.Password + "@" + Streaming_Video.IP + ":554/"
                self.__mycam__ = cv2.VideoCapture("rtsp://" + uri_rtsp, cv2.CAP_FFMPEG)
                print(self.__mycam__.isOpened())

                self.set_FrameRate(10)
                self.__thread_save_frame__ = Thread_Saving_Frame(obj_MainStreaming=self)
                self.__thread_save_frame__.start()
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
        if self.__thread_streaming__ is None:
            self.__thread_streaming__ = Thread_Live_Streaming(obj_MainStreaming=self)
            self.__thread_streaming__.start()
        else:
            if self.__thread_streaming__.isAlive() == False:
                self.__thread_streaming__.start()
            else:
                print("Thread Streaming gia' in esecuzione!")

    #----------------- Metodi Get --------------------------
    @staticmethod
    def get_Streaming_Video():
        if Streaming_Video.__mycam__ is None and Streaming_Video.Setting_Par:
            Streaming_Video.instance = Streaming_Video()
        return Streaming_Video.instance

    def get_FrameRate(self):
        return self.__frame_rate__

    def get_itemBuffer(self):
        return len(self.__BufferFrame__)

    #----------------- Metodi Set --------------------------
    @staticmethod
    def set_parameters(_IP, _Username, _Password):
        if Streaming_Video.__mycam__ is None:
            Streaming_Video.IP = _IP
            Streaming_Video.Username = _Username
            Streaming_Video.Password = _Password
            Streaming_Video.Setting_Par = True

    def set_FrameRate(self,FrameRate):
        self.__frame_rate__ = FrameRate

    #---------------- Utility Method -------------------------
    def view_FrameBuffer(self):
        for item in self.__BufferFrame__:
            frame = item["Image"]
            cv2.imshow("View Buffer Frame", frame)
            cv2.waitKey()

    def state_save_video(self):
        return self.__Can_Save__

    def save_Video(self):

        if self.__thread_save_video__ is not None:
            if self.__thread_save_video__.isAlive == False:
                self.__Can_Save__ = False

        if self.__Can_Save__:
            Esito = True
            name_video = ""

            while Esito:
                name_video = input("Enter video name: ")
                name_video = "Video/" + name_video + ".avi"

                if os.path.exists(name_video):
                    name_video = ""
                    print("File exist...")
                else:
                    Esito = False

            self.__thread_save_video__ = Thread_Video_Save(obj_MainStreaming=self, name_video=name_video)
            self.__thread_save_video__.start()

            self.__Can_Save__ = False
        else:
            print("Thread Save Video is running...")

    def stop_save(self):
        self.__thread_save_video__.stop()
        self.__thread_save_video__ = None
        self.__Can_Save__ = True

class Thread_Live_Streaming(threading.Thread):

    def __init__(self, group=None, target=None, obj_MainStreaming=None):
        super(Thread_Live_Streaming,self).__init__(group=group, target=target)
        self.obj_MainStreaming = obj_MainStreaming
        self.mutex = threading.Lock()

        return

    def run(self):
        print("Thread Live Streaming is started...")

        while self.obj_MainStreaming.__mycam__.isOpened():
            ret, frame = self.obj_MainStreaming.__mycam__.read()

            #with self.mutex:
                #cv2.imshow("Live Streaming Camera", frame)

            #io.imshow(frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                return 0

class Thread_Saving_Frame(threading.Thread):

    def __init__(self, group=None, target=None, obj_MainStreaming=None, buffer=None):
        super(Thread_Saving_Frame,self).__init__(group=group, target=target)
        self.obj_MainStreaming = obj_MainStreaming
        self.mutex = threading.Lock()

        return

    def run(self):
        __time_prev_frame__ = 0.0

        print("Saving Streaming Thread is started...")
        while self.obj_MainStreaming.__mycam__.isOpened():
            ret, frame = self.obj_MainStreaming.__mycam__.read()

            time_frame = time.time() - __time_prev_frame__

            # Salvataggio Frame
            if time_frame > 1. / self.obj_MainStreaming.__frame_rate__:
                __time_prev_frame__ = time.time()

                named_tuple = time.localtime()  # get struct_time
                time_string = time.strftime("%H:%M:%S", named_tuple)

                item = {'Image': frame, 'Time': time_string, 'ID': self.obj_MainStreaming.__n_item_buffer__}

                with self.mutex:
                    self.obj_MainStreaming.__BufferFrame__.append(item)
                    self.obj_MainStreaming.__n_item_buffer__ += 1

            if self.obj_MainStreaming.__n_item_buffer__ > 5:
                #print("Saving Streaming Thread is terminated")
                return 0

class Thread_Video_Save(threading.Thread):

    def __init__(self, group=None, target=None, obj_MainStreaming=None, name_video=None):
        super(Thread_Video_Save,self).__init__(group=group, target=target)
        self.obj_MainStreaming = obj_MainStreaming
        self.name_video = name_video
        self.mutex = threading.Lock()
        self.finish = True

        return

    def setFileName(self, filename):
        self.name_video = filename

    def run(self):
        print("Thread Save Video is started...")
        print("For stopping the recording, press the key S")

        height = None
        width = None

        self.video_writer = None
        self.finish = True
        try:
            print(self.obj_MainStreaming.__mycam__.isOpened())
            if self.obj_MainStreaming.__mycam__.isOpened():
                ret, frame = self.obj_MainStreaming.__mycam__.read()
                height = frame.shape[0]
                width = frame.shape[1]

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.video_writer = cv2.VideoWriter(self.name_video, fourcc, self.obj_MainStreaming.__frame_rate__, (width, height))


            while self.obj_MainStreaming.__mycam__.isOpened() and self.finish:
                ret, frame = self.obj_MainStreaming.__mycam__.read()

                # write the flipped frame
                self.video_writer.write(frame)
        except:
            pass

    def stop(self):
        self.video_writer.release()
        self.obj_MainStreaming.__Can_Save__ = True
        self.finish = False
        print("Thread_Video_Save is terminated")
        return 0