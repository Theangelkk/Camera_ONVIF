from Camera_onvif import Camera
from Streaming_Video import Streaming_Video
import cv2
import asyncio
import time

async def main():

    Camera.set_parameters('192.168.1.108', 80, 'project', 'ONVIFADMIN2020')
    cam = Camera.get_camera()

    cam.set_Contrast(cam,50.0)

    cam.set_Resolution(cam,2)

    #print(cv2.getBuildInformation())

    Streaming_Video.set_parameters('192.168.1.108', 'admin', 'ADMIN2020')
    streaming = Streaming_Video.get_Streaming_Video()

    #streaming.live_streaming(streaming)

    streaming.live_streaming(streaming)
    #streaming.set_FrameRate(streaming,1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
