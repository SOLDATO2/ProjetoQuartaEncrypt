from flask import Flask, request
import socket
import hashlib
import os
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

def calculate_sha256(file_path):
    """Calcula o hash SHA256 de um arquivo."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file: #le o binario do arquivo
        while True:
            data = file.read(65536)  #le 64kb do arquivo por loop
            if not data: #se tiver lido tudo, ele termina
                break
            sha256.update(data)
    return sha256.hexdigest()

def get_extension(filename):
    """Obtém a extensão do arquivo."""
    return filename.rsplit('.', 1)[-1].lower()


@app.route('/receive_file', methods=['POST'])
def receive_file():
    if 'file' in request.files and 'file_name' in request.form:
        received_file = request.files['file']
        received_file_name = request.form['file_name']
        
        # Determina a extensão do arquivo recebido
        received_extension = received_file.filename.rsplit('.', 1)[-1].lower()
        
        # Salva o arquivo recebido com a mesma extensão que foi enviada
        received_file.save(f'{received_file_name}.{received_extension}')
        
        # Aqui você pode processar o arquivo e o nome recebidos conforme necessário
        print("Nome do arquivo recebido:")
        print(received_file_name)
        print("Arquivo recebido salvo com sucesso!")
        
        
        # Calcula o SHA256 do arquivo recebido
        sha256_hash = calculate_sha256(f'{received_file_name}.{received_extension}')
        
        # Envia o nome do arquivo e o SHA256 para UniLee
        target_url = 'http://localhost:5000/receive_sha256'
        data = {'file_name': received_file_name+'.'+received_extension, 'sha256': sha256_hash}
        print("Sha256 Calculado, enviado para UniLee...")
        response = requests.post(target_url, data=data)
        if response.text == "Arquivo validado!":
            print("Arquivo validado com sucesso!")
            return response.text
        else:
            print("Arquivo NÃO foi validado com sucesso, apagando...")
            os.remove(f'{received_file_name}.{received_extension}')
            return("Arquivo NÃO foi validado com sucesso, apagando...")
        
        
        
        
        
    else:
        return "Erro ao receber o arquivo."


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
