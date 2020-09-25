from onvif import ONVIFCamera

def prova_zeep():

    cam = ONVIFCamera('192.168.1.108', 80, 'project', 'ONVIFADMIN2020', './wsdl')

    media = cam.create_media_service()

    print(media.GetProfiles())
    token_main = 'MediaProfile000'

    profile = media.GetProfile(token_main)

    #print(profile)

    token_video_encod_conf = profile.VideoEncoderConfiguration.token

    #print(media.GetVideoEncoderConfiguration(token_video_encod_conf))

    video_source = media.GetVideoSources()[0]
    #print(video_source)

    #print(media.GetVideoSourceConfiguration(video_source.token))

    image = cam.create_imaging_service()

    #print(image.GetImagingSettings(video_source.token))
    #print(image.GetOptions(video_source.token))

