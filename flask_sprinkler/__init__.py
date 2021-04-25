import serial
import serial.threaded
import threading
import time
import logging
import re

class SprinklerPacket(serial.threaded.FramedPacket):
    START = b'!'
    STOP = b';'

    ENCODING = 'utf-8'
    UNICODE_HANDLING = 'replace'

    def __init__(self):
        super().__init__()
        self.packet_handler = None

    def connection_made(self, transport):
        super(SprinklerPacket, self).connection_made(transport)

    def handle_packet(self, packet):
            self.handle_line(packet.decode(self.ENCODING, self.UNICODE_HANDLING))

    def handle_line(self, packet):
        if self.packet_handler:
            self.packet_handler(packet)

    def write_line(self, packet):
        self.transport.write(self.START + packet.encode(self.ENCODING, self.UNICODE_HANDLING) + self.STOP)

    def handle_out_of_packet_data(self, data):
        logging.warn(f'Out of protocol data: {data}')

    def set_packet_handler(self, packet_handler):
        self.packet_handler = packet_handler

class Sprinkler:

    sprinkler_state = {}
    
    def __init__(self, app):
        self.serial_device = app.config.get('SERIAL_DEVICE','/dev/serial0')
        self.serial_baudrate = app.config.get('SERIAL_BAUDRATE', 9600)
        self.serial_databits = app.config.get('SERIAL_DATABITS', 8)
        self.serial_parity = app.config.get('SERIAL_PARITY', 'N')
        self.serial_stopbits = app.config.get('SERIAL_STOPBITS', 1)
        self.serial_timeout = app.config.get('SERIAL_TIMEOUT', 0.1)
        self.serial = serial.Serial()
        self.thread_started = False
        self.send_packet = None
        self.serial_open_lock = threading.Lock()
        
        if not self.serial.is_open:
            logging.debug(f'Opening serial port {self.serial_device}')
            self._open_serial()

        if not self.thread_started:
            self.thread = threading.Thread(target=self._thread_start, daemon=True)
            self.thread.start()

    def _thread_start(self):
        if not self.thread_started:
            self.thread_started = True
            with serial.threaded.ReaderThread(self.serial, SprinklerPacket) as protocol:
                self.send_packet = protocol.write_line
                protocol.set_packet_handler(self.handle_packet)
                while True:
                    time.sleep(0.1)

    def _open_serial(self):
        if not self.serial.is_open:
            with self.serial_open_lock:
                self.serial.baudrate = self.serial_baudrate
                self.serial.port = self.serial_device
                self.serial.timeout = self.serial_timeout
                self.serial.open()

    def write(self, data):
        if self.send_packet:
            self.send_packet(data)

    def handle_packet(self, packet):
        matches = re.match('SPRz(?P<zonenumber>\d{2})t(?P<timerval>\d{3})i(?P<queuepos>\w)|SPRq(?P<queuedepth>\w)', packet)
        if matches:
            groups = matches.groupdict()
            if groups['zonenumber'] and groups['queuepos'] is not 'X':
                logging.debug(f'{groups["zonenumber"]} is in queue position {groups["queuepos"]} with {int(groups["timerval"])} minutes left')
            if groups['queuedepth']:
                if groups['queuedepth'] is '0':
                    self.sprinkler_state['queue_depth'] = 0
                else:
                    self.sprinkler_state['queue_depth'] = ord(groups['queuedepth']) - 64
                logging.debug(f'Queue depth is {self.sprinkler_state["queue_depth"]}')

    def get_sprinkler_state(self):
        return self.sprinkler_state
    