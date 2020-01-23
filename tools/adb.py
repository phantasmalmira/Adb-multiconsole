import subprocess
import sys
import re

class Device(object):
    def __init__(self, device=None, TCP=True):
        self.device = device
        self.serial_trans = ''
        self.connected = False
        self.TCP = TCP
        self.start_server()
        if self.TCP:
            self.connect_tcp()
        self.assign_serial()
        if not self.TCP:
            self.connect_usb()
    
    def connect_tcp(self):
        cmd = ['adb', 'connect', self.device]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        if re.search('connected to ' + self.device, response):
            print('Successfully connected to device with TCP')
            self.connected = True
        elif re.search('failed to connect', response):
            print('Please check device adb debug status')
            self.disconnect_tcp(self.device)
        
    def connect_usb(self):
        cmd = ['adb', '-t', self.serial_trans, 'wait-for-device']
        print('waiting for device to be authorized')
        subprocess.call(cmd)
        print('device authorized')
        self.connected = True

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
        #Logger.log_debug(str(cmd))
        subprocess.call(cmd)

    @classmethod
    def start_server(cls):
        cmd = ['adb', 'start-server']
        while True:
            try:
                response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
                if response == '':
                    print('Service already started')
                elif 'start' in response:
                    print('Started successfully')
                else:
                    print('Unexpected error, trying to kill and restart server')
                    cls.kill_server()
                    continue
                break
            except FileNotFoundError:
                print('Please install ADB correctly and include it in PATH')
                sys.exit()

    @staticmethod
    def kill_server():
        cmd = ['adb', 'kill-server']
        try:
            response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
            if response == '':
                print('Server killed successfully')
            elif 'refused' in response:
                print('Stop killing what\'s already dead!')
        except FileNotFoundError:
            print('Please install ADB correctly and include it in PATH')
            sys.exit()

    @staticmethod
    def disconnect_tcp(device):
        cmd = ['adb', 'disconnect', device]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        if re.search('error', response):
            print('The device ' + device + ' is not actively connected.')
        elif re.search('disconnected', response):
            print('Successfully disconnected device ' + device)

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
