import zmq
import threading
import simplejson as json
from .Frame_Manager import Frame_Manager

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

            # Creazione Socket Publisher
            self.__context__ = zmq.Context()
            self.__socket__ = self.__context__.socket(zmq.REP)
            self.__socket__.bind('tcp://' + str(self.__IP__) + ':' + str(self.__Port__))

    def run(self):

        while True:
            msg = self.__socket__.recv()

            json_request = json.loads(msg, encoding='utf-8')

            print(json_request)

            Risposta = {'FrameRate':None,'Height':None,'Width':None}

            if json_request['FrameRate'] is not None:
                Risposta['FrameRate'] = self.__thread_streaming__.set_FrameRate(int(json_request['FrameRate']))

            if json_request['Height'] is not None:
                Risposta['Height'] = self.__thread_streaming__.set_Height(int(json_request['Height']))

            if json_request['Width'] is not None:
                Risposta['Width'] = self.__thread_streaming__.set_Width(int(json_request['Width']))

            self.__socket__.send_string(json.dumps(Risposta))