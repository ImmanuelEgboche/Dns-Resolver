"""

[ Your Computer ]        [ Google's DNS Server ]
           |                         |
      Create Socket                   |
           |                         |
      Send Message ------------------>|
           |                         |
      Receive Response <--------------|
           |                         |
   Check ID in Response               |
           |                         |


"""

import socket
import struct

def parse_dns_response(response):
    dns_header = response[:12]
    id, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', dns_header)
    
    qr = (flags & 0x8000) >> 15
    if qr != 1:
        print("Not a DNS response.")
        return

    question_section = response[12:]
    question, question_section = decode_domain_name(question_section)
    qtype, qclass = struct.unpack('!HH', question_section[:4])

    print("Parsed Question Section:")
    print("  Question:", question)
    print("  Type:", qtype)
    print("  Class:", qclass)

    answer_section = response[12 + len(question_section):]

    if qtype == 1:  # A record
        ip_address = socket.inet_ntoa(answer_section[10:14])
        print("Resolved IP Address:", ip_address)
    elif qtype == 2:  # NS record
        authoritative_name_servers = []
        for _ in range(nscount):
            ns, answer_section = decode_domain_name(answer_section)
            authoritative_name_servers.append(ns)
        print("Authoritative Name Servers:", authoritative_name_servers)
        
        # Check the additional section for IP addresses
        additional_section = response[12 + len(question_section) + len(answer_section):]
        for _ in range(arcount):
            _, additional_section = decode_domain_name(additional_section)  # Skip the name
            atype, aclass, ttl, rdlength = struct.unpack('!HHIH', additional_section[:10])
            
            if atype == 1:  # A record
                ip_address = socket.inet_ntoa(additional_section[10:14])
                print("Resolved IP Address:", ip_address)
                return

def send_dns_query(query_domain, server_address):
    dns_id = b'\x00\x16'
    dns_flags = b'\x00\x00'  # Recursion bit set to zero
    dns_counts = b'\x00\x01\x00\x00\x00\x00\x00\x00'

    dns_question = encode_domain_name(query_domain)
    dns_query_type = b'\x00\x01'
    dns_query_class = b'\x00\x01'

    dns_query_message = dns_id + dns_flags + dns_counts + dns_question + dns_query_type + dns_query_class

    dns_query_message_hex = dns_query_message.hex().upper()
    print("DNS query message:", dns_query_message_hex)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(dns_query_message, server_address)
        response, _ = sock.recvfrom(4096)

        if response[:2] == dns_id:
            print(f"Querying {server_address} for {query_domain}")
            parse_dns_response(response)
        else:
            print("Response ID does not match the sent ID.")

def decode_domain_name(data):
    labels = []
    while True:
        length = data[0]
        data = data[1:]
        if length == 0:
            break
        labels.append(data[:length].decode('utf-8'))
        data = data[length:]
    return '.'.join(labels), data

def encode_domain_name(domain):
    labels = domain.split('.')
    encoded_domain = b''
    for label in labels:
        encoded_domain += bytes([len(label)]) + label.encode('utf-8')
    encoded_domain += b'\x00'  # Null byte to terminate the domain name
    return encoded_domain

def resolve_with_root_name_server(query_domain):
    root_name_server = ('198.41.0.4', 53)
    
    # Start by querying the root name server
    send_dns_query(query_domain, root_name_server)

# Example usage
resolve_with_root_name_server('dns.google.com')

