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


# ------------------------------------------------------------------
# Metadados (título, autor, assunto)
# ------------------------------------------------------------------

def editar_metadados(entrada, saida, titulo=None, autor=None, assunto=None):
    leitor = PdfReader(entrada)
    escritor = PdfWriter()
    for pagina in leitor.pages:
        escritor.add_page(pagina)

    metadados = {}
    if titulo:
        metadados["/Title"] = titulo
    if autor:
        metadados["/Author"] = autor
    if assunto:
        metadados["/Subject"] = assunto

    escritor.add_metadata(metadados)
    with open(saida, "wb") as f:
        escritor.write(f)


# ------------------------------------------------------------------
# Rotacionar páginas (todas ou um intervalo específico)
# ------------------------------------------------------------------

def rotacionar_paginas(entrada, saida, graus, expressao_paginas=None):
    leitor = PdfReader(entrada)
    total = len(leitor.pages)

    if expressao_paginas:
        indices = set(_parse_intervalo_paginas(expressao_paginas, total))
    else:
        indices = set(range(total))

    escritor = PdfWriter()
    for i, pagina in enumerate(leitor.pages):
        if i in indices:
            pagina.rotate(graus)
        escritor.add_page(pagina)

    with open(saida, "wb") as f:
        escritor.write(f)


# ------------------------------------------------------------------
# Dividir PDF (o oposto de unir)
# ------------------------------------------------------------------

def dividir_pdf(entrada, pasta_saida, paginas_por_arquivo=1):
    leitor = PdfReader(entrada)
    total = len(leitor.pages)
    nome_base = os.path.splitext(os.path.basename(entrada))[0]
    gerados = []

    for inicio in range(0, total, paginas_por_arquivo):
        fim = min(inicio + paginas_por_arquivo, total)
        escritor = PdfWriter()
        for i in range(inicio, fim):
            escritor.add_page(leitor.pages[i])

        nome_saida = os.path.join(pasta_saida, f"{nome_base}_parte_{inicio + 1}-{fim}.pdf")
        with open(nome_saida, "wb") as f:
            escritor.write(f)
        gerados.append(nome_saida)

    return gerados


# ------------------------------------------------------------------
# Numeração automática de páginas ("Página X de Y")
# ------------------------------------------------------------------

def numerar_paginas(entrada, saida, formato="Página {atual} de {total}"):
    leitor = PdfReader(entrada)
    total = len(leitor.pages)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        caminho_overlay = tmp.name

    try:
        c = canvas.Canvas(caminho_overlay)
        for i, pagina in enumerate(leitor.pages, start=1):
            largura = float(pagina.mediabox.width)
            altura = float(pagina.mediabox.height)
            c.setPageSize((largura, altura))
            texto = formato.format(atual=i, total=total)
            c.setFont("Helvetica", 9)
            c.drawCentredString(largura / 2, 20, texto)
            c.showPage()
        c.save()

        leitor_overlay = PdfReader(caminho_overlay)
        escritor = PdfWriter()
        for pagina, pagina_overlay in zip(leitor.pages, leitor_overlay.pages):
            pagina.merge_page(pagina_overlay)
            escritor.add_page(pagina)

        with open(saida, "wb") as f:
            escritor.write(f)
    finally:
        if os.path.exists(caminho_overlay):
            os.remove(caminho_overlay)


# ------------------------------------------------------------------
# Remover senha (só funciona se você souber a senha atual)
# ------------------------------------------------------------------

def remover_senha(entrada, saida, senha):
    leitor = PdfReader(entrada)
    if leitor.is_encrypted:
        resultado = leitor.decrypt(senha)
        if not resultado:
            raise ValueError("Senha incorreta.")

    escritor = PdfWriter()
    for pagina in leitor.pages:
        escritor.add_page(pagina)
    with open(saida, "wb") as f:
        escritor.write(f)


# ------------------------------------------------------------------
# Censura/redação (barra preta cobrindo uma faixa da página)
# ------------------------------------------------------------------

_FAIXAS_CENSURA = {
    "topo": (0.85, 1.0),
    "rodape": (0.0, 0.15),
    "meio": (0.4, 0.6),
}

def censurar_pdf(entrada, saida, regiao="rodape"):
    y0_frac, y1_frac = _FAIXAS_CENSURA.get(regiao, _FAIXAS_CENSURA["rodape"])
    leitor = PdfReader(entrada)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        caminho_overlay = tmp.name

    try:
        c = canvas.Canvas(caminho_overlay)
        for pagina in leitor.pages:
            largura = float(pagina.mediabox.width)
            altura = float(pagina.mediabox.height)
            c.setPageSize((largura, altura))
            y0 = altura * y0_frac
            y1 = altura * y1_frac
            c.setFillColorRGB(0, 0, 0)
            c.rect(0, y0, largura, y1 - y0, fill=1, stroke=0)
            c.showPage()
        c.save()

        leitor_overlay = PdfReader(caminho_overlay)
        escritor = PdfWriter()
        for pagina, pagina_overlay in zip(leitor.pages, leitor_overlay.pages):
            pagina.merge_page(pagina_overlay)
            escritor.add_page(pagina)

        with open(saida, "wb") as f:
            escritor.write(f)
    finally:
        if os.path.exists(caminho_overlay):
            os.remove(caminho_overlay)


# ------------------------------------------------------------------
# Comparar dois PDFs (diferenças de texto)
# ------------------------------------------------------------------

def _extrair_linhas(caminho):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        caminho_txt = tmp.name
    try:
        subprocess.run(["pdftotext", "-layout", caminho, caminho_txt], check=True)
        with open(caminho_txt, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().splitlines()
    finally:
        if os.path.exists(caminho_txt):
            os.remove(caminho_txt)


def comparar_pdfs(caminho_a, caminho_b):
    import difflib

    linhas_a = _extrair_linhas(caminho_a)
    linhas_b = _extrair_linhas(caminho_b)

    diff = list(difflib.unified_diff(linhas_a, linhas_b, lineterm=""))
    adicionadas = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removidas = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))

    return {
        "identico": adicionadas == 0 and removidas == 0,
        "linhas_adicionadas": adicionadas,
        "linhas_removidas": removidas,
        "trecho_diff": "\n".join(diff[:40]),
    }


# ------------------------------------------------------------------
# Carimbo/assinatura simples (imagem posicionada em todas as páginas)
# ------------------------------------------------------------------

_POSICOES_CARIMBO = {
    "inferior_direito": lambda w, h, iw, ih, m: (w - iw - m, m),
    "inferior_esquerdo": lambda w, h, iw, ih, m: (m, m),
    "superior_direito": lambda w, h, iw, ih, m: (w - iw - m, h - ih - m),
    "superior_esquerdo": lambda w, h, iw, ih, m: (m, h - ih - m),
}

def adicionar_carimbo(entrada, saida, caminho_imagem, posicao="inferior_direito", largura_pct=0.2):
    from PIL import Image as PILImage

    leitor = PdfReader(entrada)
    img = PILImage.open(caminho_imagem)
    proporcao = img.height / img.width

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        caminho_overlay = tmp.name

    try:
        c = canvas.Canvas(caminho_overlay)
        for pagina in leitor.pages:
            largura = float(pagina.mediabox.width)
            altura = float(pagina.mediabox.height)
            c.setPageSize((largura, altura))

            largura_img = largura * largura_pct
            altura_img = largura_img * proporcao
            margem = 20
            funcao_pos = _POSICOES_CARIMBO.get(posicao, _POSICOES_CARIMBO["inferior_direito"])
            x, y = funcao_pos(largura, altura, largura_img, altura_img, margem)

            c.drawImage(caminho_imagem, x, y, width=largura_img, height=altura_img, mask="auto")
            c.showPage()
        c.save()

        leitor_overlay = PdfReader(caminho_overlay)
        escritor = PdfWriter()
        for pagina, pagina_overlay in zip(leitor.pages, leitor_overlay.pages):
            pagina.merge_page(pagina_overlay)
            escritor.add_page(pagina)

        with open(saida, "wb") as f:
            escritor.write(f)
    finally:
        if os.path.exists(caminho_overlay):
            os.remove(caminho_overlay)


# ------------------------------------------------------------------
# Verificação de integridade
# ------------------------------------------------------------------

def verificar_pdf(caminho):
    """Retorna (ok, mensagem)."""
    try:
        leitor = PdfReader(caminho)
        total = len(leitor.pages)
        if total == 0:
            return False, "PDF sem páginas."
        return True, f"{total} página(s), sem problemas detectados."
    except Exception as e:
        return False, str(e)
