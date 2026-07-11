"""
PDFBOT - Conversor de arquivos para PDF
Criado por: TheAceModz
"""

import os
import questionary

from conversores import (
    converter_docx,
    converter_txt,
    converter_markdown,
    converter_html,
    converter_imagem,
    converter_pdf_para_png,
    converter_pdf_para_jpeg,
    converter_pdf_para_docx,
    converter_pdf_para_txt,
)
from verificacao import (
    arquivo_existe,
    arquivo_vazio,
    obter_extensao,
    extensao_compativel,
    eh_pdf,
)
from historico import salvar_historico, carregar_historico
from lote import listar_arquivos_compativeis
import ferramentas_pdf as fpdf
import conversao_extra as cextra

import ui

conversores = {
    ".docx": converter_docx,
    ".txt": converter_txt,
    ".md": converter_markdown,
    ".html": converter_html,
    ".jpg": converter_imagem,
    ".jpeg": converter_imagem,
    ".png": converter_imagem
}

conversores_de_pdf = {
    ".png": converter_pdf_para_png,
    ".jpg": converter_pdf_para_jpeg,
    ".jpeg": converter_pdf_para_jpeg,
    ".docx": converter_pdf_para_docx,
    ".txt": converter_pdf_para_txt,
}

# Conversores que aceitam sumário automático (--toc). Imagens não têm texto.
EXTENSOES_COM_TOC = {".docx", ".md", ".html", ".txt"}

# Estado da sessão atual: contadores + último arquivo gerado (pro "desfazer")
_sessao = {"sucessos": 0, "falhas": 0, "ultima_saida": None}


def _marcar_sucesso(saida=None):
    _sessao["sucessos"] += 1
    if saida:
        _sessao["ultima_saida"] = saida

def _marcar_falha():
    _sessao["falhas"] += 1


def escolher_saida(arquivo):
    nome_base = os.path.splitext(arquivo)[0]
    padrao = nome_base + ".pdf"
    ui.print_info(ui.t("msg_saida_padrao", caminho=padrao))
    return ui.perguntar_caminho_saida(padrao)


# ------------------------------------------------------------------
# Converter arquivo -> PDF / PDF -> outro formato / Lote / Grade de fotos
# ------------------------------------------------------------------

def converter_arquivo():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_converter"))
    arquivo = ui.perguntar_caminho_arquivo()

    if not arquivo:
        ui.print_erro(ui.t("msg_nenhum_caminho"))
        return

    if not arquivo_existe(arquivo):
        ui.print_erro(ui.t("msg_arquivo_nao_existe"))
        salvar_historico(arquivo, "Erro - arquivo não existe")
        return

    if arquivo_vazio(arquivo):
        ui.print_erro(ui.t("msg_arquivo_vazio"))
        salvar_historico(arquivo, "Erro - arquivo vazio")
        return

    extensao = obter_extensao(arquivo)
    if not extensao_compativel(extensao):
        ui.print_erro(ui.t("msg_formato_incompativel"))
        salvar_historico(arquivo, "Erro - formato não compatível")
        return

    ui.preview_arquivo(arquivo)

    toc = False
    if extensao in EXTENSOES_COM_TOC:
        toc = ui.perguntar_toc()

    saida = escolher_saida(arquivo)
    saida = ui.nome_seguro(saida)

    pasta_saida = os.path.dirname(saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        ui.print_erro(ui.t("msg_pasta_destino_inexistente"))
        salvar_historico(arquivo, "Erro - pasta de destino não existe")
        return

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_formato_saida"): "PDF",
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            if extensao in EXTENSOES_COM_TOC:
                conversores[extensao](arquivo, saida, toc=toc)
            else:
                conversores[extensao](arquivo, saida)
        ui.print_sucesso(ui.t("msg_pdf_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except PermissionError:
        ui.print_erro(ui.t("msg_sem_permissao"))
        salvar_historico(arquivo, "Erro - sem permissão")
        _marcar_falha()
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_ferramenta_ausente_pandoc"))
        salvar_historico(arquivo, "Erro - ferramenta ausente")
        _marcar_falha()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_converter", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def converter_de_pdf():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_de_pdf"))
    arquivo = ui.perguntar_caminho_arquivo()

    if not arquivo:
        ui.print_erro(ui.t("msg_nenhum_caminho"))
        return

    if not arquivo_existe(arquivo):
        ui.print_erro(ui.t("msg_arquivo_nao_existe"))
        salvar_historico(arquivo, "Erro - arquivo não existe")
        return

    if arquivo_vazio(arquivo):
        ui.print_erro(ui.t("msg_arquivo_vazio"))
        salvar_historico(arquivo, "Erro - arquivo vazio")
        return

    if not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_nao_e_pdf"))
        salvar_historico(arquivo, "Erro - não é PDF")
        return

    ui.preview_arquivo(arquivo)

    formato_destino = ui.perguntar_formato_destino()
    if not formato_destino:
        ui.print_erro(ui.t("msg_nenhum_formato"))
        return

    nome_base = os.path.splitext(arquivo)[0]
    padrao = nome_base + formato_destino
    ui.print_info(ui.t("msg_saida_padrao", caminho=padrao))
    saida = ui.perguntar_caminho_saida(padrao)
    saida = ui.nome_seguro(saida)

    pasta_saida = os.path.dirname(saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        ui.print_erro(ui.t("msg_pasta_destino_inexistente"))
        salvar_historico(arquivo, "Erro - pasta de destino não existe")
        return

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_formato_saida"): formato_destino,
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            conversores_de_pdf[formato_destino](arquivo, saida)
        ui.print_sucesso(ui.t("msg_arquivo_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except PermissionError:
        ui.print_erro(ui.t("msg_sem_permissao"))
        salvar_historico(arquivo, "Erro - sem permissão")
        _marcar_falha()
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_ferramenta_ausente_poppler"))
        salvar_historico(arquivo, "Erro - ferramenta ausente")
        _marcar_falha()
    except ImportError:
        ui.print_erro(ui.t("msg_lib_ausente_docx"))
        salvar_historico(arquivo, "Erro - biblioteca ausente")
        _marcar_falha()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_converter", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def converter_lote():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_lote"))
    pasta = ui.escolher_pasta_para_lote()
    extensoes = list(conversores.keys())
    arquivos = listar_arquivos_compativeis(pasta, extensoes)

    if not arquivos:
        ui.print_info(ui.t("msg_nenhum_arquivo_compativel"))
        return

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_pasta"): pasta,
        ui.t("resumo_qtd_arquivos"): len(arquivos),
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    sucessos = 0
    falhas = 0

    with ui.barra_progresso(len(arquivos)) as progresso:
        tarefa = progresso.add_task("lote", total=len(arquivos))
        for arquivo in arquivos:
            extensao = obter_extensao(arquivo)
            nome_base = os.path.splitext(arquivo)[0]
            saida = ui.nome_seguro(nome_base + ".pdf")
            try:
                if arquivo_vazio(arquivo):
                    raise ValueError("arquivo vazio")
                conversores[extensao](arquivo, saida)
                salvar_historico(arquivo, "Sucesso")
                sucessos += 1
            except Exception as e:
                salvar_historico(arquivo, f"Erro - {e}")
                falhas += 1
            progresso.advance(tarefa)

    ui.print_sucesso(ui.t("msg_lote_sucesso", n=sucessos))
    if falhas:
        ui.print_erro(ui.t("msg_lote_falhas", n=falhas))
    if arquivos:
        ui.salvar_ultimo_diretorio(arquivos[0])

    _sessao["sucessos"] += sucessos
    _sessao["falhas"] += falhas


def converter_grade_fotos():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_converter"), ui.t("trilha_grade"))
    caminhos = ui.perguntar_lista_fotos()
    if len(caminhos) < 1:
        ui.print_erro(ui.t("msg_unir_minimo"))
        return

    colunas, linhas = ui.perguntar_grade_fotos()
    padrao = os.path.join(os.path.dirname(caminhos[0]), "colagem_fotos.pdf")
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivos"): "\n".join(os.path.basename(c) for c in caminhos),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            cextra.montar_grade_fotos(caminhos, saida, colunas=colunas, linhas=linhas)
        ui.print_sucesso(ui.t("msg_grade_sucesso", caminho=saida))
        salvar_historico(", ".join(caminhos), "Sucesso - grade de fotos")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_grade", erro=e))
        salvar_historico(", ".join(caminhos), f"Erro - {e}")
        _marcar_falha()


def menu_converter():
    while True:
        escolha = ui.submenu_converter()

        if escolha == "arquivo":
            converter_arquivo()
        elif escolha == "de_pdf":
            converter_de_pdf()
        elif escolha == "lote":
            converter_lote()
        elif escolha == "grade":
            converter_grade_fotos()
        elif escolha == "voltar" or escolha is None:
            return

        if escolha not in ("voltar", None):
            questionary.press_any_key_to_continue(ui.t("msg_pressione_continuar")).ask()


# ------------------------------------------------------------------
# Ferramentas de PDF
# ------------------------------------------------------------------

def ferramenta_unir():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_unir"))
    caminhos = ui.perguntar_lista_pdfs_para_unir()
    if len(caminhos) < 2:
        ui.print_erro(ui.t("msg_unir_minimo"))
        return

    padrao = os.path.join(os.path.dirname(caminhos[0]), "pdf_unido.pdf")
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivos"): "\n".join(os.path.basename(c) for c in caminhos),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_unindo')}[/bold cyan]", spinner="dots"):
            fpdf.unir_pdfs(caminhos, saida)
        ui.print_sucesso(ui.t("msg_unir_sucesso", caminho=saida))
        salvar_historico(", ".join(caminhos), "Sucesso - unir")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_unir", erro=e))
        salvar_historico(", ".join(caminhos), f"Erro - {e}")
        _marcar_falha()


def ferramenta_dividir():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_dividir"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    modo = ui.perguntar_modo_divisao()
    paginas_por_arquivo = 1 if modo == "pagina" else ui.perguntar_n_paginas_divisao()

    pasta_saida = os.path.dirname(arquivo) or "."

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): pasta_saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            gerados = fpdf.dividir_pdf(arquivo, pasta_saida, paginas_por_arquivo)
        ui.print_sucesso(ui.t("msg_dividir_sucesso", n=len(gerados), pasta=pasta_saida))
        salvar_historico(arquivo, "Sucesso - dividir")
        if gerados:
            _marcar_sucesso(gerados[-1])
        else:
            _marcar_sucesso()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_dividir", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_comprimir():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_comprimir"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    nivel = ui.perguntar_nivel_compressao()
    if not nivel:
        return

    padrao = os.path.splitext(arquivo)[0] + "_comprimido.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_nivel"): nivel,
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        tamanho_antes = os.path.getsize(arquivo)
        with ui.console.status(f"[bold cyan]{ui.t('status_comprimindo')}[/bold cyan]", spinner="dots"):
            fpdf.comprimir_pdf(arquivo, saida, nivel)
        tamanho_depois = os.path.getsize(saida)
        reducao = 100 - (tamanho_depois / tamanho_antes * 100)
        ui.print_sucesso(ui.t("msg_comprimir_sucesso", caminho=saida, reducao=reducao))
        salvar_historico(arquivo, f"Sucesso - comprimir ({reducao:.0f}%)")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_ghostscript_ausente"))
        salvar_historico(arquivo, "Erro - ghostscript ausente")
        _marcar_falha()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_comprimir", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_extrair():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_extrair"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    expressao = ui.perguntar_intervalo_paginas()
    if not expressao:
        ui.print_erro(ui.t("msg_paginas_nao_informadas"))
        return

    padrao = os.path.splitext(arquivo)[0] + "_paginas.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_paginas"): expressao,
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_extraindo')}[/bold cyan]", spinner="dots"):
            fpdf.extrair_paginas(arquivo, saida, expressao)
        ui.print_sucesso(ui.t("msg_extrair_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - extrair páginas")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_extrair", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_rotacionar():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_rotacionar"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    graus = ui.perguntar_graus_rotacao()
    if not graus:
        return
    expressao = ui.perguntar_paginas_rotacao()

    padrao = os.path.splitext(arquivo)[0] + "_rotacionado.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            fpdf.rotacionar_paginas(arquivo, saida, graus, expressao)
        ui.print_sucesso(ui.t("msg_rotacionar_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - rotacionar")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_rotacionar", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_numerar():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_numerar"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    formato = ui.perguntar_formato_numeracao()
    padrao = os.path.splitext(arquivo)[0] + "_numerado.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            fpdf.numerar_paginas(arquivo, saida, formato)
        ui.print_sucesso(ui.t("msg_numerar_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - numerar páginas")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_numerar", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_metadados():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_metadados"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    dados = ui.perguntar_metadados()
    padrao = os.path.splitext(arquivo)[0] + "_metadados.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            fpdf.editar_metadados(arquivo, saida, dados["titulo"], dados["autor"], dados["assunto"])
        ui.print_sucesso(ui.t("msg_metadados_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - metadados")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_metadados", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_proteger():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_proteger"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    senha = ui.perguntar_senha()
    if not senha:
        ui.print_erro(ui.t("msg_senha_nao_informada"))
        return

    padrao = os.path.splitext(arquivo)[0] + "_protegido.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_protegendo')}[/bold cyan]", spinner="dots"):
            fpdf.proteger_pdf(arquivo, saida, senha)
        ui.print_sucesso(ui.t("msg_proteger_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - proteger")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_proteger", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_remover_senha():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_remover_senha"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    senha = ui.perguntar_senha_remover()
    if not senha:
        ui.print_erro(ui.t("msg_senha_nao_informada"))
        return

    padrao = os.path.splitext(arquivo)[0] + "_sem_senha.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            fpdf.remover_senha(arquivo, saida, senha)
        ui.print_sucesso(ui.t("msg_remover_senha_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - remover senha")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except ValueError:
        ui.print_erro(ui.t("msg_senha_incorreta"))
        salvar_historico(arquivo, "Erro - senha incorreta")
        _marcar_falha()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_remover_senha", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_censurar():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_censurar"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    regiao = ui.perguntar_regiao_censura()
    if not regiao:
        return

    padrao = os.path.splitext(arquivo)[0] + "_censurado.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            fpdf.censurar_pdf(arquivo, saida, regiao)
        ui.print_sucesso(ui.t("msg_censurar_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - censurar")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_censurar", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_marca_dagua():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_marca"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    texto = ui.perguntar_texto_marca_dagua()
    if not texto:
        ui.print_erro(ui.t("msg_marca_texto_nao_informado"))
        return

    padrao = os.path.splitext(arquivo)[0] + "_marcado.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_texto_marca"): texto,
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_marca')}[/bold cyan]", spinner="dots"):
            fpdf.adicionar_marca_dagua(arquivo, saida, texto)
        ui.print_sucesso(ui.t("msg_marca_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - marca d'água")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_marca", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_carimbo():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_carimbo"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    ui.print_info(ui.t("carimbo_imagem_pergunta"))
    imagem = ui.perguntar_caminho_arquivo()
    if not imagem or not arquivo_existe(imagem):
        ui.print_erro(ui.t("msg_arquivo_nao_existe"))
        return

    posicao = ui.perguntar_posicao_carimbo()
    padrao = os.path.splitext(arquivo)[0] + "_carimbado.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            fpdf.adicionar_carimbo(arquivo, saida, imagem, posicao)
        ui.print_sucesso(ui.t("msg_carimbo_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - carimbo")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_carimbo", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_comparar():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_comparar"))
    arquivo_a = ui.perguntar_caminho_arquivo()
    if not arquivo_a or not arquivo_existe(arquivo_a) or not eh_pdf(arquivo_a):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.print_info(ui.t("comparar_segundo_arquivo"))
    arquivo_b = ui.perguntar_caminho_arquivo()
    if not arquivo_b or not arquivo_existe(arquivo_b) or not eh_pdf(arquivo_b):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            resultado = fpdf.comparar_pdfs(arquivo_a, arquivo_b)

        if resultado["identico"]:
            ui.print_sucesso(ui.t("comparar_identico"))
        else:
            ui.print_info(ui.t(
                "comparar_diferente",
                add=resultado["linhas_adicionadas"],
                rem=resultado["linhas_removidas"],
            ))
        salvar_historico(f"{arquivo_a} vs {arquivo_b}", "Sucesso - comparar")
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_comparar", erro=e))
        salvar_historico(f"{arquivo_a} vs {arquivo_b}", f"Erro - {e}")
        _marcar_falha()


def ferramenta_ocr():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_ocr"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    idioma = ui.perguntar_idioma_ocr()
    if not idioma:
        return

    padrao = os.path.splitext(arquivo)[0] + "_pesquisavel.pdf"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_idioma_ocr"): idioma,
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_ocr')}[/bold cyan]", spinner="dots"):
            fpdf.ocr_pdf(arquivo, saida, idioma)
        ui.print_sucesso(ui.t("msg_ocr_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - OCR")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_tesseract_ausente"))
        salvar_historico(arquivo, "Erro - ferramenta ausente")
        _marcar_falha()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_ocr", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def ferramenta_verificar():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_ferramentas"), ui.t("trilha_verificar"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo):
        ui.print_erro(ui.t("msg_arquivo_nao_existe"))
        return

    ok, mensagem = fpdf.verificar_pdf(arquivo)
    if ok:
        ui.print_sucesso(ui.t("msg_verificar_ok", arquivo=os.path.basename(arquivo), mensagem=mensagem))
        salvar_historico(arquivo, "Sucesso - verificar integridade")
    else:
        ui.print_erro(ui.t("msg_verificar_falha", arquivo=os.path.basename(arquivo), mensagem=mensagem))
        salvar_historico(arquivo, f"Erro - integridade: {mensagem}")


def menu_ferramentas():
    while True:
        escolha = ui.menu_ferramentas()

        if escolha == "unir":
            ferramenta_unir()
        elif escolha == "dividir":
            ferramenta_dividir()
        elif escolha == "comprimir":
            ferramenta_comprimir()
        elif escolha == "extrair":
            ferramenta_extrair()
        elif escolha == "rotacionar":
            ferramenta_rotacionar()
        elif escolha == "numerar":
            ferramenta_numerar()
        elif escolha == "metadados":
            ferramenta_metadados()
        elif escolha == "proteger":
            ferramenta_proteger()
        elif escolha == "remover_senha":
            ferramenta_remover_senha()
        elif escolha == "censurar":
            ferramenta_censurar()
        elif escolha == "marca_dagua":
            ferramenta_marca_dagua()
        elif escolha == "carimbo":
            ferramenta_carimbo()
        elif escolha == "comparar":
            ferramenta_comparar()
        elif escolha == "ocr":
            ferramenta_ocr()
        elif escolha == "verificar":
            ferramenta_verificar()
        elif escolha == "voltar" or escolha is None:
            return

        if escolha not in ("voltar", None):
            questionary.press_any_key_to_continue(ui.t("msg_pressione_continuar")).ask()


# ------------------------------------------------------------------
# Extras: PDF -> EPUB / PDF -> Áudio
# ------------------------------------------------------------------

def extra_epub():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_extras"), ui.t("trilha_epub"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    titulo, autor = ui.perguntar_metadados_epub()
    padrao = os.path.splitext(arquivo)[0] + ".epub"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            cextra.pdf_para_epub(arquivo, saida, titulo, autor)
        ui.print_sucesso(ui.t("msg_epub_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - EPUB")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_epub", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def extra_audio():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_extras"), ui.t("trilha_audio"))
    arquivo = ui.perguntar_caminho_arquivo()
    if not arquivo or not arquivo_existe(arquivo) or not eh_pdf(arquivo):
        ui.print_erro(ui.t("msg_pdf_invalido"))
        return

    ui.preview_arquivo(arquivo)

    idioma = ui.perguntar_idioma_audio()
    if not idioma:
        return

    padrao = os.path.splitext(arquivo)[0] + ".wav"
    saida = ui.nome_seguro(ui.perguntar_caminho_saida(padrao))

    confirmado = ui.confirmar_resumo({
        ui.t("resumo_arquivo"): os.path.basename(arquivo),
        ui.t("resumo_destino"): saida,
    })
    if not confirmado:
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        with ui.console.status(f"[bold cyan]{ui.t('status_convertendo')}[/bold cyan]", spinner="dots"):
            cextra.pdf_para_audio(arquivo, saida, idioma)
        ui.print_sucesso(ui.t("msg_audio_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso - áudio")
        ui.salvar_ultimo_diretorio(saida)
        _marcar_sucesso(saida)
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_espeak_ausente"))
        salvar_historico(arquivo, "Erro - espeak ausente")
        _marcar_falha()
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_audio", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _marcar_falha()


def menu_extras():
    while True:
        escolha = ui.menu_extras()

        if escolha == "epub":
            extra_epub()
        elif escolha == "audio":
            extra_audio()
        elif escolha == "voltar" or escolha is None:
            return

        if escolha not in ("voltar", None):
            questionary.press_any_key_to_continue(ui.t("msg_pressione_continuar")).ask()


# ------------------------------------------------------------------
# Presets
# ------------------------------------------------------------------

def presets_criar():
    nome = ui.perguntar_nome_preset()
    if not nome:
        return
    dados = ui.perguntar_dados_preset()
    ui.salvar_preset(nome, dados)
    ui.print_sucesso(ui.t("presets_criado", nome=nome))


def presets_usar():
    nome = ui.perguntar_escolher_preset()
    if not nome:
        return
    dados = ui.listar_presets().get(nome, {})
    ui.print_painel(nome, "\n".join(f"{k}: {v}" for k, v in dados.items() if v))


def presets_apagar():
    nome = ui.perguntar_escolher_preset()
    if not nome:
        return
    ui.apagar_preset(nome)
    ui.print_sucesso(ui.t("presets_apagado", nome=nome))


def menu_presets():
    while True:
        ui.trilha(ui.t("trilha_menu"), ui.t("trilha_presets"))
        escolha = ui.menu_presets()

        if escolha == "criar":
            presets_criar()
        elif escolha == "usar":
            presets_usar()
        elif escolha == "apagar":
            presets_apagar()
        elif escolha == "voltar" or escolha is None:
            return

        if escolha not in ("voltar", None):
            questionary.press_any_key_to_continue(ui.t("msg_pressione_continuar")).ask()


# ------------------------------------------------------------------
# Estatísticas / Histórico / Desfazer
# ------------------------------------------------------------------

def estatisticas():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_estatisticas"))
    itens = carregar_historico()
    ui.tela_estatisticas(itens)


def ver_historico():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_historico"))
    itens = carregar_historico()
    if not itens:
        ui.print_info(ui.t("historico_vazio"))
        return
    ui.console.print(ui.tabela_historico(itens))


def desfazer_ultima_acao():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_desfazer"))
    ultima = _sessao.get("ultima_saida")
    if not ultima or not os.path.exists(ultima):
        ui.print_info(ui.t("desfazer_nada"))
        return

    if not ui.confirmar_desfazer(ultima):
        ui.print_info(ui.t("operacao_cancelada"))
        return

    try:
        os.remove(ultima)
        ui.print_sucesso(ui.t("desfazer_sucesso", arquivo=os.path.basename(ultima)))
        _sessao["ultima_saida"] = None
    except Exception as e:
        ui.print_erro(ui.t("desfazer_erro", erro=e))


# ------------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------------

def menu():
    while True:
        ui.banner()
        escolha = ui.menu_principal()

        if escolha == "converter":
            menu_converter()
        elif escolha == "ferramentas":
            menu_ferramentas()
        elif escolha == "extras":
            menu_extras()
        elif escolha == "presets":
            menu_presets()
        elif escolha == "estatisticas":
            estatisticas()
        elif escolha == "historico":
            ver_historico()
        elif escolha == "desfazer":
            desfazer_ultima_acao()
        elif escolha == "idioma":
            ui.trilha(ui.t("trilha_menu"), ui.t("trilha_idioma"))
            ui.perguntar_idioma()
        elif escolha == "sair" or escolha is None:
            ui.tela_despedida(_sessao["sucessos"], _sessao["falhas"])
            break

        if escolha in ("estatisticas", "historico", "desfazer", "idioma"):
            questionary.press_any_key_to_continue(ui.t("msg_pressione_voltar")).ask()


if __name__ == "__main__":
    menu()
