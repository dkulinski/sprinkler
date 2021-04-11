import serial
import serial.threaded
import threading
import time
import logging

class SprinklerPacket(serial.threaded.LineReader):
    TERMINATOR = b';'

    def connection_made(self, transport):
        super(SprinklerPacket, self).connection_made(transport)
        logging.info(f'Connected to {transport}')

    def handle_line(self, packet):
        logging.info(f'Captured packet {packet}')

class Sprinkler:
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
            logging.info(f'Opening serial port {self.serial_device}')
            self._open_serial()

        if not self.thread_started:
            logging.info(f'Starting thread')
            self.thread = threading.Thread(target=self._thread_start, daemon=True)
            self.thread.start()

    def _thread_start(self):
        logging.info(f'Starting infinite loop.')
        if not self.thread_started:
            logging.info(f'Starting thread')
            self.thread_started = True
            with serial.threaded.ReaderThread(self.serial, SprinklerPacket) as protocol:
                self.send_packet = protocol.write_line
                while True:
                    time.sleep(0.1)

    def _open_serial(self):
        if not self.serial.is_open:
            with self.serial_open_lock:
                self.serial.baudrate = self.serial_baudrate
                self.serial.port = self.serial_device
                self.serial.timeout = self.serial_timeout
                self.serial.open()

    def _on_packet(self, packet):
        logging.info(packet)

    def set_on_packet(self, packet_handler):
        self._on_packet = packet_handler

    def on_packet(self, packet_function):
        def wrapper():
            self._on_packet = packet_function
        return wrapper

    def write(self, data):
        if self.send_packet:
            self.send_packet(data)


        
