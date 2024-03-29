#!/bin/python3
# Adicionar operações CRIPTO ao Organizze

import requests
import organizze

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'


def addCripto(tipo, nome_ativo, unidades, valor, data_transacao):
    valor = str(round(float(valor), 2))
    preco_transacao = str(float(unidades) * float(valor))

    if tipo == '0':
        tag_uuid = organizze.tags['despesa_cripto']
        activity_type = organizze.activity_type['despesa']
    elif tipo == '1':
        tag_uuid = organizze.tags['receita_cripto']
        activity_type = organizze.activity_type['receita']
    else:
        return #TODO tipo 2, tem que fazer compra e venda do ativo, seriam 2 requests

    data = '{\"transaction\": {\"amount\": '+preco_transacao+', \"activity_type\": '+activity_type+', \"done\": 1, \"times\": 2, \"date\": \"'+data_transacao+'\", \"finite_periodicity\": \"monthly\", \"infinite_periodicity\": \"monthly\", \"attachments_attributes\": {}, \"account_uuid\": \"'+organizze.account_uuid['corretora_cripto']+'\", \"description\": \"' + \
        nome_ativo+' - '+unidades + \
        ' ['+valor+']\", \"tag_uuid\": \"'+tag_uuid + \
        '\", \"observation\": \"\", \"joined_tags\": \"\", \"finite\": false, \"infinite\": false}, \"installmentValue\": \"R$ 0, 61\", \"isCreditCardSelected\": false}'

    response = requests.post(
        organizze.url, headers=organizze.headers, data=data, verify=False)
    response_dictionary = response.json()
    print(response_dictionary)
    # print(data)


def menuCripto():
    data = input('Data (31/12): ')
    data = data + '/2022'
    qtd_operacoes = input(
        'Quantas operações deseja inserir para esta mesma data?: ')
    for i in range(int(qtd_operacoes)):
        tipo = input('Tipo (0 - Compra; 1 - Venda; 2 - Conversão): ')
        if(tipo == '2'):
            moeda_origem_qtd = input(
                'Quantidade da moeda de Origem (0,1234): ')
            moeda_origem_qtd = moeda_origem_qtd.replace(',', '.')
            moeda_origem_cotacao = input(
                'Cotação da moeda de Origem (235140,96): ')
            moeda_origem_cotacao = moeda_origem_cotacao.replace(',', '.')
            unidades = input('Quantidade da moeda de Destino (0,1234): ')
            unidades = unidades.replace(',', '.')
            nome_ativo = input('Nome do ativo de Destino (BTC): ')
            valor = str(round(
                ((float(moeda_origem_qtd)*float(moeda_origem_cotacao))/float(unidades)), 10))
            valor = valor.replace(',', '.')

        else:
            nome_ativo = input('Nome do ativo (BTC): ')
            valor = input('Cotação (235140,96): ')
            valor = valor.replace(',', '.')
            unidades = input('Quantidade (0,1234): ')
            unidades = unidades.replace(',', '.')

        if (len(tipo) < 1 or len(nome_ativo) < 1 or len(unidades) < 1 or len(valor) < 1 or len(data) < 1):
            print('\n--- Valor vazio! ---\n')
            return
        else:
            addCripto(tipo, nome_ativo.upper(), unidades, valor, data)
            print('-----------------------------------')


def main():
    while True:
        menuCripto()


if __name__ == "__main__":
    main()
