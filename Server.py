import socket
import select

def iniciar_servidor(host='127.0.0.1', puerto=12345, max_clientes=100):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen(max_clientes)
    print(f"Servidor iniciado en {host}:{puerto}")

    sockets_lista = [servidor_socket]
    conexiones_activas = 0

    while True:
        read_sockets, _, _ = select.select(sockets_lista, [], [])

        for sock in read_sockets:
            if sock == servidor_socket:
                cliente_socket, cliente_direccion = servidor_socket.accept()
                conexiones_activas += 1
                print(f"Conexión aceptada de {cliente_direccion} | Conexiones activas: {conexiones_activas}")
                sockets_lista.append(cliente_socket)
            else:
                try:
                    datos = sock.recv(1024)
                    if datos:
                        sock.send(datos)
                    else:
                        conexiones_activas -= 1
                        print(f"Cliente desconectado {sock.getpeername()} | Conexiones activas: {conexiones_activas}")
                        sockets_lista.remove(sock)
                        sock.close()
                except:
                    conexiones_activas -= 1
                    print(f"Error con el cliente {sock.getpeername()} | Conexiones activas: {conexiones_activas}")
                    sockets_lista.remove(sock)
                    sock.close()

if __name__ == "__main__":
    iniciar_servidor()
