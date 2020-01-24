import configparser
import os
from tools.logger import Logger
from tools.adb import Device

class Profile(object):
    def __init__(self, profile_dir=None):
        self.profile_dir = profile_dir
        self.config = configparser.ConfigParser()
        self.logger = Logger()
        self.name = ''
        self.device = {'Device': 'SERIAL|IP:PORT', 'TCP': True}
        self.advanced = {'Debugging': False}
        if self.profile_dir is None:
            self.init_new()
            self.modify_profile()
        else:
            self.read_profile()
        self.adb = Device(self.__dict__)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.name == other.name and
            self.profile_dir == other.profile_dir
        )
    
    def read_profile(self):
        self.config.read(self.profile_dir)
        if not self.malformed():
            self.update_local()
        else:
            Logger.log_error('Profile is malformed. Please check the file or create a new profile.')

    def update_local(self):
        self.__read_device()
        self.__read_advanced()
        self.profile_dir = './profiles/{}.prof'.format(self.name)

    def __read_device(self):
        self.name = self.config.get('Profile', 'Name')
        self.device['Device'] = self.config.get('Device', 'Device')
        self.device['TCP'] = self.config.getboolean('Device', 'TCP')

    def __read_advanced(self):
        self.advanced['Debugging'] = self.config.getboolean('Advanced', 'Debugging')
        if self.advanced['Debugging']:
            self.logger.enable_debugging()
        else:
            self.logger.disable_debugging()

    def malformed(self):
        return not (
            self.config.has_option('Profile', 'Name') and
            self.config.has_option('Device', 'Device') and
            self.config.has_option('Device', 'TCP') and
            self.config.has_option('Advanced', 'Debugging')
        )

    def init_new(self):
        default_profile = {
            'Profile': {'Name': self.name},
            'Device': self.device,
            'Advanced': self.advanced
        }
        self.config.read_dict(default_profile)

    def save_profile(self):
        os.makedirs(os.path.dirname(self.profile_dir), exist_ok=True)
        with open(self.profile_dir, 'w') as config_file:
            self.config.write(config_file)

    def modify_profile(self):
        self.config.set('Profile', 'Name', input('Enter profile name: '))
        self.config.set('Device', 'Device', input('Enter device: '))
        self.config.set('Device', 'TCP', input('Enter TCP: '))
        self.config.set('Advanced', 'Debugging', input('Enter debugging: '))
        self.update_local()
        