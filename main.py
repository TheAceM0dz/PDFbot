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

# Contador de operações da sessão atual, mostrado na tela de despedida
_sessao = {"sucessos": 0, "falhas": 0}


def escolher_saida(arquivo):
    nome_base = os.path.splitext(arquivo)[0]
    padrao = nome_base + ".pdf"
    ui.print_info(ui.t("msg_saida_padrao", caminho=padrao))
    return ui.perguntar_caminho_saida(padrao)


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
            conversores[extensao](arquivo, saida)
        ui.print_sucesso(ui.t("msg_pdf_sucesso", caminho=saida))
        salvar_historico(arquivo, "Sucesso")
        ui.salvar_ultimo_diretorio(saida)
        _sessao["sucessos"] += 1
    except PermissionError:
        ui.print_erro(ui.t("msg_sem_permissao"))
        salvar_historico(arquivo, "Erro - sem permissão")
        _sessao["falhas"] += 1
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_ferramenta_ausente_pandoc"))
        salvar_historico(arquivo, "Erro - ferramenta ausente")
        _sessao["falhas"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_converter", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


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
        _sessao["sucessos"] += 1
    except PermissionError:
        ui.print_erro(ui.t("msg_sem_permissao"))
        salvar_historico(arquivo, "Erro - sem permissão")
        _sessao["falhas"] += 1
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_ferramenta_ausente_poppler"))
        salvar_historico(arquivo, "Erro - ferramenta ausente")
        _sessao["falhas"] += 1
    except ImportError:
        ui.print_erro(ui.t("msg_lib_ausente_docx"))
        salvar_historico(arquivo, "Erro - biblioteca ausente")
        _sessao["falhas"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_converter", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


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
        _sessao["sucessos"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_unir", erro=e))
        salvar_historico(", ".join(caminhos), f"Erro - {e}")
        _sessao["falhas"] += 1


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
        salvar_historico(arquivo, "Sucesso - comprimir")
        ui.salvar_ultimo_diretorio(saida)
        _sessao["sucessos"] += 1
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_ghostscript_ausente"))
        salvar_historico(arquivo, "Erro - ghostscript ausente")
        _sessao["falhas"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_comprimir", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


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
        _sessao["sucessos"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_extrair", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


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
        _sessao["sucessos"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_proteger", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


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
        _sessao["sucessos"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_marca", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


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
        _sessao["sucessos"] += 1
    except FileNotFoundError:
        ui.print_erro(ui.t("msg_tesseract_ausente"))
        salvar_historico(arquivo, "Erro - ferramenta ausente")
        _sessao["falhas"] += 1
    except Exception as e:
        ui.print_erro(ui.t("msg_erro_ocr", erro=e))
        salvar_historico(arquivo, f"Erro - {e}")
        _sessao["falhas"] += 1


def menu_ferramentas():
    while True:
        escolha = ui.menu_ferramentas()

        if escolha == "unir":
            ferramenta_unir()
        elif escolha == "comprimir":
            ferramenta_comprimir()
        elif escolha == "extrair":
            ferramenta_extrair()
        elif escolha == "proteger":
            ferramenta_proteger()
        elif escolha == "marca_dagua":
            ferramenta_marca_dagua()
        elif escolha == "ocr":
            ferramenta_ocr()
        elif escolha == "voltar" or escolha is None:
            return

        if escolha not in ("voltar", None):
            questionary.press_any_key_to_continue(
                ui.t("msg_pressione_continuar")
            ).ask()


def ver_historico():
    ui.trilha(ui.t("trilha_menu"), ui.t("trilha_historico"))
    itens = carregar_historico()
    if not itens:
        ui.print_info(ui.t("historico_vazio"))
        return
    ui.console.print(ui.tabela_historico(itens))


def menu():
    while True:
        ui.banner()
        escolha = ui.menu_principal()

        if escolha == "converter":
            converter_arquivo()
        elif escolha == "de_pdf":
            converter_de_pdf()
        elif escolha == "lote":
            converter_lote()
        elif escolha == "ferramentas":
            menu_ferramentas()
        elif escolha == "historico":
            ver_historico()
        elif escolha == "idioma":
            ui.trilha(ui.t("trilha_menu"), ui.t("trilha_idioma"))
            ui.perguntar_idioma()
        elif escolha == "sair" or escolha is None:
            ui.tela_despedida(_sessao["sucessos"], _sessao["falhas"])
            break

        if escolha in ("converter", "de_pdf", "lote", "historico", "idioma"):
            questionary.press_any_key_to_continue(
                ui.t("msg_pressione_voltar")
            ).ask()


if __name__ == "__main__":
    menu()
