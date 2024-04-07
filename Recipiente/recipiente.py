from flask import Flask, request
import socket
import hashlib

import requests

def find_available_port():
    """Encontra uma porta disponível."""
    port = 5001  # Porta inicial
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            return port
        except OSError:
            port += 1
        finally:
            sock.close()



app = Flask(__name__)

def get_extension(filename):
    """Obtém a extensão do arquivo."""
    return filename.rsplit('.', 1)[-1].lower()


@app.route('/receive_file', methods=['POST'])
def receive_file():
    if 'file' in request.files and 'sha256' in request.form:
        received_file = request.files['file']
        received_sha256 = request.form['sha256']
        
        # Determina o tipo de arquivo recebido
        received_extension = get_extension(received_file.filename)
        
        # Salva o arquivo recebido com a extensão correta
        received_file.save(f'received_file.{received_extension}')
        
        # Verifica o SHA256 do arquivo recebido
        sha256_hash = hashlib.sha256()
        with open(f'received_file.{received_extension}', 'rb') as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                sha256_hash.update(data)
        
        # Verifica se os hashes SHA256 coincidem
        if sha256_hash.hexdigest() == received_sha256:
            print("SHA256 recebido:")
            print(received_sha256)
            print("SHA256 validado localmente:")
            print(sha256_hash.hexdigest())
            print("Arquivo validado!")
        else:
            print("Erro: O SHA256 do arquivo recebido não coincide")
            return "Erro: O SHA256 do arquivo recebido não coincide"
    return "Recipiente recebeu alguma coisa."

@app.route('/request_file', methods=['GET'])
def requisitar_arquivo():
    choice = int(input("Voce gostaria de copiar qual arquivo? \n 1. PDF \n 2. Imagem \n 3. docx \n"))
    if(choice == 1):
        file_path = 'big_oh_fest.pdf'
    elif(choice == 2):
        file_path = 'images.jpeg'
    elif(choice == 3):
        file_path = 'arquivo.docx'
    target_url = 'http://localhost:5000/send_file'
    
    
    with open('arquivo_requisitado.txt', 'w') as arquivo:
        arquivo.write(file_path)
    
    print("Arquivo requisitado")
    requests.post(target_url, files={'file': open('arquivo_requisitado.txt', 'rb')}) #nao consegui enviar apenas o text ent vou mandar um arquivo txt
    return "Request enviado"

if __name__ == '__main__':
    #port = find_available_port()
    #print(f"Using port: {port}")
    #app.run(host='localhost', port=port)
    app.run(host='localhost', port=5001)
