from flask import Flask, request
import requests
import hashlib

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

def send_file_with_sha256(file_path, target_url):
    """Envia um arquivo e seu hash SHA256 para o URL de destino."""
    sha256_hash = calculate_sha256(file_path)
    files = {'file': open(file_path, 'rb')}
    data = {'sha256': sha256_hash}
    response = requests.post(target_url, files=files, data=data)
    return response.text

app = Flask(__name__)
@app.route('/send_file', methods=['POST'])
def enviar_arquivo():
    if 'file' in request.files:
        # Baixa o arquivo TXT enviado
        file_content = request.files['file'].read().decode('utf-8')
        
        # Usar o conteúdo do arquivo como uma string
        # aqui você pode fazer o que precisar com essa string
        print("Conteúdo do arquivo:")
        print(file_content)
        
        # Aqui você pode manipular a string conforme necessário
        
        target_url = 'http://localhost:5001/receive_file'  # URL da rota no Programa 2
        
        resposta = send_file_with_sha256(file_content, target_url)
        if resposta == "Recipiente recebeu alguma coisa.":
            return "Arquivo enviado."
    else:
        print("Arquivo não foi enviado")
        return "Arquivo não foi enviado"

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
