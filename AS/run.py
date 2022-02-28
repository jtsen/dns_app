import socket
    
if __name__=='__main__':
    #listen on UDP port
    UDP_IP = "0.0.0.0"
    UDP_PORT =53533
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP,UDP_PORT))
    DNS_records={}
    while True:
        data, addr = sock.recvfrom(1024)
        data_str = data.decode("utf-8")
        data_list = data_str.split()

        if len(data_list)==2:#query has two elements
            hostname=data_list[0][1:-1] #removing left paran and comma
            query_type=data_list[1][0] #removing right paran
            #only serve Type A queries
            if query_type == 'A':
                try:#see if there is a hostname that is registered.
                    #respond to user server if the hostname is registered
                    hostname_IP=DNS_records[hostname]
                    query_response_message=f"TYPE={query_type}\nNAME={hostname}\nVALUE={hostname_IP}\nTTL=10\n"
                    message = bytes(query_response_message,"utf-8")
                    sock.sendto(message,addr)
                except KeyError:#hostname is not registered
                    query_fail_message="Record for server not found."
                    message=bytes(query_fail_message,"utf-8")
                    sock.sendto(message,addr)
        if len(data_list)==4:#registration has 4 elements, serving Type A only
            if data_list[0].split('=')[1] == 'A':
                target_ip = data_list[2].split('=')[1]
                hostname = data_list[1].split('=')[1]
                DNS_records[hostname]= target_ip
                reg_response_message = "Registration success"
                mes = bytes(reg_response_message,"utf-8")
                sock.sendto(mes,addr)
            else:
                #do nothing, type is incorrect
                reg_response_message="Only support Type A Registrations!"
                mes = bytes(reg_response_message,"utf-8")
                sock.sendto(mes,addr)
                print("Registration failed")