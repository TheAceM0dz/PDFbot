import os
import glob
import tempfile
import subprocess
from PIL import Image

def converter_docx(caminho, saida):
    subprocess.run(["pandoc", caminho, "-o", saida, "--pdf-engine=tectonic"], check=True)

def converter_markdown(caminho, saida):
    subprocess.run(["pandoc", caminho, "-o", saida, "--pdf-engine=tectonic"], check=True)

def converter_html(caminho, saida):
    subprocess.run(["pandoc", caminho, "-o", saida, "--pdf-engine=tectonic"], check=True)

def converter_txt(caminho, saida):
    subprocess.run(["pandoc", caminho, "-o", saida, "--pdf-engine=tectonic"], check=True)

def converter_imagem(caminho, saida):
    img = Image.open(caminho)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(saida)


# ------------------------------------------------------------------
# Conversões de PDF para outros formatos
# Requer: pkg install poppler   (pdftoppm / pdftotext)
#         pip install python-docx   (apenas pra converter_pdf_para_docx)
# ------------------------------------------------------------------

def _pdf_para_imagem(caminho, saida, formato):
    """formato: 'png' ou 'jpeg'. Gera 1 imagem por pagina do PDF."""
    pasta_saida = os.path.dirname(saida) or "."
    base = os.path.splitext(os.path.basename(saida))[0]
    prefixo = os.path.join(pasta_saida, base)

    flag = "-png" if formato == "png" else "-jpeg"
    subprocess.run(
        ["pdftoppm", flag, "-r", "200", caminho, prefixo],
        check=True
    )

    extensao = "png" if formato == "png" else "jpg"
    gerados = sorted(glob.glob(f"{prefixo}-*.{extensao}"))

    if not gerados:
        raise RuntimeError("pdftoppm nao gerou nenhuma imagem.")

    if len(gerados) == 1:
        destino_final = saida if saida.lower().endswith(f".{extensao}") else f"{saida}.{extensao}"
        os.replace(gerados[0], destino_final)

def converter_pdf_para_png(caminho, saida):
    _pdf_para_imagem(caminho, saida, "png")

def converter_pdf_para_jpeg(caminho, saida):
    _pdf_para_imagem(caminho, saida, "jpeg")

def converter_pdf_para_txt(caminho, saida):
    subprocess.run(["pdftotext", "-layout", caminho, saida], check=True)

def converter_pdf_para_docx(caminho, saida):
    """
    Conversao simples: extrai o texto do PDF (via pdftotext) e monta
    um .docx com paragrafos. Nao preserva layout, imagens ou tabelas
    complexas do PDF original.
    """
    from docx import Document

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        caminho_txt = tmp.name

    try:
        subprocess.run(["pdftotext", "-layout", caminho, caminho_txt], check=True)
        with open(caminho_txt, "r", encoding="utf-8", errors="ignore") as f:
            conteudo = f.read()

        doc = Document()
        for paragrafo in conteudo.split("\n\n"):
            doc.add_paragraph(paragrafo.strip())
        doc.save(saida)
    finally:
        if os.path.exists(caminho_txt):
            os.remove(caminho_txt)
