import json
import datetime

import requests

from .validate import check_pagador, check_desconto, check_multa, check_mora


class ApiInter:
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def __init__(self, numero_conta, cert_crt, cert_key):
        self.NUMERO_CONTA = numero_conta
        self.CERT_CRT = cert_crt
        self.CERT_KEY = cert_key
        self._URL_BOLETOS = "https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos"
        self._DEFAULT_HEADERS = {
            "x-inter-conta-corrente": self.NUMERO_CONTA
        }
        self.check_pagador = check_pagador
        self.check_desconto = check_desconto

    def _default_response(self, r, json=True):
        if r.status_code == 200:
            if json:
                return r.json()
            else:
                return r
        elif r.status_code == 400:
            return {
                "code": 400,
                "msg": r.json(),
            }
        elif r.status_code == 500:
            return {
                "code": 500,
                "msg": "Serviço indisponivel",
            }
        else:
            response = {
                "code": r.status_code,
                "response": r
            }
            # if r.json()["message"]:
            #     response["msg"] = r.json().message
            return r

    def get_boletos(self, data_inicial=datetime.date.today(), data_final=datetime.date.today()):
        params = {
            "dataInicial": data_inicial,
            "dataFinal": data_final,
        }

        r = requests.get(
            url=self._URL_BOLETOS,
            params=params,
            verify=False,
            cert=[self.CERT_CRT, self.CERT_KEY],
            headers=self._DEFAULT_HEADERS
        )

        return r

    def emitir_boleto(self, valor_nominal, cnpj_cpf_beneficiario, num, desconto1=None, valor_abatimento=0,
                      desconto2=None, desconto3=None, num_dias_agenda="SESSENTA", data_emissao=datetime.date.today(),
                      mensagem=None, multa=None, mora=None, pagador=None,
                      data_vencimento=datetime.date.today() + datetime.timedelta(days=1)):

        if mora is None:
            mora = {
                "codigoMora": "ISENTO",
                "valor": 0,
                "taxa": 0
            }
        if multa is None:
            multa = {
                "codigoMulta": "NAOTEMMULTA",
                "valor": 0,
                "taxa": 0
            }
        if pagador is None:
            pagador = {}

        check_pagador(pagador)

        data_limite = num_dias_agenda

        data = {}
        data["pagador"] = pagador
        data["dataEmissao"] = data_emissao.strftime("%Y-%m-%d")
        data["seuNumero"] = num
        data["dataLimite"] = data_limite
        data["dataVencimento"] = data_vencimento.strftime("%Y-%m-%d")
        if mensagem is not None:
            data["mensagem"] = mensagem
        data["desconto1"] = desconto1
        if desconto1 is None:
            data["desconto1"] = {
                "codigoDesconto": "NAOTEMDESCONTO",
                "taxa": 0,
                "valor": 0,
                "data": "",
            }
        data["desconto2"] = desconto2
        if desconto2 is None:
            data["desconto2"] = {
                "codigoDesconto": "NAOTEMDESCONTO",
                "taxa": 0,
                "valor": 0,
                "data": "",
            }
        data["desconto3"] = desconto3
        if desconto3 is None:
            data["desconto3"] = {
                "codigoDesconto": "NAOTEMDESCONTO",
                "taxa": 0,
                "valor": 0,
                "data": "",
            }

        check_desconto(desconto1)
        check_desconto(desconto2)
        check_desconto(desconto3)
        check_multa(multa)
        check_mora(mora)

        data["valorNominal"] = valor_nominal
        data["valorAbatimento"] = valor_abatimento
        data["multa"] = multa
        data["mora"] = mora
        data["cnpjCPFBeneficiario"] = cnpj_cpf_beneficiario
        data["numDiasAgenda"] = num_dias_agenda

        headers = self._DEFAULT_HEADERS
        headers["accept"] = "application/json"
        headers["content-type"] = "application/json"
        r = requests.post(
            url=self._URL_BOLETOS,
            data=json.dumps(data),
            verify=False,
            cert=[self.CERT_CRT, self.CERT_KEY],
            headers=self._DEFAULT_HEADERS
        )

        return r

    def get_pdf(self, nosso_numero):
        url = f"https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos/{nosso_numero}/pdf"
        print(url)

        r = requests.get(
            url=url,
            verify=False,
            cert=[self.CERT_CRT, self.CERT_KEY],
            headers=self._DEFAULT_HEADERS
        )

        return r
