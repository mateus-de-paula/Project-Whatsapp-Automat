#Programa com 2 inputs do usuário:
#  1- nome do arquivo, sem a extensão, imaginando que sempre será .CSV
#  2- Mensagem que será enviada ao usuário. (O programa irá trocar a palavra 'fulano' pelo nome do destinatário)
#Necessário baixar o driver do navegador Firefox:
# https://github.com/mozilla/geckodriver/releases
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib
import os
import pandas as pd
import random

navegador = webdriver.Firefox()

def carregar_wpp():    
    navegador.get("https://web.whatsapp.com")
    
    # esperar a tela do whatsapp carregar
    while len(navegador.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
        time.sleep(1)
    time.sleep(5) # só uma garantia


def carregar_planilha(nome_arquivo):
    tabela = pd.read_csv(f"{nome_arquivo}.csv", sep=',')
    tabela = tabela[["Nome Fantasia", "Razão Social", "Todos os telefones extras (exceto de contador)"]]
    #preenchendo valores nulos com 'vazio'
    tabela["Nome Fantasia"] = tabela["Nome Fantasia"].fillna('vazio')
    tabela["Razão Social"] = tabela["Razão Social"].fillna('vazio')
    #Acrescentando uma linha ao topo da DF
    tabela = tabela.transpose()
    tabela.insert(0, "0", ['vazio', 'Zindé', '31994455666, 31994455666'])
    tabela = tabela.transpose()
    tabela.reset_index(drop=True, inplace=True)
    print("Aqui está a tabela simplificada para verificação: ")
    print(tabela)
    return tabela

def definir_nome(tabela, linha):
    nome = tabela.loc[linha, "Nome Fantasia"].strip()
    if nome == 'vazio':
        nome = tabela.loc[linha, "Razão Social"].strip()
        #removendo certos detalhes do nome
        if 'LTDA' in nome:
            nome = nome[:-5]
        if 'S/A' in nome:
            nome = nome[:-4]
        if 'EIRELI' in nome:
            nome = nome[:-7] 
        #Verifica se começa ou termina com CPF, e os remove do nome
        if nome[-11:].isnumeric():
            nome = nome[:-12]
        if nome[:11].isnumeric():
            nome = nome[12:]
        #Verifica se começa com sequencia de números to tipo XX.XXX.XXX
        if nome[:10].replace('.','').isnumeric():
            nome = nome[11:]
    return nome

def definir_lista_telefones(tabela, linha):
    telefone = tabela.loc[linha, "Todos os telefones extras (exceto de contador)"]
    return str(telefone).split(', ')


def definir_mensagem(parte):
    return input(f"Digite a mensagem ({parte}) (a palavra 'fulano' será trocada pelo nome do destinatário): ")


def modificar_mensagem(nome, mensagem_template):
    return mensagem_template.replace("fulano", nome)


def mensagem_to_link(mensagem):
    return urllib.parse.quote(mensagem)


def definir_anexo():
    pass


def definir_link_mensagem(num_tel, texto_link):
    print(num_tel, texto_link)
    return f"https://web.whatsapp.com/send?phone={num_tel}&text={texto_link}"


def esperar_tela_principal(cont):    
    # esperar a tela do whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
    # -> lista for vazia -> que o elemento não existe ainda
    print("ESPERANDO TELA PRINCIPAL...")
    while len(navegador.find_elements(By.ID, "pane-side")) < 1:
        time.sleep(1)
    if cont == 1:
        print("Esperando 45s, por ser a primeira mensagem de todas. (As vezes ela demora para carregar) X_( ...")
        time.sleep(45)
        print("Esperando mais 5s... Só pra garantir! :D")
    else:
        print("Esperando 5s...")
    time.sleep(5)


def envia_mensagem(vai_mudar_contato=True):
    navegador.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]').click()
    vamos_esperar = 10
    if vai_mudar_contato:
        #espera segundos aleatórios entre uma mensagem e outra, caso alguma mensagem seja enviada
        vamos_esperar = random.randint(20, 45)
        print(f"Cronos: Esperando {vamos_esperar} segundos antes de iniciar as mensagens do próximo contato...")
    else:
        print(f"Cronos: Esperando {vamos_esperar} segundos antes de iniciar a próxima mensagem...")
    time.sleep(vamos_esperar)    


def main():
    carregar_wpp()
    # o whatsapp já carregou
    nome_arquivo = input("Digite o nome do arquivo (sem a extensão) :") #teste: "restaurantes-lead-nata-Zap-full"
    tabela = carregar_planilha(nome_arquivo)
    mensagem_cumprimentos = input("Digite a mensagem de cumprimentos (a palavra 'fulano' será trocada pelo nome do destinatário): ")
    mensagem_template_1 = definir_mensagem('Parte 1')
    mensagem_template_2 = definir_mensagem('Parte 2')
    #Tratando os dados
    cont = 0
    qntd_num_invalidos = 0
    qntd_msg_enviadas = 0
    for linha in tabela.index:
        nome = definir_nome(tabela, linha)
        lista_telefones = definir_lista_telefones(tabela, linha)
        #definir mensagem de cumprimentos
        mensagem = modificar_mensagem(nome, mensagem_cumprimentos)
        texto_link_cumprimentos = mensagem_to_link(mensagem)
        mensagem = modificar_mensagem(nome, mensagem_template_1)
        texto_link_parte_1 = mensagem_to_link(mensagem)
        mensagem = modificar_mensagem(nome, mensagem_template_2)
        texto_link_parte_2 = mensagem_to_link(mensagem)
        for num_tel in lista_telefones:
            cont += 1
            link_cumprimentos = definir_link_mensagem(num_tel, texto_link_cumprimentos)
            link_parte_1 = definir_link_mensagem(num_tel, texto_link_parte_1)
            link_parte_2 = definir_link_mensagem(num_tel, texto_link_parte_2)
            print(link_cumprimentos)
            navegador.get(link_cumprimentos)
            esperar_tela_principal(cont)
            #Try / Except => Para verificar se exite uma tela de número URL invalido. Caso o número seja inválido, não faz nada e passa pro próximo número.
            timeout = 10
            try:
                tela_invalida = WebDriverWait(navegador, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[1]"))
                )
                # Se o elemento (janela de url inválida) for encontrado, adiciona à contagem e não faça nada
                qntd_num_invalidos += 1
                pass
            
            except:
                # Se o elemento não for encontrado dentro do tempo limite, envie uma mensagem
                print("A tela de número inválido NÃO apareceu. Enviando mensagem...")
                envia_mensagem(vai_mudar_contato=False)
                cont += 1
                print(link_parte_1)
                navegador.get(link_parte_1)
                esperar_tela_principal(cont)
                envia_mensagem(vai_mudar_contato=False)
                print(link_parte_2)
                navegador.get(link_parte_2)
                esperar_tela_principal(cont)
                envia_mensagem()
                qntd_msg_enviadas += 1
    print(f"Foram enviadas mensagens para {qntd_msg_enviadas} números diferentes.")
    print(f"Foram encontrados {qntd_num_invalidos} números inválidos.")

if __name__ == "__main__":
    main()

