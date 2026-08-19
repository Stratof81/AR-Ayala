import argparse
import socket
import sys


def main():
    parser = argparse.ArgumentParser(description="Cliente TCP simple")
    parser.add_argument('--host', action="store", dest="host", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    parser.add_argument('--file', action="store", dest="file", required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    # Primer bloque try-except -- crear el socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print "Error creating socket: %s" % e
        sys.exit(1)

    # Segundo bloque try-except -- conectar al host/puerto dado
    try:
        s.connect((host, port))
    except socket.gaierror, e:
        print "Address-related error connecting to server: %s" % e
        sys.exit(1)
    except socket.error, e:
        print "Connection error: %s" % e
        sys.exit(1)

    # Tercer bloque try-except -- enviando datos
    try:
        s.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
    except socket.error, e:
        print "Error sending data: %s" % e
        sys.exit(1)

    while 1:
        # Cuarto bloque try-except -- esperando recibir datos del host remoto
        try:
            buf = s.recv(2048)
        except socket.error, e:
            print "Error receiving data: %s" % e
            sys.exit(1)

        if not len(buf):
            break

        # escribir los datos recibidos
        sys.stdout.write(buf)

    s.close()


if __name__ == '__main__':
    main()
