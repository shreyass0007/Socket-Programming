import socket
ip='localhost'
port=9999
def udp_file_receiver(ip, port, output_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Server listening on {ip}:{port}")
    
    with open(output_file, 'wb') as f:
        while True:
            data, addr = sock.recvfrom(65535)  # Max UDP packet size
            if data == b'__END__':  # End of file transfer signal
                break
            f.write(data)
    
    print(f"File received and saved as {output_file}")
    sock.close()

if __name__ == "__main__":
    udp_file_receiver(ip, port, "received_file")
