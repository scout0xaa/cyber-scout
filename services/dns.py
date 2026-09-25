import socket

def get_dns_info(domain):
    domain = domain.rstrip('/')
    ascii_domain = domain.encode("idna").decode("ascii")

    ip = socket.gethostbyname(ascii_domain)

    return ip 
