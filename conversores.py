import os
import glob
import tempfile
import subprocess
import zipfile
import shutil
from PIL import Image

# Cabeçalho LaTeX que força um limite de tamanho pras imagens do documento.
# Corrige o erro "Dimension too large" que acontece quando um EPUB/DOCX tem
# uma imagem (geralmente a capa) com metadado de resolução corrompido
# (ex: EXIF/JFIF relatando "0x0" ou "1x1"), fazendo o LaTeX tentar calcular
# um tamanho físico absurdo pra ela.
_LATEX_HEADER_IMAGENS = r"""
\usepackage{graphicx}
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\makeatother
\setkeys{Gin}{width=\maxwidth,height=0.85\textheight,keepaspectratio}
"""

def _cabecalho_imagens_seguro():
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".tex", delete=False, encoding="utf-8"
    )
    tmp.write(_LATEX_HEADER_IMAGENS)
    tmp.close()
    return tmp.name


def _converter_via_pandoc(caminho, saida, toc=False):
    cabecalho = _cabecalho_imagens_seguro()
    try:
        comando = [
            "pandoc", caminho, "-o", saida,
            "--pdf-engine=tectonic",
            f"--include-in-header={cabecalho}",
        ]
        if toc:
            comando.append("--toc")

        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode != 0:
            erro = resultado.stderr.strip().splitlines()
            trecho = "\n".join(erro[-6:]) if erro else "erro desconhecido do pandoc/tectonic."
            raise RuntimeError(trecho)
    finally:
        if os.path.exists(cabecalho):
            os.remove(cabecalho)


def converter_docx(caminho, saida, toc=False):
    _converter_via_pandoc(caminho, saida, toc)

def converter_markdown(caminho, saida, toc=False):
    _converter_via_pandoc(caminho, saida, toc)

def converter_html(caminho, saida, toc=False):
    _converter_via_pandoc(caminho, saida, toc)

def converter_txt(caminho, saida, toc=False):
    _converter_via_pandoc(caminho, saida, toc)


# ------------------------------------------------------------------
# EPUB -> PDF precisa de um cuidado a mais: capas/imagens de EPUB
# frequentemente têm metadado de resolução (DPI) corrompido, o que faz
# o LaTeX estourar ao calcular o tamanho físico da imagem ("Dimension
# too large"). A correção de verdade é reprocessar cada imagem embutida
# com o Pillow, normalizando o DPI, antes de passar pro pandoc.
# ------------------------------------------------------------------

_EXTENSOES_IMAGEM = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def _reempacotar_epub_com_imagens_seguras(caminho_epub):
    """Extrai o EPUB (é um .zip), corrige o DPI de toda imagem embutida
    e reempacota num novo arquivo .epub temporário. Retorna o caminho
    do novo arquivo — quem chamar é responsável por apagá-lo depois."""
    pasta_tmp = tempfile.mkdtemp(prefix="epub_fix_")

    with zipfile.ZipFile(caminho_epub, "r") as z:
        z.extractall(pasta_tmp)

    for raiz, _, arquivos in os.walk(pasta_tmp):
        for nome in arquivos:
            if not nome.lower().endswith(_EXTENSOES_IMAGEM):
                continue
            caminho_img = os.path.join(raiz, nome)
            try:
                img = Image.open(caminho_img)
                img.load()
                if nome.lower().endswith((".jpg", ".jpeg")) and img.mode in ("P", "RGBA"):
                    img = img.convert("RGB")
                # Resalva com um DPI normal e consistente, descartando
                # qualquer metadado EXIF/JFIF de resolução quebrado.
                img.save(caminho_img, dpi=(96, 96))
            except Exception:
                # Se uma imagem específica não puder ser processada,
                # não trava a conversão inteira por causa dela.
                continue

    with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp_saida:
        caminho_novo_epub = tmp_saida.name

    try:
        with zipfile.ZipFile(caminho_novo_epub, "w") as z:
            caminho_mimetype = os.path.join(pasta_tmp, "mimetype")
            if os.path.exists(caminho_mimetype):
                z.write(caminho_mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
            for raiz, _, arquivos in os.walk(pasta_tmp):
                for nome in arquivos:
                    caminho_completo = os.path.join(raiz, nome)
                    nome_relativo = os.path.relpath(caminho_completo, pasta_tmp)
                    if nome_relativo == "mimetype":
                        continue
                    z.write(caminho_completo, nome_relativo, compress_type=zipfile.ZIP_DEFLATED)
    finally:
        shutil.rmtree(pasta_tmp, ignore_errors=True)

    return caminho_novo_epub


def converter_epub(caminho, saida, toc=False):
    epub_corrigido = _reempacotar_epub_com_imagens_seguras(caminho)
    try:
        _converter_via_pandoc(epub_corrigido, saida, toc)
    finally:
        if os.path.exists(epub_corrigido):
            os.remove(epub_corrigido)

def converter_imagem(caminho, saida, tamanho_max=2000, qualidade=85):
    """Reduz automaticamente fotos muito grandes (comuns em câmeras de
    celular) antes de embutir no PDF, deixando o arquivo final bem menor."""
    img = Image.open(caminho)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    if max(img.size) > tamanho_max:
        img.thumbnail((tamanho_max, tamanho_max))
    img.save(saida, quality=qualidade, optimize=True)


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
