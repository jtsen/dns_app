from flask import Flask, request, Response
import socket, requests
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'User server for DNS App (Lab 3)'

@app.route('/fibonacci')
def get_fib():
    #request path params:
    #hostname | fs_port | number | as_ip | as_port
    hostname, fs_port = request.args.get('hostname'), request.args.get('fs_port')
    number = request.args.get('number')
    as_ip, as_port = request.args.get('as_ip'), request.args.get('as_port')
    if hostname and fs_port and number and  as_ip and  as_port:
        #parse the json object for the ip/port for setting up UDP connection
        udp_ip, udp_port = as_ip, int(as_port)
        print(udp_port)
        #DNS query message
        reg_message = f"({hostname}, A)"
        #Establish UDP connection and send registration message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((udp_ip,udp_port))
        sock.sendto(bytes(reg_message,"utf-8"),(udp_ip,udp_port))
        #receive response
        data, addr = sock.recvfrom(1024)
        data_str = data.decode("utf-8")
        sock.close()
        #respond according to response message
        if data_str == "Record for server not found.":
            return Response(
                "Record for server not found.",
                status=400
            )
        else:#found the hostname
            data_list = data_str.split()
            #ip of hostname to return
            fs_ip=data_list[2].split('=')[1]
            #querying FS server for fibonacci answer
            url = "http://"+fs_ip+":9090/fibonacci?number="+number
            res_json = requests.get(url=url)
            res = res_json.json()
            
            return Response(
                str(res)+'\n'+fs_ip,
                status=200
            )
    else:
        return Response(
        "Bad Request",
        status=400
        )

app.run(host='0.0.0.0',#127.0.0.1 (?)
        port=8080,
        debug=True)
