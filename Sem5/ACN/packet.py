import socket
import time
import cv2
import wave
import numpy as np
import struct
from cryptography.fernet import Fernet
print("Calling this")
# CustomPacket class and encryption functions
class CustomPacket:
    HEADER_FORMAT = '4s4sdBII'
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    
    DATA_PACKET = 0
    ACK_PACKET = 1

    def __init__(self, src_addr, dest_addr, packet_type, sequence_num, payload):
        self.src_addr = src_addr
        self.dest_addr = dest_addr
        self.timestamp = time.time()
        self.packet_type = packet_type
        self.sequence_num = sequence_num
        self.payload = payload
    
    def serialize(self):
        encrypted_payload = encrypt_data(ENCRYPTION_KEY, self.payload)
        header = struct.pack(self.HEADER_FORMAT, self.src_addr, self.dest_addr, self.timestamp, 
                             self.packet_type, self.sequence_num, len(encrypted_payload))
        return header + encrypted_payload
    
    @classmethod
    def deserialize(cls, data):
        header = data[:cls.HEADER_SIZE]
        src_addr, dest_addr, timestamp, packet_type, sequence_num, payload_length = struct.unpack(cls.HEADER_FORMAT, header)
        encrypted_payload = data[cls.HEADER_SIZE:cls.HEADER_SIZE+payload_length]
        payload = decrypt_data(ENCRYPTION_KEY, encrypted_payload)
        packet = cls(src_addr, dest_addr, packet_type, sequence_num, payload)
        packet.timestamp = timestamp
        return packet

def generate_key():
    return Fernet.generate_key()

def encrypt_data(key, data):
    cipher = Fernet(key)
    return cipher.encrypt(data)

def decrypt_data(key, encrypted_data):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data)

ENCRYPTION_KEY = b'j75-9sQsRA_ETGoR_cBxz2xXUQzbLBoLCkXpy3VQwyw='
