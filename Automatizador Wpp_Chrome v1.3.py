#Programa com 4 inputs do usuário:
#  1- nome do arquivo, sem a extensão, imaginando que sempre será .CSV
#  2, 3 e 4 - Mensagem, divida em 3 partes, que será enviada ao usuário. (O programa irá trocar a palavra 'fulano' pelo nome do destinatário)
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
import pandas as pd
import random

#Auto install para o chromedriver
servico = Service(ChromeDriverManager().install())

#Configurando navegador por um perfil, para evitar QR Scan o tempo todo 
opcoes = webdriver.ChromeOptions()
opcoes.add_argument(r'user-data-dir=C:\Users\mateu\AppData\Local\Google\Chrome\User Data\Profile Selenium')

#Iniciando navegador...
navegador = webdriver.Chrome(service=servico, options=opcoes)


def carregar_wpp():    
    navegador.get("https://web.whatsapp.com")
    
    # esperar a tela do whatsapp carregar
    while len(navegador.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
        time.sleep(1)
    print("Tela do Whatsapp carregada com sucesso! Esperando 5 segundos, por garantia...")
    #time.sleep(5) # só uma garantia
    tempo_espera(5)

def carregar_planilha():
    janela = Tk()
    arquivo = tkinter.filedialog.askopenfilename(title = 'Escolha o arquivo CSV que queira utilizar')
    janela.destroy()
    #encoding = 'ISO-8859-1'
    tabela = pd.read_csv(arquivo, sep=',')
    tabela = tabela[["Nome Fantasia", "Razão Social", "Todos os telefones extras (exceto de contador)"]]
    
    #preenchendo valores nulos com 'vazio'
    tabela["Nome Fantasia"] = tabela["Nome Fantasia"].fillna('vazio')
    tabela["Razão Social"] = tabela["Razão Social"].fillna('vazio')
    
    #Acrescentando uma linha ao topo da DF ----->>>> Criar função para linha de teste
    opcao_teste = input("Deseja criar uma linha de testes, com dois números? (s/n) ").lower()
    if opcao_teste == 's':
        tabela = linha_teste_planilha(tabela)   
    
    print("Aqui está a tabela simplificada para verificação: ")
    print(tabela)
    return tabela


def linha_teste_planilha(tabela):
    num1 = input("Digite o primeiro numero: ")
    num2 = input("Digite o segundo numero (pode ser o mesmo do primeiro) : ")
    linha_teste = ['vazio', 'vazio', f'{num1}, {num2}']
    tabela = tabela.transpose()
    tabela.insert(0, "0", linha_teste)
    tabela = tabela.transpose()
    tabela.reset_index(drop=True, inplace=True)
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


def esperar_tela_principal():    
    # esperar a tela do whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
    print("ESPERANDO TELA PRINCIPAL...")
    elemento = WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.ID, "pane-side"))) #60s é o tempo maximo de espera
    print("Esperando 5s por garantia...")
    #time.sleep(5)
    tempo_espera(5)
    

def envia_mensagem(vai_mudar_contato=True):
    navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click()
    vamos_esperar = 10
    if vai_mudar_contato:
        #espera segundos aleatórios entre uma mensagem e outra, caso alguma mensagem seja enviada
        vamos_esperar = random.randint(20, 45)
        print(f"Cronos: Esperando {vamos_esperar} segundos antes de iniciar as mensagens do próximo contato...")
    else:
        print(f"Cronos: Esperando {vamos_esperar} segundos antes de iniciar a próxima mensagem para esse contato...")
    #time.sleep(vamos_esperar)    
    tempo_espera(vamos_esperar)
    

def tempo_espera(tempo):
    for i in range(tempo, 0, -1):
        print(f"Tempo restante: {i} segundos", end='\r')  # \r para sobrescrever a linha anterior
        time.sleep(1)  # Espera 1 segundo

def main():
    carregar_wpp()
    # o whatsapp já carregou
    tabela = carregar_planilha()
    mensagem_cumprimentos = input("Digite a mensagem de cumprimentos (a palavra 'fulano' será trocada pelo nome do destinatário): ")
    mensagem_template_1 = definir_mensagem('Parte 1')
    mensagem_template_2 = definir_mensagem('Parte 2')
  
    qntd_num_invalidos = 0
    qntd_msg_enviadas = 0

    #Percorrendo a planilha, tratando os dados para criar nomes e seus respectivos contatos
    for linha in tabela.index:
        nome = definir_nome(tabela, linha)
        lista_telefones = definir_lista_telefones(tabela, linha)
        #definir mensagem de cumprimentos
        mensagem = modificar_mensagem(nome, mensagem_cumprimentos)
        texto_link_cumprimentos = mensagem_to_link(mensagem)
        #definir mensagem do meio
        mensagem = modificar_mensagem(nome, mensagem_template_1)
        texto_link_parte_1 = mensagem_to_link(mensagem)
        #definir mensagem final
        mensagem = modificar_mensagem(nome, mensagem_template_2)
        texto_link_parte_2 = mensagem_to_link(mensagem)

        #Percorrendo a lista de telefones do contato atual
        for num_tel in lista_telefones:            
            link_cumprimentos = definir_link_mensagem(num_tel, texto_link_cumprimentos)
            link_parte_1 = definir_link_mensagem(num_tel, texto_link_parte_1)
            link_parte_2 = definir_link_mensagem(num_tel, texto_link_parte_2)
            print(link_cumprimentos)
            navegador.get(link_cumprimentos)
            esperar_tela_principal()
            
            #Try / Except => Para verificar se exite uma tela de número URL invalido. Caso o número seja inválido, não faz nada e passa pro próximo número.
            timeout = 10
            print("Esperando 10 segundos pela presença de um alerta de número inválido, por precaução...")
            try:
                tela_invalida = WebDriverWait(navegador, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'))
                )
                # Se o elemento (janela de url inválida) for encontrado, adiciona à contagem e não faça nada
                print("Janela de numero invalido detectada!! Ignorando numero e passando para o próximo da lista...")
                time.sleep(2) #Para que o usuário tenha tempo de ler essa última mensagem
                qntd_num_invalidos += 1
                pass
            
            except:
                # Se o elemento não for encontrado dentro do tempo limite, envie uma mensagem
                print("A tela de número inválido NÃO apareceu. Enviando mensagem...")
                envia_mensagem(vai_mudar_contato=False)                
                print(link_parte_1)
                navegador.get(link_parte_1)
                esperar_tela_principal()
                envia_mensagem(vai_mudar_contato=False)
                print(link_parte_2)
                navegador.get(link_parte_2)
                esperar_tela_principal()
                envia_mensagem()
                qntd_msg_enviadas += 1
    janela = Tk()
    messagebox.showinfo('Relatório', f'Foram enviadas mensagens para {qntd_msg_enviadas} números diferentes.\nForam encontrados {qntd_num_invalidos} números inválidos.')
    janela.destroy()

if __name__ == "__main__":
    main()

