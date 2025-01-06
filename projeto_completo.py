import os
import queue
import threading
import pandas as pd
from flask import Flask, request, send_file
from pdfminer.high_level import extract_text
import re

app = Flask(__name__)

# Fila para processar arquivos
fila = queue.Queue()

# Dicionário para armazenar os dados dos processos por arquivo
dados_processos = {}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Envio e Download de Planilhas</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .header {
                position: absolute;
                top: 10px;
                left: 10px;
                font-size: 48px; /* Ajustei o tamanho para ser um pouco menor */
                font-weight: bold;
                color: #000;
            }
            .header .orange-dot {
                color: #FF4500; /* Cor laranja */
            }
            .button {
                background-color: #FF4500; /* Cor laranja */
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 10px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .button:hover {
                background-color: #e03e00; /* Tom mais escuro ao passar o mouse */
            }
            h1 {
                text-align: center;
            }
            form {
                text-align: center;
            }
            .custom-file-input {
                background-color: #FF4500; /* Cor laranja */
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 10px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .custom-file-input:hover {
                background-color: #e03e00;
            }
        </style>
    </head>
    <body>
        <div class="header">
            f<span class="orange-dot">i</span>nch
        </div>
        <h1>Envio de Arquivos</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label class="custom-file-input">
                Escolher Arquivos
                <input type="file" name="files" multiple style="display: none;">
            </label>
            <button type="submit" class="button">Enviar Arquivos</button>
        </form>
        <h1>Baixar Planilha de Dados</h1>
        <form action="/download_planilha" method="get">
            <button type="submit" class="button">Baixar Planilha</button>
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist("files")
    for file in files:
        file_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)
        fila.put(file_path)  # Coloca o arquivo na fila para processamento
    return "Arquivos enviados para a fila com sucesso!"

def extrair_informacoes_pdf(file_path):
    try:
        texto = extract_text(file_path)
        print(f"Texto extraído do arquivo {file_path}:\n{texto}")

        nome_autor = re.search(r'Nome do Autor:\s*(.*)', texto)
        doc_autor = re.search(r'Documento do Autor:\s*(.*)', texto)
        nomes_reus = re.search(r'Nome\(s\) do\(s\) Réu\(s\):\s*(.*)', texto)
        docs_reus = re.search(r'Documento\(s\) do\(s\) Réu\(s\):\s*(.*)', texto)

        return {
            'Nome do Autor': nome_autor.group(1) if nome_autor else "Desconhecido",
            'Documento do Autor': doc_autor.group(1) if doc_autor else "Desconhecido",
            'Nome(s) do(s) Réu(s)': nomes_reus.group(1) if nomes_reus else "Desconhecido",
            'Documento(s) do(s) Réu(s)': docs_reus.group(1) if docs_reus else "Desconhecido"
        }
    except Exception as e:
        print(f"Erro ao extrair informações do PDF {file_path}: {e}")
        return None

def processar_arquivos():
    global dados_processos
    while True:
        file_path = fila.get()
        try:
            print(f"Processando arquivo: {file_path}")
            informacoes = extrair_informacoes_pdf(file_path)
            if informacoes:
                # Armazenar as informações usando o nome do arquivo como chave
                nome_arquivo = os.path.splitext(os.path.basename(file_path))[0]
                dados_processos[nome_arquivo] = informacoes
        except Exception as e:
            print(f"Erro ao processar o arquivo {file_path}: {e}")
        finally:
            fila.task_done()
        # Salvar os dados em uma planilha quando a fila estiver vazia
        if fila.empty():
            salvar_planilha()
            dados_processos.clear()  # Limpar os dados para evitar duplicações

def salvar_planilha():
    global dados_processos
    if dados_processos:
        excel_path = os.path.expanduser("~/Downloads/dados_processos.xlsx")
        with pd.ExcelWriter(excel_path) as writer:
            for nome_processo, dados in dados_processos.items():
                df = pd.DataFrame([dados])
                df.to_excel(writer, sheet_name=nome_processo[:31], index=False)
        print(f"Planilha salva com sucesso em: {excel_path}")

threading.Thread(target=processar_arquivos, daemon=True).start()

@app.route('/download_planilha', methods=['GET'])
def download_planilha():
    excel_path = os.path.expanduser("~/Downloads/dados_processos.xlsx")
    if os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True)
    else:
        return "Nenhuma planilha foi gerada ainda."

if __name__ == '__main__':
    app.run(debug=True)
