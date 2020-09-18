from Camera_onvif import Camera
from Streaming_Video import Streaming_Video

Camera.set_parameters('192.168.1.108', 80, 'project', 'ONVIFADMIN2020')
cam = Camera.get_camera()

cam.set_Contrast(cam,50.0)

cam.set_Resolution(cam,2)

Streaming_Video.set_parameters('192.168.1.108', 'admin', 'ADMIN2020')
streaming = Streaming_Video.get_Streaming_Video()

streaming.live_streaming(streaming)

print("ciao")
