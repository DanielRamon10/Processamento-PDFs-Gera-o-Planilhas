import os
from fpdf import FPDF

# Classe personalizada para criar o PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Processo Jurídico", border=0, ln=1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

# Dados fictícios para os PDFs
dados_processos = [
    {
        "Nome do Autor": "Carolina Lima",
        "Documento do Autor": "459.000.333-00",
        "Nome(s) do(s) Réu(s)": "Miguel Ferreira, Miranda Cruz",
        "Documento(s) do(s) Réu(s)": "568.351.333-00, 224.151.655-00"
    },
    {
        "Nome do Autor": "João Alves",
        "Documento do Autor": "789.123.456-78",
        "Nome(s) do(s) Réu(s)": "Pedro Silva, Ana Souza",
        "Documento(s) do(s) Réu(s)": "321.654.987-00, 654.987.321-00"
    },
    {
        "Nome do Autor": "Fernanda Rocha",
        "Documento do Autor": "123.456.789-00",
        "Nome(s) do(s) Réu(s)": "Lucas Mendes, Paula Lima",
        "Documento(s) do(s) Réu(s)": "987.654.321-00, 321.987.654-00"
    },
    {
        "Nome do Autor": "Rafael Costa",
        "Documento do Autor": "456.789.123-45",
        "Nome(s) do(s) Réu(s)": "Mariana Silva, Carlos Santos",
        "Documento(s) do(s) Réu(s)": "654.321.987-00, 987.321.654-00"
    },
    {
        "Nome do Autor": "Ana Clara",
        "Documento do Autor": "321.654.987-00",
        "Nome(s) do(s) Réu(s)": "Victor Lima, Julia Mendes",
        "Documento(s) do(s) Réu(s)": "123.321.123-00, 456.654.456-00"
    }
]

# Caminho para salvar os PDFs
diretorio = r"D:\Área de Trabalho\Documentos\Teste técnico Finch"

# Criação do diretório caso não exista
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# Função para gerar cada PDF
def gerar_pdf(dados, indice):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Nome do Autor: {dados['Nome do Autor']}", ln=1)
    pdf.cell(0, 10, f"Documento do Autor: {dados['Documento do Autor']}", ln=1)
    pdf.cell(0, 10, f"Nome(s) do(s) Réu(s): {dados['Nome(s) do(s) Réu(s)']}", ln=1)
    pdf.cell(0, 10, f"Documento(s) do(s) Réu(s): {dados['Documento(s) do(s) Réu(s)']}", ln=1)

    arquivo_pdf = os.path.join(diretorio, f"processo_teste_{indice}.pdf")
    pdf.output(arquivo_pdf)
    print(f"PDF {indice} gerado com sucesso no caminho: {arquivo_pdf}")

# Gerar os cinco PDFs
for i, dados in enumerate(dados_processos):
    gerar_pdf(dados, i + 1)
