"""
conversao_extra.py - Conversões extras que não são só "arquivo -> PDF"
Criado por: TheAceModz

Dependências:
    pkg install pandoc poppler espeak-ng    (ou 'espeak' dependendo do repo)
"""

import os
import subprocess
import tempfile

from PIL import Image


# ------------------------------------------------------------------
# PDF -> EPUB (via extração de texto + pandoc)
# ------------------------------------------------------------------

def pdf_para_epub(entrada, saida, titulo=None, autor=None):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        caminho_txt = tmp.name

    try:
        subprocess.run(["pdftotext", "-layout", entrada, caminho_txt], check=True)

        comando = ["pandoc", caminho_txt, "-o", saida]
        if titulo:
            comando += ["--metadata", f"title={titulo}"]
        if autor:
            comando += ["--metadata", f"author={autor}"]

        subprocess.run(comando, check=True)
    finally:
        if os.path.exists(caminho_txt):
            os.remove(caminho_txt)


# ------------------------------------------------------------------
# PDF -> Áudio (via espeak, 100% offline, sem Termux:API)
# ------------------------------------------------------------------

_VOZES = {"pt": "pt-br", "en": "en-us"}

def pdf_para_audio(entrada, saida, idioma="pt"):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        caminho_txt = tmp.name

    try:
        subprocess.run(["pdftotext", "-layout", entrada, caminho_txt], check=True)
        voz = _VOZES.get(idioma, "pt-br")
        subprocess.run(
            ["espeak", "-v", voz, "-s", "150", "-f", caminho_txt, "-w", saida],
            check=True
        )
    finally:
        if os.path.exists(caminho_txt):
            os.remove(caminho_txt)


# ------------------------------------------------------------------
# Colagem de fotos em grade (várias fotos por página, vira 1 PDF)
# ------------------------------------------------------------------

def montar_grade_fotos(lista_imagens, saida, colunas=2, linhas=2,
                        largura_pagina=1240, altura_pagina=1754):
    por_pagina = colunas * linhas
    paginas = []

    for inicio in range(0, len(lista_imagens), por_pagina):
        lote = lista_imagens[inicio:inicio + por_pagina]
        pagina = Image.new("RGB", (largura_pagina, altura_pagina), "white")

        cel_largura = largura_pagina // colunas
        cel_altura = altura_pagina // linhas

        for idx, caminho_img in enumerate(lote):
            img = Image.open(caminho_img)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.thumbnail((cel_largura - 20, cel_altura - 20))

            col = idx % colunas
            lin = idx // colunas
            x = col * cel_largura + (cel_largura - img.width) // 2
            y = lin * cel_altura + (cel_altura - img.height) // 2
            pagina.paste(img, (x, y))

        paginas.append(pagina)

    if not paginas:
        raise ValueError("Nenhuma imagem válida foi informada.")

    paginas[0].save(saida, save_all=True, append_images=paginas[1:])
