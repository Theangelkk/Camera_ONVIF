import threading
import time
import cv2
import base64
import zmq
import simplejson as json

class Thread_Frame(threading.Thread):

    def __init__(self, group=None, target=None, obj_FrameManager=None):
        super(Thread_Frame,self).__init__(group=group, target=target)
        self.obj_FrameManager = obj_FrameManager

        self.__time_prev_frame__ = 0.0

    def run(self):

        print("Saving Streaming Thread is started...")

        while True:

            if self.obj_FrameManager.__mycam__.isOpened():

                if self.obj_FrameManager.__Attiva_Invio__:
                    # Cattura il Frame Corrente
                    ret, frame = self.obj_FrameManager.__mycam__.read()

                    #if ret:  # per avere il loop del video

                    if frame is not None:
                        time_frame = time.time() - self.__time_prev_frame__

                        # Invio (o Salvataggio) Frame
                        if time_frame > 1. / self.obj_FrameManager.__frame_rate__:
                            self.__time_prev_frame__ = time.time()

                            # Prendere il tempo attuale
                            named_tuple = time.localtime()
                            time_string = time.strftime("%H:%M:%S", named_tuple)

                            # Resize Frame
                            #frame = cv2.resize(frame, (self.obj_FrameManager.__width_frame__,self.obj_FrameManager.__height_frame__))

                            # Encode Base64
                            encoded, buffer = cv2.imencode('.jpg', frame)
                            frame_64 = base64.b64encode(buffer)

                            # Creazione elemento Json
                            item = {'Image': frame_64, 'Time': time_string, 'ID': self.obj_FrameManager.__n_item_buffer__}

                            # Invio Frame Client
                            self.obj_FrameManager.__socket__.send_string(json.dumps(item), zmq.NOBLOCK)

                            # Salvataggio Frame Buffer
                            if self.obj_FrameManager.__Save_Frame__:
                                self.obj_FrameManager.__BufferFrame__.append(item)

                            self.obj_FrameManager.__n_item_buffer__ += 1

                        #else:  # per avere il video in loop
                            #self.obj_FrameManager.__mycam__.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    else:
                        print("Attendo Riconnessione")
                        self.obj_FrameManager.Connessione_Camera()
            else:
                print("Attendo Connessione")
                self.obj_FrameManager.Connessione_Camera()
