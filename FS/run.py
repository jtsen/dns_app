from flask import Flask, request, Response, jsonify
import socket

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
    

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Fibonacci server for DNS App (Lab 3)'

@app.route('/fibonacci')
def direct_fib_serve():
    #check that all required fields are provided
    if request.args.get('number') and request.args.get('number').isdigit() and request.args.get('number')[0]!='-' and request.args.get('number')[0]!='+' and not request.args.get('number').isalpha():
            res = fib(int(request.args.get('number')))
            return Response(
                str(res),
                status=200
            )
    else:
        return Response(
            "Bad Format or Missing argument [number=Int]",
            status = 400
        )
        

@app.route('/register', methods=['PUT'])
def fib_calc():
    #request path params:
    #hostname | fs_port | number | as_ip | as_port
    data = request.get_json()
    req_keys = ['hostname', 'ip', 'as_ip', 'as_port']
    #Make sure the JSON object has all the required keys, else 400
    if list(data.keys()) == req_keys:
        #parse the json object for the ip/port for setting up UDP connection
        udp_ip, udp_port = data['as_ip'], int(data['as_port'])
        #registration message
        reg_message = f"TYPE=A\nNAME={data['hostname']}\nVALUE={data['ip']}\nTTL=10\n"
        #Establish UDP connection and send registration message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((udp_ip,udp_port))
        sock.sendto(bytes(reg_message,"utf-8"),(udp_ip,udp_port))
        #Receive a success/fail response
        data, addr = sock.recvfrom(1024)
        data_str = data.decode("utf-8")
        if data_str == "Registration success":#success
            return Response(
            data_str,
            status=201
            )
        else:#failure
            return Response(
                data_str,
                status=400
            )
    else:#request does not have the required params
        return Response(
        "Bad Request",
        status=400
        )

app.run(host='0.0.0.0',#127.0.0.1 (?)
        port=9090,
        debug=True)
