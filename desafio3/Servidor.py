import socket 
import os     
import sys   

TcpIp = '0.0.0.0'
TcpPorta = 10727 
TamanhoBuffer = 1024
DiretorioRecebidos = 'recebidos'

if not os.path.exists(DiretorioRecebidos):
    os.makedirs(DiretorioRecebidos)

def ReceberArquivo(Conexao, NomeArquivo):
    CaminhoCompleto = os.path.join(DiretorioRecebidos, NomeArquivo)
    
    TamanhoBytes = Conexao.recv(TamanhoBuffer).decode('utf-8')
    try:
        TamanhoTotal = int(TamanhoBytes.split('\n')[0].strip()) 
    except ValueError:
        print("ERRO")
        Conexao.sendall("TAMANHO_ERRO".encode('utf-8'))
        return 
        
    Conexao.sendall("TAMANHO_OK".encode('utf-8')) 
    
    try:
        BytesRecebidos = 0
        with open(CaminhoCompleto, 'wb') as ArquivoNovo:
            print(f"Recebendo arquivo: {NomeArquivo}")
            
            while BytesRecebidos < TamanhoTotal:
                BytesParaReceber = min(TamanhoBuffer, TamanhoTotal - BytesRecebidos)
                
                Peca = Conexao.recv(BytesParaReceber)
                if not Peca:
                    print("ERRO")
                    break
                    
                ArquivoNovo.write(Peca)
                BytesRecebidos += len(Peca)

        if BytesRecebidos == TamanhoTotal:
            print(f"\nArquivo '{NomeArquivo}' recebido. Salvo em: {CaminhoCompleto}")
            Conexao.sendall("ARQUIVO_SUCESSO".encode('utf-8'))
        else:
             print(f"\nArquivo incompleto")
             Conexao.sendall("ARQUIVO_INCOMPLETO".encode('utf-8'))
        
    except Exception as Erro:
        print(f"\n{Erro}")
        Conexao.sendall("ARQUIVO_ERRO".encode('utf-8'))

ServidorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServidorSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    ServidorSocket.bind((TcpIp, TcpPorta))
    ServidorSocket.listen(1)
    print(f"Servidor iniciado em {TcpIp}:{TcpPorta}. escutando")
    
    Conexao, Endereco = ServidorSocket.accept()
    print(f'Cliente conectado de: {Endereco}')

    while True:
        DadosRecebidos = Conexao.recv(TamanhoBuffer).decode('utf-8').strip()
        
        if not DadosRecebidos:
            print("Cliente desconectou.")
            break
            
        if DadosRecebidos.upper() == 'QUIT':
            print("QUIT recebido, encerrado")
            break
            
        if DadosRecebidos.startswith("FILE_TRANSFER:"):
            _, NomeArquivo = DadosRecebidos.split(':', 1)
            ReceberArquivo(Conexao, NomeArquivo.strip()) 
            
        else:
            print(f"[CLIENTE]: {DadosRecebidos}")
            
            RespostaServidor = input("[Servidor]: ")
            Conexao.send(RespostaServidor.encode('UTF-8'))
            
            if RespostaServidor.upper() == 'QUIT':
                print("QUIT enviado, fechando")
                break

except Exception as Erro:
    print(f"{Erro}")
    
finally:
    if 'Conexao' in locals():
        Conexao.close()
    ServidorSocket.close()
    print("Fim")