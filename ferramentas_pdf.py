"""
ferramentas_pdf.py - Ferramentas avançadas sobre PDFs já existentes
Criado por: TheAceModz

Dependências:
    pip install pypdf reportlab
    pkg install ghostscript poppler tesseract tesseract-data-por
"""

import os
import glob
import subprocess
import tempfile

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# ------------------------------------------------------------------
# Unir PDFs
# ------------------------------------------------------------------

def unir_pdfs(lista_caminhos, saida):
    escritor = PdfWriter()
    for caminho in lista_caminhos:
        leitor = PdfReader(caminho)
        for pagina in leitor.pages:
            escritor.add_page(pagina)
    with open(saida, "wb") as f:
        escritor.write(f)


# ------------------------------------------------------------------
# Comprimir PDF (via Ghostscript)
# niveis validos: screen (menor/pior qualidade), ebook, printer, prepress
# ------------------------------------------------------------------

def comprimir_pdf(entrada, saida, nivel="ebook"):
    subprocess.run([
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{nivel}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={saida}", entrada
    ], check=True)


# ------------------------------------------------------------------
# Extrair páginas específicas (ex: "1-3,5,8-10")
# ------------------------------------------------------------------

def _parse_intervalo_paginas(expressao, total_paginas):
    paginas = set()
    for parte in expressao.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            ini, fim = parte.split("-")
            for p in range(int(ini), int(fim) + 1):
                if 1 <= p <= total_paginas:
                    paginas.add(p - 1)
        else:
            p = int(parte)
            if 1 <= p <= total_paginas:
                paginas.add(p - 1)
    return sorted(paginas)


def extrair_paginas(entrada, saida, expressao_paginas):
    leitor = PdfReader(entrada)
    total = len(leitor.pages)
    indices = _parse_intervalo_paginas(expressao_paginas, total)

    if not indices:
        raise ValueError("Nenhuma página válida foi selecionada.")

    escritor = PdfWriter()
    for i in indices:
        escritor.add_page(leitor.pages[i])

    with open(saida, "wb") as f:
        escritor.write(f)


# ------------------------------------------------------------------
# Proteger com senha
# ------------------------------------------------------------------

def proteger_pdf(entrada, saida, senha):
    leitor = PdfReader(entrada)
    escritor = PdfWriter()
    for pagina in leitor.pages:
        escritor.add_page(pagina)
    escritor.encrypt(senha)
    with open(saida, "wb") as f:
        escritor.write(f)


# ------------------------------------------------------------------
# Marca d'água (texto diagonal semi-transparente em todas as páginas)
# ------------------------------------------------------------------

def adicionar_marca_dagua(entrada, saida, texto):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        caminho_marca = tmp.name

    try:
        c = canvas.Canvas(caminho_marca, pagesize=letter)
        c.saveState()
        c.translate(300, 400)
        c.rotate(45)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        try:
            c.setFillAlpha(0.3)
        except Exception:
            pass
        c.setFont("Helvetica-Bold", 40)
        c.drawCentredString(0, 0, texto)
        c.restoreState()
        c.save()

        leitor_base = PdfReader(entrada)
        leitor_marca = PdfReader(caminho_marca)
        pagina_marca_modelo = leitor_marca.pages[0]

        escritor = PdfWriter()
        for pagina in leitor_base.pages:
            pagina.merge_page(pagina_marca_modelo)
            escritor.add_page(pagina)

        with open(saida, "wb") as f:
            escritor.write(f)
    finally:
        if os.path.exists(caminho_marca):
            os.remove(caminho_marca)


# ------------------------------------------------------------------
# OCR - torna um PDF escaneado pesquisável
# ------------------------------------------------------------------

def ocr_pdf(entrada, saida, idioma="por"):
    with tempfile.TemporaryDirectory() as pasta_tmp:
        prefixo_imagens = os.path.join(pasta_tmp, "pagina")
        subprocess.run(
            ["pdftoppm", "-png", "-r", "300", entrada, prefixo_imagens],
            check=True
        )

        imagens = sorted(glob.glob(f"{prefixo_imagens}-*.png"))
        if not imagens:
            raise RuntimeError("Não foi possível rasterizar o PDF.")

        pdfs_pagina = []
        for imagem in imagens:
            saida_base = os.path.splitext(imagem)[0]
            subprocess.run(
                ["tesseract", imagem, saida_base, "-l", idioma, "pdf"],
                check=True
            )
            pdfs_pagina.append(saida_base + ".pdf")

        unir_pdfs(pdfs_pagina, saida)
