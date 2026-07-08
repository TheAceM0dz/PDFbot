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


def escolher_saida(arquivo):
    nome_base = os.path.splitext(arquivo)[0]
    padrao = nome_base + ".pdf"
    ui.print_info(f"Saída padrão: {padrao}")
    return ui.perguntar_caminho_saida(padrao)


def converter_arquivo():
    arquivo = ui.perguntar_caminho_arquivo()

    if not arquivo:
        ui.print_erro("Nenhum caminho informado.")
        return

    if not arquivo_existe(arquivo):
        ui.print_erro("Arquivo não existe.")
        salvar_historico(arquivo, "Erro - arquivo não existe")
        return

    if arquivo_vazio(arquivo):
        ui.print_erro("Arquivo está vazio.")
        salvar_historico(arquivo, "Erro - arquivo vazio")
        return

    extensao = obter_extensao(arquivo)
    ui.print_info(f"Extensão detectada: {extensao}")

    if not extensao_compativel(extensao):
        ui.print_erro("Formato não compatível.")
        salvar_historico(arquivo, "Erro - formato não compatível")
        return

    saida = escolher_saida(arquivo)

    pasta_saida = os.path.dirname(saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        ui.print_erro("A pasta de destino não existe.")
        salvar_historico(arquivo, "Erro - pasta de destino não existe")
        return

    try:
        with ui.console.status("[bold cyan]Convertendo...[/bold cyan]", spinner="dots"):
            conversores[extensao](arquivo, saida)
        ui.print_sucesso(f"PDF criado com sucesso: {saida}")
        salvar_historico(arquivo, "Sucesso")
        ui.salvar_ultimo_diretorio(saida)
    except PermissionError:
        ui.print_erro("Sem permissão pra ler ou escrever o arquivo.")
        salvar_historico(arquivo, "Erro - sem permissão")
    except FileNotFoundError:
        ui.print_erro("Alguma ferramenta necessária (ex: pandoc) não foi encontrada.")
        salvar_historico(arquivo, "Erro - ferramenta ausente")
    except Exception as e:
        ui.print_erro(f"Erro ao converter: {e}")
        salvar_historico(arquivo, f"Erro - {e}")


def converter_de_pdf():
    arquivo = ui.perguntar_caminho_arquivo()

    if not arquivo:
        ui.print_erro("Nenhum caminho informado.")
        return

    if not arquivo_existe(arquivo):
        ui.print_erro("Arquivo não existe.")
        salvar_historico(arquivo, "Erro - arquivo não existe")
        return

    if arquivo_vazio(arquivo):
        ui.print_erro("Arquivo está vazio.")
        salvar_historico(arquivo, "Erro - arquivo vazio")
        return

    if not eh_pdf(arquivo):
        ui.print_erro("Esse arquivo não é um PDF.")
        salvar_historico(arquivo, "Erro - não é PDF")
        return

    formato_destino = ui.perguntar_formato_destino()
    if not formato_destino:
        ui.print_erro("Nenhum formato de destino escolhido.")
        return

    nome_base = os.path.splitext(arquivo)[0]
    padrao = nome_base + formato_destino
    ui.print_info(f"Saída padrão: {padrao}")
    saida = ui.perguntar_caminho_saida(padrao)

    pasta_saida = os.path.dirname(saida)
    if pasta_saida and not os.path.exists(pasta_saida):
        ui.print_erro("A pasta de destino não existe.")
        salvar_historico(arquivo, "Erro - pasta de destino não existe")
        return

    try:
        with ui.console.status("[bold cyan]Convertendo...[/bold cyan]", spinner="dots"):
            conversores_de_pdf[formato_destino](arquivo, saida)
        ui.print_sucesso(f"Arquivo criado com sucesso: {saida}")
        salvar_historico(arquivo, "Sucesso")
        ui.salvar_ultimo_diretorio(saida)
    except PermissionError:
        ui.print_erro("Sem permissão pra ler ou escrever o arquivo.")
        salvar_historico(arquivo, "Erro - sem permissão")
    except FileNotFoundError:
        ui.print_erro(
            "Alguma ferramenta necessária não foi encontrada "
            "(instale com: pkg install poppler)."
        )
        salvar_historico(arquivo, "Erro - ferramenta ausente")
    except ImportError:
        ui.print_erro(
            "Falta uma biblioteca pra essa conversão "
            "(instale com: pip install python-docx)."
        )
        salvar_historico(arquivo, "Erro - biblioteca ausente")
    except Exception as e:
        ui.print_erro(f"Erro ao converter: {e}")
        salvar_historico(arquivo, f"Erro - {e}")


def ver_historico():
    itens = carregar_historico()
    if not itens:
        ui.print_info("Nenhuma conversão registrada ainda.")
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
        elif escolha == "historico":
            ver_historico()
        elif escolha == "sair" or escolha is None:
            ui.console.print("\n[bold magenta]Até mais! 👋[/bold magenta]\n")
            break

        if escolha in ("converter", "de_pdf", "historico"):
            questionary.press_any_key_to_continue(
                "Pressione qualquer tecla para voltar ao menu..."
            ).ask()


if __name__ == "__main__":
    menu()
