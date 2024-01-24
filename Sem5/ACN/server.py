import socket
import cv2
import wave

import numpy as np
from packet import CustomPacket, decrypt_data, ENCRYPTION_KEY

buffered_data = bytearray()

def server(ip, port):
    global buffered_data
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_video = cv2.VideoWriter('source_video_server.mp4', fourcc, 20.0, (640, 480))
    frames = []
    
    try:
        while True:
            data, addr = s.recvfrom(65535)
            chunk_type = data[0:1]
            actual_data = data[1:]

            if chunk_type == b'S':
                buffered_data = actual_data
            elif chunk_type == b'C':
                buffered_data += actual_data
            elif chunk_type == b'E':
                buffered_data += actual_data
                packet = CustomPacket.deserialize(buffered_data)
                buffered_data = bytearray()  # Clear the buffer for the next set of chunks

                if packet.packet_type == CustomPacket.DATA_PACKET:
                    if packet.sequence_num == 1:  # Video data
                        frame = cv2.imdecode(np.frombuffer(packet.payload, np.uint8), cv2.IMREAD_COLOR)
                        out_video.write(frame)
                    elif packet.sequence_num == 2:  # Audio data
                        frames.append(packet.payload)
                
    except KeyboardInterrupt:
        pass

    out_video.release()
    
    # Save audio
    with wave.open('source_audio_server.wav', 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

server('localhost', 12345)