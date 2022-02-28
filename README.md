# dns_app
Authoritative server + Fibonacci Server + User Server

Three docker containers (servers) communicating with one another with UDP and HTTP requests to form a Fibonacci Application Network.

## Set-up
0. Set-up docker network
   1. `docker network create NETWORK-NAME`
1. Set-up Authoritative server 
   1. `docker build -t USERNAME/as-server:latest .`
   2. `docker run --network NETWORK-NAME --name as-server -p 53533:53533/udp -it USERNAME/as-server:latest`
2. Set-up Fibonacci server
   1. `docker build -t USERNAME/fs-server:latest .`
   2. `docker run --network NETWORK-NAME --name fs-server -p 9090:9090 -it USERNAME/fs-server:latest`
3. Set-up User server
   1. `docker build -t USERNAME/us-server:latest .`
   2. `docker run --network NETWORK-NAME --name us-server -p 8080:8080 -it USERNAME/us-server:latest`

## Sample requests
- GET `http://localhost:8080/fibonacci?hostname=HOSTNAME&fs_port=9090&number=X&as_ip=AS_IP&as_port=53533`
- PUT `http://localhost:9090/register`
  - Body:
    - {
    "hostname":"fibo.com",
    "ip":"FS_IP",
    "as_ip":"AS_IP",
    "as_port":"53533"
    }
