from onvif import ONVIFCamera, exceptions
import time

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

    # Configurazione Servizio Device Managment
    __device_mgmt__ = None

    # Configurazione Servizio Media
    __all_profiles__ = None
    __main_profile__ = None

    __config_media__ = None
    __option_camera__ = None

    __config_metadata__ = None
    __option_metadata__ = None

    __config_videosources__ = None
    __option_videosources__ = None

    __config_video_source_modes__ = None
    __option_media_capabilities__ = None

    # Configurazione Servizio Imaging
    __config_image__ = None
    __option_image__ = None

    __option_image_capabilities__ = None

    __config_move__ = None
    __option_move__ = None

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

                self.get_device_management()
                self.get_config_image()
                self.get_config_media()

                self.update_system_Date_Time()

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

        self.__all_profiles__ = self.__media__.GetProfiles()
        self.__main_profile__ = self.__all_profiles__[0]

        self.__config_media__ = self.__media__.GetVideoEncoderConfiguration(self.__token_encoder__)
        self.__option_camera__ = self.__media__.GetVideoEncoderConfigurationOptions(self.__token_encoder__)

        self.__config_metadata__ = self.__media__.GetMetadataConfiguration(self.__token_encoder__)
        self.__option_metadata__ = self.__media__.GetMetadataConfigurationOptions(self.__token_encoder__)

        self.__config_videosources__ = self.__main_profile__.VideoSourceConfiguration
        self.__option_videosources__ = self.__media__.GetVideoSourceConfigurationOptions(self.__token_encoder__)

        self.__option_media_capabilities__ = self.__media__.GetServiceCapabilities()


        #self.__config_video_source_modes__ = self.__media__.GetVideoSourceModes(self.__token_encoder__)

    def get_config_image(self):
        self.__config_image__ = self.__image__.GetImagingSettings(self.__token_encoder__)
        self.__option_image__ = self.__image__.GetOptions(self.__token_encoder__)

        self.__option_image_capabilities__ = self.__image__.GetServiceCapabilities()

        self.__config_move__ = self.__image__.GetStatus(self.__token_encoder__)
        self.__option_move__ = self.__image__.GetMoveOptions(self.__token_encoder__)


    '''
    -- Da controllare il metodo get utilizzato per il recupero dei settaggi del servizio PTZ --
    def get_config_ptz(self):
        self.__config_ptz__ = self.__ptz_service__.GetCompatibleConfigurations(Camera.__token__)
    '''

    # ------------------ Setting Core ---------------------------
    def get_device_management(self):
        self.__device_mgmt__ = self.__mycam__.devicemgmt

    def get_Hostname(self):
        return self.__device_mgmt__.GetHostname().Name

    def set_Hostname(self, name):
        request_device = self.__device_mgmt__.create_type("SetHostname")

        request_device.Name = name

        self.__device_mgmt__.SetHostname(request_device)

    def get_all_information_device(self):
        return self.__device_mgmt__.GetDeviceInformation()

    '''
        This operation is used to retrieve URIs from which system information may be downloaded using HTTP. 
        URIs may be returned for the following system information:
            -   System Logs:                Multiple system logs may be returned, of different types.  
                                            The exact format of the system logs is outside the scope of this specification.
            -   Support  Information:       This consists of arbitrary device diagnostics information from a device.  
                                            The exact format of the diagnostic information is outside the scope of this specification.
            -   System  Backup:             The received file is a backup file that can be used to restore the current device configuration  
                                            at a later date.  
                                            The exact format of the backup configuration file is outside the scope of this specification.
    
        Non sono stati implementati i seguenti metodi:
            -   GetSystemUris
            -   GetSystemBackup
            -   GetSystemLog
    '''
    def get_system_Date_Time(self):
        return self.__device_mgmt__.GetSystemDateAndTime()

    def update_system_Date_Time(self):
        request_device = self.__device_mgmt__.create_type("SetSystemDateAndTime")

        actual_time = time.localtime()

        request_device.DateTimeType = 'Manual'
        request_device.DaylightSavings = True
        request_device.TimeZone = {'TZ':'CST-0:00:00'}
        request_device.UTCDateTime = {
                                        'Date':{'Year':actual_time.tm_year,'Month':actual_time.tm_mon,'Day':actual_time.tm_mday},\
                                        'Time':{'Hour':actual_time.tm_hour,'Minute':actual_time.tm_min,'Second':actual_time.tm_sec}
                                    }

        self.__device_mgmt__.SetSystemDateAndTime(request_device)

    def reboot(self):
        self.__device_mgmt__.SystemReboot()

    def soft_factory_reset(self):
        request_device = self.__device_mgmt__.create_type("SetSystemFactoryDefault")

        request_device.FactoryDefault = 'Soft'

        self.__device_mgmt__.SetSystemFactoryDefault(request_device)

    def hard_factory_reset(self):
        request_device = self.__device_mgmt__.create_type("SetSystemFactoryDefault")

        request_device.FactoryDefault = 'Hard'

        self.__device_mgmt__.SetSystemFactoryDefault(request_device)

    #------------------ Setting Imaging -------------------------
    # Creazione della richiesta da inviare alla camera relativa alla modifica dei parametri dell'immagine
    def create_request_image(self):
        request_img = self.__image__.create_type('SetImagingSettings')
        request_img.VideoSourceToken = self.__token_encoder__
        request_img.ForcePersistence = True

        return request_img

    def create_request_focus(self):
        request_focus = self.__image__.create_type('Move')
        request_focus.VideoSourceToken = self.__token_encoder__

        return request_focus

    def print_config_image(self):
        self.get_config_image()
        print(self.__config_image__)

    def print_options_image__(self):
        self.get_config_image()
        print(self.__option_image__)

    def print_config_move(self):
        self.get_config_image()
        print(self.__config_move__)

    def print_options_move__(self):
        self.get_config_image()
        print(self.__option_move__)

    def print_option_image_capabilities(self):
        self.get_config_image()
        print(self.__option_image_capabilities__)

    def get_Brightness(self):
        return self.__config_image__.Brightness

    def set_Brightness(self,Value_Brightness):

        if(Value_Brightness >= 0.0 and Value_Brightness <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.Brightness = Value_Brightness
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def get_Saturation(self):
        return self.__config_image__.ColorSaturation

    def set_Saturation(self,Value_Saturation):

        if(Value_Saturation >= 0.0 and Value_Saturation <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.ColorSaturation = Value_Saturation
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def get_Sharpness(self):
        return self.__config_image__.Sharpness

    def set_Sharpness(self,Value_Sharpness):

        if(Value_Sharpness >= 0.0 and Value_Sharpness <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.Sharpness = Value_Sharpness
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def get_Contrast(self):
        return self.__config_image__.Contrast

    def set_Contrast(self,Value_Contrast):

        if(Value_Contrast >= 0.0 and Value_Contrast <= 100.0):
            request_img = self.create_request_image()

            self.__config_image__.Contrast = Value_Contrast
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

        #--------------- Exposure ------------------------
    def get_Iris(self):
        return self.__config_image__.Exposure.Iris

    def set_Iris(self, Value_Iris):

        if(Value_Iris >= 0.0 and Value_Iris <= 1.0):
            request_img = self.create_request_image()

            self.__config_image__.Exposure.Iris = Value_Iris
            request_img.ImagingSettings = self.__config_image__

            self.__image__.SetImagingSettings(request_img)

    def get_Focus_Position(self):
        return self.__config_move__.FocusStatus20.Position

    def set_Focus_Move(self, Value_Position):

        if (Value_Position >= 0.0 and Value_Position <= 1.0):
            request_focus = self.create_request_focus()

            request_focus.Focus = {'Absolute': {'Position': Value_Position, 'Speed': None}, \
                                   'Relative': {'Distance': Value_Position, 'Speed': None}, \
                                   'Continuous': {'Speed': 0.0}}

            self.__image__.Move(request_focus)
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

    def print_all_profiles(self):
        self.get_config_media()
        print(self.__all_profiles__)

    def print_main_profile(self):
        self.get_config_media()
        print(self.__main_profile__)

    def print_config_media(self):
        self.get_config_media()
        print(self.__config_media__)

    def print_options_config_media(self):
        self.get_config_media()
        print(self.__option_camera__)

    def print_config_metadata(self):
        self.get_config_media()
        print(self.__config_metadata__)

    def print_options_config_metadata(self):
        self.get_config_media()
        print(self.__option_metadata__)

    def print_config_videosources(self):
        self.get_config_media()
        print(self.__config_videosources__)

    def print_options_config_videosources(self):
        self.get_config_media()
        print(self.__option_videosources__)

    def print_config_videosources_modes(self):
        self.get_config_media()
        print(self.__config_video_source_modes__)

    def print_option_media_capabilities__(self):
        self.get_config_media()
        print(self.__option_media_capabilities__)

    def get_ResolutionAvailable(self):
        return self.__option_camera__.H264.ResolutionsAvailable

    def get_Resolution(self):
        return self.__config_media__.Resolution

    def set_Resolution(self, Index_Resolution):

        if(Index_Resolution >= 0 and Index_Resolution < len(self.get_ResolutionAvailable())):
            request_media = self.create_request_media()
            self.__config_media__.Resolution = self.__option_camera__.H264.ResolutionsAvailable[Index_Resolution]

            request_media.Configuration = self.__config_media__

            self.__media__.SetVideoEncoderConfiguration(request_media)

    def get_Options_QualityRange(self):
        min = int(self.__option_camera__.QualityRange.Min)
        max = int(self.__option_camera__.QualityRange.Max)

        return min,max

    def get_QualityRange(self):
        return self.__config_media__.Quality

    def set_QualityRange(self, value_QualityRange):

        min,max = self.get_Options_QualityRange()

        if(value_QualityRange > min and value_QualityRange < max):
            request_media = self.create_request_media()
            self.__config_media__.Quality = value_QualityRange

            request_media.Configuration = self.__config_media__

            self.__media__.SetVideoEncoderConfiguration(request_media)

    '''
        The GOV length of an H.264 stream is the sum total of I-frames and P-frames in a GOV (Group
        of video images). An I-frame, or intra frame, is an image that is coded in its entirety. A P-frame,
        or predictive inter frame, refers to parts of earlier images (I-frames and/or P-frames) to code the
        frame and therefore uses less bits to transmit the image. Increasing the GOV length decreases
        the frequency of I-frames, and therefore reduces bandwidth consumption and image quality.
    '''
    def get_Options_GovLengthRange(self):
        min = int(self.__option_camera__.H264.GovLengthRange.Min)
        max = int(self.__option_camera__.H264.GovLengthRange.Max)

        return min,max

    def get_GovLengthRange(self):
        return self.__config_media__.H264.GovLength

    def set_GovLengthRange(self, value_GovLengthRange):

        min,max = self.get_Options_GovLengthRange()

        if(value_GovLengthRange > min and value_GovLengthRange < max):
            request_media = self.create_request_media()
            self.__config_media__.H264.GovLength = value_GovLengthRange

            request_media.Configuration = self.__config_media__

            self.__media__.SetVideoEncoderConfiguration(request_media)

    def get_Options_FrameRate(self):
        min = int(self.__option_camera__.H264.FrameRateRange.Min)
        max = int(self.__option_camera__.H264.FrameRateRange.Max)

        return min,max

    def get_FrameRate(self):
        return self.__config_media__.RateControl.FrameRateLimit

    # NON FUNZIONA
    def set_FrameRate(self, value_FrameRate):

        min,max = self.get_Options_FrameRate()

        if(value_FrameRate > min and value_FrameRate < max):
            request_media = self.create_request_media()
            self.__config_media__.RateControl.FrameRateLimit = value_FrameRate

            request_media.Configuration = self.__config_media__

            self.__media__.SetVideoEncoderConfiguration(request_media)

    # ------------------ Setting PTZ -------------------------
    def print_config_ptz(self):
        pass

