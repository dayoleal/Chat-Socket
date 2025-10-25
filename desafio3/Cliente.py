import socket 
import os

TcpIp = '127.0.0.1' 
TcpPorta = 10727 
TamanhoBuffer = 1024

def EnviarArquivo(ClienteSocket, CaminhoArquivo):
    try:
        NomeArquivo = os.path.basename(CaminhoArquivo)
        TamanhoTotal = os.path.getsize(CaminhoArquivo)
        
        ClienteSocket.sendall(f"FILE_TRANSFER: {NomeArquivo}\n".encode('utf-8'))
        
        ClienteSocket.sendall(str(TamanhoTotal).encode('utf-8'))
        
        AckTamanho = ClienteSocket.recv(TamanhoBuffer).decode('utf-8').strip()
        if AckTamanho != "TAMANHO_OK":
             print(f"ERRO")
             return 
        
        print(f"Enviando arquivo: {NomeArquivo}")
        BytesEnviados = 0
        
        with open(CaminhoArquivo, 'rb') as ArquivoParaEnviar:
            while True:
                Pedaco = ArquivoParaEnviar.read(TamanhoBuffer)
                if not Pedaco:
                    break
                
                ClienteSocket.sendall(Pedaco)
                BytesEnviados += len(Pedaco)
                
        StatusFinal = ClienteSocket.recv(TamanhoBuffer).decode('utf-8').strip()
        
        if StatusFinal == "ARQUIVO_SUCESSO":
            print(f"\nSUCESSO.")
        else:
            print(f"\nFALHOU")

    except FileNotFoundError:
        print(f"ERRO")
    except Exception as Erro:
        print(f"{Erro}")

ClienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ClienteSocket.connect((TcpIp, TcpPorta))
    print(f"Conectado ao servidor em {TcpIp}:{TcpPorta}.")
    
    while True:
        print("\n--- MENU DE OPÇÕES ---")
        print("1. Enviar Mensagem de Chat")
        print("2. Enviar Arquivo")
        print("3. Sair (QUIT)")
        
        Escolha = input("Escolha o número (1, 2, 3): ").strip()
        
        if Escolha == '3':
            ClienteSocket.sendall('QUIT'.encode('utf-8'))
            print("QUIT enviado, encerrou")
            break
            
        elif Escolha == '2':
            CaminhoArquivo = input("Digite o caminho COMPLETO do arquivo: ").strip()
            if os.path.exists(CaminhoArquivo) and os.path.isfile(CaminhoArquivo):
                EnviarArquivo(ClienteSocket, CaminhoArquivo)
            else:
                print("Verifique se o arquivo existe.")

        elif Escolha == '1':
            MensagemCliente = input("[Cliente]: ")
            
            ClienteSocket.sendall(MensagemCliente.encode('UTF-8'))
            
            if MensagemCliente.upper() == 'QUIT':
                print("QUIT enviado, encerrou")
                break

            DadosServidor = ClienteSocket.recv(TamanhoBuffer)
            if not DadosServidor:
                print("Servidor desconectou.")
                break
                
            MensagemRecebida = DadosServidor.decode('UTF-8').strip()
            print(f"[Servidor]: {MensagemRecebida}")
            
            if MensagemRecebida.upper() == 'QUIT':
                print("QUIT recebido, encerrou")
                break
                
        else:
            print("Opção inválida")

except socket.error as Erro:
    print(f"{Erro}")
    
finally:
    ClienteSocket.close()
    print("Fim")