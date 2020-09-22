from onvif import ONVIFCamera, exceptions

class Camera:

    instance = None

    __mycam__ = None
    IP = None
    Port = None
    Username = None
    Password = None
    Setting_Par = False

    __token__ = None
    __media__ = None
    _ptz_service__ = None
    __image__ = None
    __video_sources__ = None

    __config_media__ = None
    __option_camera__ = None

    __config_image__ = None

    def __init__(self):
        if Camera.__mycam__ is None:
            Camera.__mycam__ = ONVIFCamera(Camera.IP, Camera.Port, Camera.Username, Camera.Password, './wsdl')

            Camera.__media__ = Camera.__mycam__.create_media_service()

            try:
                Camera.__video_sources__ = Camera.__media__.GetVideoSources()

                Camera.__ptz_service__ = Camera.__mycam__.create_ptz_service()
                Camera.__image__ = Camera.__mycam__.create_imaging_service()

                Camera.__token__ = Camera.__media__.GetVideoEncoderConfigurations()[0].token

                self.get_config_image()
                self.get_config_media()

            except(exceptions.ONVIFError):
                Camera.__mycam__ = None
                Camera.__media__ = None

                Camera.reset_parameters()

                print("ONVIF Invalid Username e Password!")

        else:
           raise("You cannot create another Camera class")

    @staticmethod
    def set_parameters(_IP,_Port,_Username,_Password):
        if Camera.__mycam__ is None:
            Camera.IP = _IP
            Camera.Port = _Port
            Camera.Username = _Username
            Camera.Password = _Password
            Camera.Setting_Par = True

    @staticmethod
    def reset_parameters():
        Camera.IP = None
        Camera.Port = None
        Camera.Username = None
        Camera.Password = None
        Camera.Setting_Par = False


    @staticmethod
    def get_camera():
        if Camera.__mycam__ is None and Camera.Setting_Par:
            Camera.instance = Camera()
        return Camera.instance

    def get_config_media(self):
        Camera.__config_media__ = Camera.__media__.GetVideoEncoderConfiguration(Camera.__token__)
        Camera.__option_camera__ = Camera.__media__.GetVideoEncoderConfigurationOptions(Camera.__token__)

    def get_config_image(self):
        Camera.__config_image__ = Camera.__image__.GetImagingSettings(Camera.__token__)

    #------------------ Setting Imaging -------------------------
    def create_request_image(self):
        request_img = Camera.__image__.create_type('SetImagingSettings')
        request_img.VideoSourceToken = Camera.__token__
        request_img.ForcePersistence = True

        return request_img

    def set_Contrast(self,Value_Contrast):

        if(Value_Contrast >= 0.0 and Value_Contrast <= 100.0):
            request_img = self.create_request_image(self)

            Camera.__config_image__.Contrast = Value_Contrast
            request_img.ImagingSettings = Camera.__config_image__

            Camera.__image__.SetImagingSettings(request_img)

    # ------------------ Setting Media -------------------------
    def create_request_media(self):
        request_media = Camera.__media__.create_type('SetVideoEncoderConfiguration')
        request_media.ForcePersistence = True

        return request_media

    def get_ResolutionAvailable(self):
        return Camera.__option_camera__.H264.ResolutionsAvailable

    def set_Resolution(self, Index_Resolution):

        if(Index_Resolution >= 0 and Index_Resolution < len(self.get_ResolutionAvailable(self))):
            request_media = self.create_request_media(self)
            Camera.__config_media__.Resolution = Camera.__option_camera__.H264.ResolutionsAvailable[Index_Resolution]

            request_media.Configuration = Camera.__config_media__

            Camera.__media__.SetVideoEncoderConfiguration(request_media)




