import wave
import cv2
import pyaudio
import socket
from packet import CustomPacket, encrypt_data, ENCRYPTION_KEY

MAX_CHUNK_SIZE = 60000

def send_chunked_data(s, server_ip, server_port, packet):
    data = packet.serialize()
    chunks = [data[i:i+MAX_CHUNK_SIZE] for i in range(0, len(data), MAX_CHUNK_SIZE)]
    
    if len(chunks) == 1:
        s.sendto(b'S' + chunks[0] + b'E', (server_ip, server_port))
    else:
        s.sendto(b'S' + chunks[0], (server_ip, server_port))
        for chunk in chunks[1:-1]:
            s.sendto(b'C' + chunk, (server_ip, server_port))
        s.sendto(b'E' + chunks[-1], (server_ip, server_port))

def capture_and_send(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create the socket object here

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_video = cv2.VideoWriter('source_video_client.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    initial_packet = CustomPacket(b'client', b'server', CustomPacket.DATA_PACKET, 0, b'INIT')
    send_chunked_data(s, server_ip, server_port, initial_packet)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, video_data = cv2.imencode('.jpg', frame)
            video_packet = CustomPacket(b'client', b'server', CustomPacket.DATA_PACKET, 1, video_data.tobytes())
            send_chunked_data(s, server_ip, server_port, video_packet)
            out_video.write(frame)
            
            audio_data = stream.read(1024)
            audio_packet = CustomPacket(b'client', b'server', CustomPacket.DATA_PACKET, 2, audio_data)
            send_chunked_data(s, server_ip, server_port, audio_packet)
            frames.append(audio_data)
            
    except KeyboardInterrupt:
        pass

    cap.release()
    out_video.release()
    cv2.destroyAllWindows()
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open('source_audio_client.wav', 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

capture_and_send('localhost', 12345)