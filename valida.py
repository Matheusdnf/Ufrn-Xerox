import re
from telas import menu_meses


def verifica_ano(ano):
    padrao_ano = r"^(20\d{2})$"
    match = re.match(padrao_ano, ano)
    if not match:
        return False
    return ano

    
def verifica_mes(mes):
    meses_dict = {
        "01": "01-JANEIRO", "02": "02-FEVEREIRO", "03": "03-MARÇO", "04": "04-ABRIL",
        "05": "05-MAIO", "06": "06-JUNHO", "07": "07-JULHO", "08": "08-AGOSTO",
        "09": "09-SETEMBRO", "10": "10-OUTUBRO", "11": "11-NOVEMBRO", "12": "12-DEZEMBRO"
    }
    padrao_mes = r"^(0[1-9]|1[0-2])$"
    match = re.match(padrao_mes, mes)
    if not match:
        return False
    else:
        mes_num = match.group()
        return meses_dict[mes_num]

def entrada_ano():
    while True:
        ano = input("Digite o ano (ex: 2023): ")
        if not verifica_ano(ano):
            print("Ano inválido! Digite um ano no formato 20XX.")
        else:
            return ano

def entrada_mes():
    menu_meses()
    while True:
        entrada_mes = input("Digite o mês: ")
        if entrada_mes == "0":
            return "0"
        if not verifica_mes(entrada_mes):
            print("Mês inválido! Digete o número que corresponde ao mês!.")
        else:
            mes = verifica_mes(entrada_mes)
            return mes

