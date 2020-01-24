import subprocess
import sys
import re
import time

class Device(object):
    def __init__(self, profile_dict):
        self.profile = profile_dict
        self.device = self.profile['device']['Device']
        self.TCP = self.profile['device']['TCP']
        self.Logger = self.profile['logger']
        self.serial_trans = ''
        self.connected = False
        self.start_server()
        if self.TCP:
            self.connect_tcp()
        if not self.TCP:
            self.connect_usb()
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.device == other.device and
            self.serial_trans == other.serial_trans
        )
    
    def connect_tcp(self):
        cmd = ['adb', 'connect', self.device]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        if re.search('connected to ' + self.device, response):
            self.Logger.success('Successfully connected to device [' + self.device + '] with TCP.')
            self.connected = True
            self.assign_serial()
        elif re.search('failed to connect', response):
            self.Logger.error('Unable to connect. Please check if info of device [' + self.device + '] is correct.')
            self.disconnect_tcp()
        
    def connect_usb(self):
        while True:
            try:
                cmd = ['adb', 'devices', '-l']
                response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').splitlines()
                self.sanitize_device_info(response)
                for item in response:
                    if self.device in item:
                        cmd = ['adb', '-t', self.serial_trans, 'wait-for-device']
                        self.Logger.info('Waiting for device [' + self.device + '] to be authorized...')
                        subprocess.call(cmd)
                        self.Logger.success('Device [' + self.device + '] authorized and connected.')
                        self.connected = True
                        break
                if not self.connected:
                    self.Logger.error('Waiting for device [' + self.device + '] to be connected... Interrupt keyboard to stop waiting.')
                    time.sleep(3)
                    continue
                break
            except KeyboardInterrupt:
                self.Logger.info('Stopped waiting device [' + self.device + '] to be connected.')
                break

    def assign_serial(self):
        cmd = ['adb', 'devices', '-l']
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').splitlines()
        self.sanitize_device_info(response)
        self.serial_trans = self.get_serial_trans(self.device, response)

    def exec_out(self, args):
        """Executes the command via exec-out

        Args:
            args (string): Command to execute.

        Returns:
            tuple: A tuple containing stdoutdata and stderrdata
        """
        cmd = ['adb', '-t', self.serial_trans, 'exec-out'] + args.split(' ')
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        return process.communicate()[0]

    def shell(self, args):
        """Executes the command via adb shell

        Args:
            args (string): Command to execute.
        """
        cmd = ['adb', '-t', self.serial_trans, 'shell'] + args.split(' ')
        self.Logger.debug('[' + self.device + '] ' + ' '.join(cmd))
        subprocess.call(cmd)

    def start_server(self):
        cmd = ['adb', 'start-server']
        while True:
            try:
                response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
                if response == '':
                    self.Logger.info('ADB Server is already started.')
                elif 'start' in response:
                    self.Logger.success('ADB Server started successfully.')
                else:
                    self.Logger.error('Unexpected error, trying to kill and restart server.')
                    self.kill_server()
                    continue
                break
            except FileNotFoundError:
                self.Logger.error('Please install ADB correctly and include it in PATH.')
                sys.exit()

    def kill_server(self):
        cmd = ['adb', 'kill-server']
        try:
            response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
            if response == '':
                self.Logger.success('ADB Server killed successfully.')
            elif 'refused' in response:
                self.Logger.info('Stop killing what\'s already dead!')
        except FileNotFoundError:
            self.Logger.error('Please install ADB correctly and include it in PATH.')
            sys.exit()

    def disconnect_tcp(self):
        cmd = ['adb', 'disconnect', self.device]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        if re.search('error', response):
            self.Logger.error('The device [' + self.device + '] is not actively connected.')
        elif re.search('disconnected', response):
            self.Logger.debug('Successfully disconnected device [' + self.device + '].')

    @staticmethod
    def sanitize_device_info(string_list):
        for index in range(len(string_list) - 1, -1, -1):
            if 'transport_id' not in string_list[index]:
                string_list.pop(index)

    @staticmethod
    def get_serial_trans(device, string_list):
        for index in range(len(string_list)):
            if device in string_list[index]:
                return string_list[index][string_list[index].index('transport_id:') + 13:]
