from onvif import ONVIFCamera, exceptions

class Camera:

    # Istanza della classe Camera
    instance = None

    __mycam__ = None

    # Parametri necessari per la connesione
    IP = None
    Port = None
    Username = None
    Password = None
    Setting_Par = False

    # Token Camera
    __main_token__ = None
    __token_encoder__ = None

    # Servizi offerti dal Framework ONVIF
    __media__ = None
    __ptz_service__ = None
    __image__ = None
    __video_sources__ = None

    # Configurazione Servizio Media
    __config_media__ = None
    __option_camera__ = None

    # Configurazione Servizio Imaging
    __config_image__ = None

    # Configurazione Servizio PTZ_Service
    __config_ptz__ = None

    def __init__(self):
        if self.__mycam__ is None:

            # Connessione al dispositivo Onvif
            self.__mycam__ = ONVIFCamera(Camera.IP, Camera.Port, Camera.Username, Camera.Password, './wsdl')

            self.__media__ = self.__mycam__.create_media_service()

            try:
                self.__video_sources__ = self.__media__.GetVideoSources()

                self.__ptz_service__ = self.__mycam__.create_ptz_service()
                self.__image__ = self.__mycam__.create_imaging_service()

                # Token del Profilo Principale
                self.__main_token__ = self.__media__.GetProfiles()[0].token

                # Token del Video Encoder utilizzato
                self.__token_encoder__ = self.__media__.GetVideoEncoderConfigurations()[0].token

                self.get_config_image()
                self.get_config_media()

            except(exceptions.ONVIFError):
                self.__mycam__ = None
                self.__media__ = None

                Camera.reset_parameters()

                print("ONVIF Invalid Username e Password!")

        else:
           raise("You cannot create another Camera class")

    @staticmethod
    def set_parameters(_IP,_Port,_Username,_Password):
        if Camera.Setting_Par is False:
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
        if Camera.Setting_Par:
            Camera.instance = Camera()
        return Camera.instance

    def get_config_media(self):
        self.__config_media__ = self.__media__.GetVideoEncoderConfiguration(self.__token_encoder__)
        self.__option_camera__ = self.__media__.GetVideoEncoderConfigurationOptions(self.__token_encoder__)

    def get_config_image(self):
        self.__config_image__ = self.__image__.GetImagingSettings(self.__token_encoder__)

    '''
    -- Da controllare il metodo get utilizzato per il recupero dei settaggi del servizio PTZ --
    def get_config_ptz(self):
        self.__config_ptz__ = self.__ptz_service__.GetCompatibleConfigurations(Camera.__token__)
    '''

    #------------------ Setting Imaging -------------------------
    # Creazione della richiesta da inviare alla camera relativa alla modifica dei parametri dell'immagine
    def create_request_image(self):
        request_img = self.__image__.create_type('SetImagingSettings')
        request_img.VideoSourceToken = self.__token_encoder__
        request_img.ForcePersistence = True

        return request_img

    def print_config_image(self):
        self.get_config_image()
        print(self.__config_image__)

    def set_Brightness(self,Value_Brightness):

        if(Value_Brightness >= 0.0 and Value_Brightness <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.Brightness = Value_Brightness
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def set_Saturation(self,Value_Saturation):

        if(Value_Saturation >= 0.0 and Value_Saturation <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.ColorSaturation = Value_Saturation
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def set_Sharpness(self,Value_Sharpness):

        if(Value_Sharpness >= 0.0 and Value_Sharpness <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.ColorSharpness = Value_Sharpness
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def set_Contrast(self,Value_Contrast):

        if(Value_Contrast >= 0.0 and Value_Contrast <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.Contrast = Value_Contrast
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

        #--------------- Exposure ------------------------
    def set_Iris(self, Value_Iris):

        if(Value_Iris >= 0.0 and Value_Iris <= 1.0):
            request_img = self.create_request_image()

            self.__config_image__.Exposure.Iris = Value_Iris
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    '''
        #------------- FOCUS ---------------------------
    def set_AutoFocus(self):

        request_img = self.create_request_image()

        WideDynamicRange = {'Mode':'MANUAL','CrGain':90.0,'CbGain':20.0,'Extension':None}

        Camera.__config_image__.WideDynamicRange = WideDynamicRange
        #print(Camera.__config_image__)
        request_img.ImagingSettings = Camera.__config_image__

        Camera.__image__.SetImagingSettings(request_img)
    '''

    # ------------------ Setting Media -------------------------
    # Creazione della richiesta da inviare alla camera relativa alla modifica dei parametri dell'encoder
    def create_request_media(self):
        request_media = self.__media__.create_type('SetVideoEncoderConfiguration')
        request_media.ForcePersistence = True

        return request_media

    def print_config_media(self):
        self.get_config_media()
        print(Camera.__config_media__)

    def get_ResolutionAvailable(self):
        return self.__option_camera__.H264.ResolutionsAvailable

    def set_Resolution(self, Index_Resolution):

        if(Index_Resolution >= 0 and Index_Resolution < len(self.get_ResolutionAvailable())):
            request_media = self.create_request_media()
            self.__config_media__.Resolution = self.__option_camera__.H264.ResolutionsAvailable[Index_Resolution]

            request_media.Configuration = self.__config_media__

            self.__media__.SetVideoEncoderConfiguration(request_media)


    # ------------------ Setting PTZ -------------------------
    def print_config_ptz(self):
        pass

