digraph G {
    rankdir=LR;

    // Defining nodes
    socket [shape=box];
    time [shape=box];
    cv2 [shape=box];
    wave [shape=box];
    numpy [shape=box];
    struct [shape=box];
    cryptography [shape=box, label="cryptography\n(Fernet)"];
    CustomPacket [shape=record, label="{CustomPacket | {+serialize() | +deserialize()}}"];
    encrypt_data [shape=box];
    decrypt_data [shape=box];
    generate_key [shape=box];
    server [shape=box];
    capture_and_send [shape=box];
    pyaudio [shape=box];

    // Defining relationships
    server -> socket;
    server -> cv2;
    server -> numpy;
    server -> CustomPacket;
    server -> decrypt_data;
    
    capture_and_send -> socket;
    capture_and_send -> cv2;
    capture_and_send -> pyaudio;
    capture_and_send -> CustomPacket;
    capture_and_send -> encrypt_data;
    
    CustomPacket -> time;
    CustomPacket -> struct;
    CustomPacket -> encrypt_data;
    CustomPacket -> decrypt_data;

    encrypt_data -> cryptography;
    decrypt_data -> cryptography;
    generate_key -> cryptography;
    
    // Print statement
    print [shape=box, label="print()"];
    print -> server;
    print -> capture_and_send;
}

