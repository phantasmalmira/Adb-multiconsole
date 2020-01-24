from tools.profiles import Profile
from tools.logger import Color
from os import listdir
from os.path import isfile, join

class AKBots():
    def __init__(self):
        self.profiles = []
        self.active = []

    def get_all_profiles(self):
        self.profiles = [f for f in listdir('./profiles') if isfile(join('./profiles', f)) and '.prof' in f]

    def print_all_profiles(self):
        self.get_all_profiles()
        for index in range(len(self.profiles)):
            print(Color.green + str(index) + '. ' + self.profiles[index] + Color.END)

    def enable_profile(self):
        self.print_all_profiles()
        target = './profiles/' + self.profiles[int(input(Color.yellow + 'Which profile to enable? > ' + Color.END))]
        self.active.append(Profile(target))