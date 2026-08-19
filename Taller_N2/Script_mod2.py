import argparse
import socket
import sys

def main():
    parser = argparse.ArgumentParser(description="Cliente TCP simple")
    parser.add_argument('--host', action="store", dest="host", required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    parser.add_argument('--file', action="store", dest="file", default="/", required=False)
    # NUEVO: Opción para definir el nombre del archivo de salida (por defecto: resultado.txt)
    parser.add_argument('--output', action="store", dest="output", default="resultado.txt", required=False, help="Archivo TXT donde guardar la salida")
    given_args = parser.parse_args()
    
    host = given_args.host
    port = given_args.port
    filename = given_args.file or "/"
    output_file = given_args.output

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
        msg = f"Address-related error connecting to server: {e}\n"
        print(msg, end="")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(msg)
        sys.exit(1)
    except socket.error as e:
        msg = f"Connection error: {e}\n"
        print(msg, end="")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(msg)
        sys.exit(1)

    # Tercer bloque try-except: Enviando datos
    try:
        request = f"GET {filename} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode('utf-8'))
    except socket.error as e:
        msg = f"Error sending data: {e}\n"
        print(msg, end="")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(msg)
        sys.exit(1)

    # Cuarto bloque: Recibir datos en bucle y guardar en archivo simultáneamente
    with open(output_file, "w", encoding="utf-8") as log_file:
        while True:
            try:
                buf = s.recv(2048)
            except socket.error as e:
                msg = f"Error receiving data: {e}\n"
                print(msg, end="")
                log_file.write(msg)
                sys.exit(1)

            if not buf:
                break

            decoded_text = buf.decode('utf-8', errors='replace')
            
            # 1. Muestra en pantalla
            sys.stdout.write(decoded_text)
            # 2. Guarda en el archivo de texto
            log_file.write(decoded_text)

    s.close()
    print(f"\n\n[+] Resultado guardado exitosamente en: {output_file}")

if __name__ == '__main__':
    main()
