import socket
import time
import sys
server_ip='localhost'
server_port=9999
file_path=r"C:\Users\shrey\Downloads\Socket\script.txt"  # Added 'r' prefix
# alternatively: file_path="C:\\Users\\shrey\\Downloads\\Socket\\script.txt"

def udp_file_sender(server_ip, server_port, file_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buffer_size = 65507  # Max UDP payload size
    
    with open(file_path, 'rb') as f:
        while True:
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                break
            sock.sendto(bytes_read, (server_ip, server_port))
            time.sleep(0.01)  # Small delay to avoid packet loss
    
    # Send end of file signal
    sock.sendto(b'__END__', (server_ip, server_port))
    
    print("File sent successfully.")
    sock.close()

if __name__ == "__main__":
    # Use default values if no command line arguments are provided
    if len(sys.argv) == 1:
        udp_file_sender(server_ip, server_port, file_path)
    elif len(sys.argv) == 4:
        send_ip = sys.argv[1]
        send_port = int(sys.argv[2])
        send_file = sys.argv[3]
        udp_file_sender(send_ip, send_port, send_file)
    else:
        print("Usage: python udp_file_sender.py <server_ip> <server_port> <file_path>")
        print("Or run without arguments to use default values")
        sys.exit(1)
