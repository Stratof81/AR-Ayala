import argparse
import socket
import sys

def main():
    parser = argparse.ArgumentParser(description="Cliente TCP simple")
    parser.add_argument('--host', action="store", dest="host", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    parser.add_argument('--file', action="store", dest="file", default="/", required=False)
    given_args = parser.parse_args()
    
    host = given_args.host
    port = given_args.port
    filename = given_args.file or "/"

    # Primer bloque try-except: Crear el socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error creating socket: %s" % e)
        sys.exit(1)

    # Segundo bloque try-except: Conectar al host/puerto
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Connection error: %s" % e)
        sys.exit(1)

    # Tercer bloque try-except: Enviando datos
    try:
        # Construcción de la petición HTTP agregando la cabecera Host
        request = f"GET {filename} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode('utf-8'))
    except socket.error as e:
        print("Error sending data: %s" % e)
        sys.exit(1)

    # Cuarto bloque: Recibir datos en bucle
    while True:
        try:
            buf = s.recv(2048)
        except socket.error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        if not buf:
            break

        # Escribir los datos recibidos en la consola
        sys.stdout.write(buf.decode('utf-8', errors='replace'))

    s.close()

if __name__ == '__main__':
    main()
