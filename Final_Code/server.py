from Final_Code.Frame_Manager import Frame_Manager
from Final_Code.Feedback_Manager import Feedback_Manager

server_frame = None
server_feedback = None

if __name__ == '__main__':

    server_frame = Frame_Manager(ip='192.168.1.108', username='admin', password='ADMIN2020')
    server_feedback = Feedback_Manager(ip='127.0.0.1', port='20000', thread_streaming=server_frame)

    server_frame.start()
    server_feedback.start()

    server_frame.join()
    server_feedback.join()