import socket
import sys

TCP_IP = '0.0.0.0' 
TCP_PORTA = 10727  
TAMANHO_BUFFER = 1024

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    servidor.bind((TCP_IP, TCP_PORTA))
except socket.error as msg:
    print('Bind falhou. Erro:', str(msg))
    sys.exit()

servidor.listen(1)
print(f"Servidor CHAT TCP rodando em {TCP_IP}:{TCP_PORTA} e escutando")

conn, addr = servidor.accept()
print(f'Conexão com: {addr}')

try:
    while True:
        dados_cliente = conn.recv(TAMANHO_BUFFER)
        if not dados_cliente:
            break
        
        mensagem_recebida = dados_cliente.decode('UTF-8').strip()
        print(f"[CLIENTE]: {mensagem_recebida}")

        if mensagem_recebida.upper() == 'QUIT':
            print("Comando QUIT. Encerrando")
            break

        mensagem_servidor = input("[Servidor (Eu)]: ")
        conn.send(mensagem_servidor.encode('UTF-8'))
        
        if mensagem_servidor.upper() == 'QUIT':
            print("QUIT enviado. Encerrando")
            break

finally:
    conn.close()
    servidor.close()
    print("Conexão e Servidor encerrados")