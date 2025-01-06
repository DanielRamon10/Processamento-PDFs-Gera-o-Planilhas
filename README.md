Processamento e Extração de Dados de Arquivos PDF
Este projeto é uma aplicação web construída com Flask que permite o envio de arquivos PDF, processando-os para extrair informações específicas, como nome do autor, documento do autor, nomes dos réus e documentos dos réus. As informações extraídas são armazenadas em uma planilha Excel, que pode ser baixada pelo usuário.

Funcionalidades
Envio de Arquivos PDF: O usuário pode enviar múltiplos arquivos PDF através de um formulário simples.
Extração de Dados: O sistema processa os PDFs e extrai informações relevantes de cada processo, como nome do autor, documentos dos réus, etc.
Geração de Planilha Excel: Após o processamento, os dados extraídos são organizados em uma planilha Excel, que pode ser baixada.
Interface Simples: A interface é intuitiva, com botões claros para realizar upload e download dos arquivos.
Tecnologias Utilizadas
Flask: Framework web em Python para criar a aplicação.
pdfminer: Biblioteca utilizada para a extração de texto de arquivos PDF.
pandas: Usada para manipulação dos dados extraídos e geração da planilha Excel.
HTML/CSS: Para criação da interface do usuário com estilo personalizado.
