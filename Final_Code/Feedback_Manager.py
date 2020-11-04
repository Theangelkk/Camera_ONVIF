import zmq
import threading
import simplejson as json
from .Frame_Manager import Frame_Manager
from .Onvif_Manager import Onvif_Manager

class Feedback_Manager(threading.Thread):

    __IP__ = None
    __Port__ = None

    __thread_streaming__ = None

    # Variabili Connessione Socket
    __context__ = None
    __socket__ = None

    def __init__(self, group=None, target=None, ip=None, port=None, thread_streaming=None):
        super(Feedback_Manager, self).__init__(group=group, target=target)

        if self.__context__ is None and self.__socket__ is None and ip is not None and port is not None:

            self.__IP__ = ip
            self.__Port__ = port
            self.__thread_streaming__ = thread_streaming
            self.Threshould_acc = 0.6

            self.Connessione_Onvif()
            self.onvif = Onvif_Manager.get_camera()

            # Creazione Socket Request/Reply
            self.__context__ = zmq.Context()
            self.__socket__ = self.__context__.socket(zmq.REP)
            self.__socket__.bind('tcp://' + str(self.__IP__) + ':' + str(self.__Port__))

    def run(self):

        FirstTime = True

        while True:
            msg = self.__socket__.recv()

            Risposta = {'accuracy': None, 'avg_fps': None}
            self.onvif = Onvif_Manager.get_camera()

            if self.onvif is not None:
                json_request = json.loads(msg, encoding='utf-8')

                print(json_request)

                Risposta = {'accuracy':None,'avg_fps':None}

                # Frame Rate
                if json_request['avg_fps'] is not None:
                    Risposta['avg_fps'] = self.__thread_streaming__.set_FrameRate(int(json_request['avg_fps']))

                if json_request['accuracy'] is not None:
                    if float(json_request['accuracy'] < self.Threshould_acc):
                        Risposta['accuracy'] = self.onvif.set_Focus_Move(0.1)
                    else:
                        Risposta['accuracy'] = False

                self.__socket__.send_string(json.dumps(Risposta))
                FirstTime = True
            else:
                print("Attendo Connessione Camera ONVIF")
                self.Connessione_Onvif()

                if FirstTime:
                    self.__socket__.send_string(json.dumps(Risposta))
                    FirstTime = False

    def Connessione_Onvif(self):
        Onvif_Manager.set_parameters('192.168.1.108', 80, 'project', 'ONVIFADMIN2020')