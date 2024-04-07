from flask import Flask, request
import requests
import hashlib
import os
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

def send_file_with_name(file_path, target_url):
    """Envia o arquivo e seu nome (sem a extensão) para o URL de destino."""
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    files = {'file': open(file_path, 'rb')}
    data = {'file_name': file_name}
    response = requests.post(target_url, files=files, data=data)
    return response.text

app = Flask(__name__)

@app.route('/send_file', methods=['POST'])
def enviar_arquivo():
    if 'file' in request.files:
        # Baixa o arquivo enviado
        file_content = request.files['file'].read().decode('utf-8')
        
        # Aqui você pode manipular a string conforme necessário
        
        target_url = 'http://localhost:5001/receive_file'  # URL da rota no Programa 2
        
        resposta = send_file_with_name(file_content, target_url)
        if resposta == "Recipiente recebeu alguma coisa.":
            print(resposta)
            print("Arquivo enviado.")
            return "Arquivo enviado."
        else:
            print("Erro ao enviar o arquivo.")
            return "Erro ao enviar o arquivo."
    else:
        print("Arquivo não foi enviado")
        return "Arquivo não foi enviado"
    
@app.route('/receive_sha256', methods=['POST'])
def receive_sha256():
    if 'file_name' in request.form and 'sha256' in request.form:
        received_file_name = request.form['file_name']
        received_sha256 = request.form['sha256']
        print("Sha256 e nome do arquivo recebidos!")
        
        # Localiza o arquivo no diretório local
        file_path = os.path.join(os.getcwd(), received_file_name)
        
        # Calcula o SHA256 do arquivo local
        local_sha256 = calculate_sha256(file_path)
        
        # Verifica se os hashes SHA256 coincidem
        if local_sha256 == received_sha256:
            print("SHA256 recebido:", received_sha256)
            print("SHA256 calculado localmente:", local_sha256)
            print("Arquivo validado!")
            return "Arquivo validado!"
        else:
            print("Erro: O SHA256 do arquivo recebido não coincide")
            return "Erro: O SHA256 do arquivo recebido não coincide"
    else:
        return "Erro: Informações incompletas recebidas."
    

if __name__ == "__main__":
    app.run(host='localhost', port=5000)