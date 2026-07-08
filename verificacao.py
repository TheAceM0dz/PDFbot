import os

FORMATOS_SUPORTADOS = [
    ".docx", ".txt", ".md", ".html",
    ".jpg", ".jpeg", ".png"
]

FORMATOS_DESTINO_PDF = [".png", ".jpg", ".jpeg", ".docx", ".txt"]

def arquivo_existe(caminho):
    return os.path.exists(caminho)

def arquivo_vazio(caminho):
    return os.path.getsize(caminho) == 0

def obter_extensao(caminho):
    return os.path.splitext(caminho)[1].lower()

def extensao_compativel(extensao):
    return extensao in FORMATOS_SUPORTADOS

def eh_pdf(caminho):
    return obter_extensao(caminho) == ".pdf"
