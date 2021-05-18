import pdfplumber
import requests
import re
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

url = 'https://app.organizze.com.br/zze_front/transactions'

headers = {"X-Auth-Token": "TOKEN",
           "Current-Entity-Id": "ID", "Content-Type": "application/json;charset=UTF-8"}

account_uuid = 'UUID'


def addTransacao(data_transacao, ativos):

    for ativo in ativos:
        if (ativo["nome"] == 'TAXAS'):
            requisicaoTaxas(data_transacao, ativo["valor"])

        else:
            requisicao(data_transacao, ativo["tipo"], ativo["nome"],
                       ativo["qtd"], ativo["preco"])


def requisicaoTaxas(data_transacao, preco_ativo):

    tag_uuid = 'UUID'

    data = '{\"transaction\": {\"amount\": '+preco_ativo+', \"activity_type\": 0, \"done\": 1, \"times\": 2, \"date\": \"'+data_transacao+'\", \"finite_periodicity\": \"monthly\", \"infinite_periodicity\": \"monthly\", \"attachments_attributes\": {}, \"account_uuid\": \"'+account_uuid+'\", \"description\": \"TAXAS\", \"tag_uuid\": \"' + \
        tag_uuid + '\", \"observation\": \"\", \"joined_tags\": \"\", \"finite\": false, \"infinite\": false}, \"installmentValue\": \"R$ 0, 61\", \"isCreditCardSelected\": false}'

    response = requests.post(url, headers=headers, data=data, verify=False)
    response_dictionary = response.json()
    print(response_dictionary)


def requisicao(data_transacao, activity_type, nome_ativo, qtd_ativo, preco_ativo,):

    preco_transacao = str(float(qtd_ativo) * float(preco_ativo))

    tag_uuid = 'UUID'

    if activity_type == 'V':
        activity_type = '1'
        tag_uuid = 'UUID'
    else:
        activity_type = '0'

    data = '{\"transaction\": {\"amount\": '+preco_transacao+', \"activity_type\": '+activity_type+', \"done\": 1, \"times\": 2, \"date\": \"'+data_transacao+'\", \"finite_periodicity\": \"monthly\", \"infinite_periodicity\": \"monthly\", \"attachments_attributes\": {}, \"account_uuid\": \"'+account_uuid+'\", \"description\": \"' + \
        nome_ativo+' - '+qtd_ativo + \
        ' ['+preco_ativo+']\", \"tag_uuid\": \"'+tag_uuid + \
        '\", \"observation\": \"\", \"joined_tags\": \"\", \"finite\": false, \"infinite\": false}, \"installmentValue\": \"R$ 0, 61\", \"isCreditCardSelected\": false}'

    response = requests.post(url, headers=headers, data=data, verify=False)
    response_dictionary = response.json()
    print(response_dictionary)


with pdfplumber.open("rico.pdf", password="XXX") as pdf:
    pagina = pdf.pages[0]
    pagina_texto = pagina.extract_text()

    data_transacao = ''
    valor_com_taxas = ''
    valor_sem_taxas = ''
    ativos = []

    for linha in pagina_texto.split("\n"):

        ativo = {}

        if linha.find('/') == 12:
            match = re.search(r'\d{2}\/\d{2}\/\d{4}', linha)
            datas = match.group().split("/")
            data_transacao = "-".join(datas[::-1])

        if linha.startswith("Líquido"):
            match = re.search(r'\d*\.*\d+\,\d{2}', linha)
            valor_com_taxas = float(
                match.group().replace(".", "").replace(",", "."))

        if linha.startswith("Vendas à vista"):
            match = re.findall(r'\d*\.*\d+\,\d{2}', linha)
            valor_sem_taxas = float(
                match[1].replace(".", "").replace(",", "."))

        if linha.startswith("1-BOVESPA"):
            linha_elementos = (linha.split())

            tipo_transacao = linha_elementos[1]
            nome_ativo = linha_elementos[3]

            ativo["tipo"] = tipo_transacao
            ativo["nome"] = nome_ativo

            for i in range(6, len(linha_elementos)):
                try:
                    int(linha_elementos[i])
                except:
                    continue

                qtd_ativo = linha_elementos[i]
                preco_ativo = linha_elementos[i+1].replace(",", ".")
                ativo["qtd"] = qtd_ativo
                ativo["preco"] = preco_ativo

        if (ativo.keys()):
            ativos.append(ativo)

    taxa = {"nome": "TAXAS", "valor": format(
        valor_com_taxas - valor_sem_taxas, '.2f')}
    ativos.append(taxa)

    addTransacao(data_transacao, ativos)
    #print(data_transacao, ativos)
