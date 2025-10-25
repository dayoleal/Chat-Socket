import socket
import sys

TCP_IP = '127.0.0.1' 
TCP_PORTA = 10727 
TAMANHO_BUFFER = 1024

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((TCP_IP, TCP_PORTA))
    print(f"Conectado ao servidor em {TCP_IP}:{TCP_PORTA}. Digite 'QUIT' para sair.")

    while True:
        mensagem_cliente = input("[Cliente (Eu)]: ")
        cliente.send(mensagem_cliente.encode('UTF-8'))
        
        if mensagem_cliente.upper() == 'QUIT':
            print("QUIT enviado. Encerrando")
            break

        dados_servidor = cliente.recv(TAMANHO_BUFFER)
        if not dados_servidor:
            break

        mensagem_recebida = dados_servidor.decode('UTF-8').strip()
        print(f"[Servidor]: {mensagem_recebida}")
        
        if mensagem_recebida.upper() == 'QUIT':
            print("QUIT recebido do servidor. Encerrando")
            break

except socket.error as e:
    print(f"Erro de conexão: {e}")
finally:
    # Fecha o socket
    cliente.close()
    print("Conexão do Cliente encerrada.")