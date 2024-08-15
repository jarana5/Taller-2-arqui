import threading
import socket
import time

def iniciar_cliente(host='127.0.0.1', puerto=12345, mensaje="Hola desde cliente"):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, puerto))
        cliente_socket.send(mensaje.encode('utf-8'))
        respuesta = cliente_socket.recv(1024)
       
    except Exception as e:
        print(f"Error al conectar: {e}")
    finally:
        cliente_socket.close()

def probar_concurrencia(n_concurrente):
    threads = []
    for _ in range(n_concurrente):
        thread = threading.Thread(target=iniciar_cliente)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    max_clientes = 0
    try:
        while True:
            max_clientes += 100
            print(f"Probando con {max_clientes} clientes concurrentes...")
            probar_concurrencia(max_clientes)
            time.sleep(1)  # Esperar un segundo antes de la próxima ronda
    except KeyboardInterrupt:
        print(f"Prueba detenida. Máximo de clientes concurrentes probados: {max_clientes}")
        exit()
