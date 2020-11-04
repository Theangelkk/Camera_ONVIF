from onvif import ONVIFCamera, exceptions
import time

class Onvif_Manager:

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
    __image__ = None
    __video_sources__ = None

    # Configurazione Servizio Device Managment
    __device_mgmt__ = None

    __main_profile__ = None
    __config_media__ = None
    __config_videosources__ = None
    __option_camera__ = None

    __config_image__ = None
    __config_move__ = None

    def __init__(self):
        if self.__mycam__ is None:

            # Connessione al dispositivo Onvif
            self.__mycam__ = ONVIFCamera(Onvif_Manager.IP, Onvif_Manager.Port, Onvif_Manager.Username, Onvif_Manager.Password, '../wsdl')

            self.__media__ = self.__mycam__.create_media_service()

            try:
                self.__video_sources__ = self.__media__.GetVideoSources()

                self.__image__ = self.__mycam__.create_imaging_service()

                # Token del Profilo Principale
                self.__main_token__ = self.__media__.GetProfiles()[0].token

                # Token del Video Encoder utilizzato
                self.__token_encoder__ = self.__media__.GetVideoEncoderConfigurations()[0].token

                self.get_device_management()
                self.get_config_image()
                self.get_config_media()

                self.update_system_Date_Time()

                Onvif_Manager.instance = self

            except(exceptions.ONVIFError):
                self.__mycam__ = None
                self.__media__ = None

                Onvif_Manager.reset_parameters()

                print("ONVIF Invalid Username e Password!")

        else:
           raise("You cannot create another Camera class")

    @staticmethod
    def set_parameters(_IP, _Port, _Username, _Password):
        if Onvif_Manager.Setting_Par is False:
            Onvif_Manager.IP = _IP
            Onvif_Manager.Port = _Port
            Onvif_Manager.Username = _Username
            Onvif_Manager.Password = _Password
            Onvif_Manager.Setting_Par = True

    @staticmethod
    def reset_parameters():
        Onvif_Manager.instance = None
        Onvif_Manager.IP = None
        Onvif_Manager.Port = None
        Onvif_Manager.Username = None
        Onvif_Manager.Password = None
        Onvif_Manager.Setting_Par = False

    @staticmethod
    def get_camera():
        if Onvif_Manager.Setting_Par and Onvif_Manager.instance is None:
            Onvif_Manager()
        return Onvif_Manager.instance

    def get_config_media(self):

        self.__main_profile__ = self.__media__.GetProfiles()[0]
        self.__config_media__ = self.__media__.GetVideoEncoderConfiguration(self.__token_encoder__)
        self.__config_videosources__ = self.__main_profile__.VideoSourceConfiguration
        self.__option_camera__ = self.__media__.GetVideoEncoderConfigurationOptions(self.__token_encoder__)

    def get_config_image(self):

        self.__config_image__ = self.__image__.GetImagingSettings(self.__token_encoder__)
        self.__config_move__ = self.__image__.GetStatus(self.__token_encoder__)

    # ------------------ Setting Core ---------------------------
    def get_device_management(self):
        self.__device_mgmt__ = self.__mycam__.devicemgmt

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

    # ------------------ Setting Imaging -------------------------
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

    def set_Brightness(self,Value_Brightness):

        try:
            if(Value_Brightness >= 0.0 and Value_Brightness <= 100.0):
                request_img = self.create_request_image()

                self.__config_image__.Brightness = Value_Brightness
                request_img.ImagingSettings = self.__config_image__

                self.__image__.SetImagingSettings(request_img)
        except(exceptions.ONVIFError):
            self.__mycam__ = None
            self.__media__ = None

            Onvif_Manager.reset_parameters()

            print("Onvif Errore Connessione")

    def set_Saturation(self,Value_Saturation):

        try:
            if(Value_Saturation >= 0.0 and Value_Saturation <= 100.0):
                request_img = self.create_request_image()

                self.__config_image__.ColorSaturation = Value_Saturation
                request_img.ImagingSettings = self.__config_image__

                self.__image__.SetImagingSettings(request_img)
        except(exceptions.ONVIFError):
            self.__mycam__ = None
            self.__media__ = None

            Onvif_Manager.reset_parameters()

            print("Onvif Errore Connessione")

    def set_Sharpness(self,Value_Sharpness):

        try:
            if(Value_Sharpness >= 0.0 and Value_Sharpness <= 100.0):
                request_img = self.create_request_image()

                self.__config_image__.Sharpness = Value_Sharpness
                request_img.ImagingSettings = self.__config_image__

                self.__image__.SetImagingSettings(request_img)
        except(exceptions.ONVIFError):
            self.__mycam__ = None
            self.__media__ = None

            Onvif_Manager.reset_parameters()

            print("Onvif Errore Connessione")

    def set_Contrast(self,Value_Contrast):

        try:
            if(Value_Contrast >= 0.0 and Value_Contrast <= 100.0):
                request_img = self.create_request_image()

                self.__config_image__.Contrast = Value_Contrast
                request_img.ImagingSettings = self.__config_image__

                self.__image__.SetImagingSettings(request_img)
        except(exceptions.ONVIFError):
            self.__mycam__ = None
            self.__media__ = None

            Onvif_Manager.reset_parameters()

            print("Onvif Errore Connessione")

    def set_Focus_Move(self, Value_Position):

        try:
            if (Value_Position >= 0.0 and Value_Position <= 1.0):
                request_focus = self.create_request_focus()

                request_focus.Focus = {'Absolute': {'Position': Value_Position, 'Speed': None}, \
                                       'Relative': {'Distance': Value_Position, 'Speed': None}, \
                                       'Continuous': {'Speed': 0.0}}

                self.__image__.Move(request_focus)

                return True

            return False
        except(exceptions.ONVIFError):
            self.__mycam__ = None
            self.__media__ = None

            Onvif_Manager.reset_parameters()

            print("Onvif Errore Connessione")

            return False

    # ------------------ Setting Media -------------------------
    # Creazione della richiesta da inviare alla camera relativa alla modifica dei parametri dell'encoder
    def create_request_media(self):
        request_media = self.__media__.create_type('SetVideoEncoderConfiguration')
        request_media.ForcePersistence = True

        return request_media

    def get_ResolutionAvailable(self):
        return self.__option_camera__.H264.ResolutionsAvailable

    def set_Resolution(self, Index_Resolution):

        try:
            if(Index_Resolution >= 0 and Index_Resolution < len(self.get_ResolutionAvailable())):
                request_media = self.create_request_media()
                self.__config_media__.Resolution = self.__option_camera__.H264.ResolutionsAvailable[Index_Resolution]

                request_media.Configuration = self.__config_media__

                self.__media__.SetVideoEncoderConfiguration(request_media)
        except(exceptions.ONVIFError):
            self.__mycam__ = None
            self.__media__ = None

            Onvif_Manager.reset_parameters()

            print("Onvif Errore Connessione")