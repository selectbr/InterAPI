from datetime import datetime
from .Exceptions import *

_UF = {"RO", "AC", "AM", "RR", "PA", "AP", "TO", "MA", "PI", "CE", "RN", "PB", "PE", "AL",
       "SE", "BA", "MG", "ES", "RJ", "SP", "PR", "SC", "RS", "MS", "MT", "GO", "DF"}

_CODIGOS_DESCONTO = {"NAOTEMDESCONTO", "VALORFIXODATAINFORMADA", "PERCENTUALDATAINFORMADA",
                     "VALORANTECIPACAODIACORRIDO", "VALORANTECIPACAODIAUTIL", "PERCENTUALVALORNOMINALDIACORRIDO",
                     "PERCENTUALVALORNOMINALDIAUTIL"}

_CODIGOS_MULTA = {"NAOTEMMULTA", "VALORFIXO", "PERCENTUAL"}

_CODIGOS_MORA = {"VALORDIA", "TAXAMENSAL", "ISENTO"}

_TIPO_PESSOA = {"FISICA", "JURIDICA"}


def check_date(date):
    if isinstance(date, datetime):
        return True
    return False


def check_pagador(pagador=None):
    if pagador is None:
        return PagadorInvalido("Pagador vázio")

    if not pagador["tipoPessoa"]:
        raise PagadorInvalido("tipoPessoa não definido")

    if not pagador["nome"]:
        raise PagadorInvalido("nome não definido")

    if not pagador["endereco"]:
        raise PagadorInvalido("endereço não definido")

    if not pagador["numero"]:
        raise PagadorInvalido("numero não definido")

    if not pagador["bairro"]:
        raise PagadorInvalido("bairro não definido")

    if not pagador["cidade"]:
        raise PagadorInvalido("cidade não definido")

    if not pagador["uf"]:
        raise PagadorInvalido("uf não definido")

    if not pagador["cep"]:
        raise PagadorInvalido("cep não definido")

    if not pagador["cnpjCpf"]:
        raise PagadorInvalido("cnpjCpf não definido")

    if (len(pagador["nome"]) > 100
            or len(pagador["endereco"]) > 90
            or len(pagador["numero"]) > 10
            or len(pagador["complemento"]) > 30
            or len(pagador["bairro"]) > 60
            or len(pagador["cidade"]) > 60
            or len(pagador["cep"]) > 8
            or len(pagador["cnpjCpf"]) > 15
            or len(pagador["email"]) > 50
            or len(pagador["ddd"]) > 2
            or len(pagador["telefone"]) > 9):
        raise PagadorInvalido("Muitos caracteres")

    if pagador["tipoPessoa"] not in _TIPO_PESSOA:
        raise PagadorInvalido(f"tipoPessoa invalido, valores aceitos: {_TIPO_PESSOA.__str__()}")

    if not pagador["uf"].upper() in _UF:
        raise PagadorInvalido(f"ud invalido, valores aceitos: {_UF.__str__()}")


def check_mensagem(mensagem=None):
    if mensagem is not None:
        if len(mensagem) > 5:
            raise MuitasLinhas("Maximo de linhas 5")

        for m in mensagem:
            if len(m) > 78:
                raise MuitosCaracteres("Máximo de caracteres 78")


def check_desconto(desconto=None):
    if desconto is None:
        raise DescontoInvalido("Desconto vazio")

    if desconto["codigoDesconto"] not in _CODIGOS_DESCONTO:
        message = f"codigoDesconto invalido, valores aceitos: {_CODIGOS_DESCONTO.__str__()}"
        raise DescontoInvalido(message)

    if desconto["codigoDesconto"] in ('VALORFIXODATAINFORMADA', 'PERCENTUALDATAINFORMADA'):
        if not check_date(desconto["data"]):
            raise DescontoInvalido("formato de data invalido")
        if "data" in desconto:
            raise DescontoInvalido(f"data não pode ser nula quando codigoDesconto = {desconto['codigoDesconto']}")
    elif desconto["codigoDesconto"] == "NAOTEMDESCONTO":
        if "data" in desconto and desconto["data"] != "":
            raise DescontoInvalido(f"data deve ser vázia quando codigoDesconto = {desconto['codigoDesconto']}")
        if desconto["taxa"] != 0:
            raise DescontoInvalido(f"taxa deve ser 0 quando codigoDesconto = {desconto['codigoDesconto']}")
    elif desconto["codigoDesconto"] not in ('VALORFIXODATAINFORMADA', 'PERCENTUALDATAINFORMADA', 'NAOTEMDESCONTO'):
        if "data" in desconto:
            raise DescontoInvalido(f"não se deve informar data quando codigoDesconto = {desconto['codigoDesconto']}")

    if desconto["codigoDesconto"] in ('PERCENTUALDATAINFORMADA', 'PERCENTUALVALORNOMINALDIACORRIDO',
                                      'PERCENTUALVALORNOMINALDIAUTIL'):
        if "taxa" in desconto:
            raise DescontoInvalido(f"taxa obrigatoria quando codigoDesconto = {desconto['codigoDesconto']}")


def check_multa(multa=None, vencimento=None):
    if multa is None:
        raise MultaInvalida("multa não pode ser vazia")
    if vencimento is None:
        MultaInvalida("informe o vencimento")

    if multa["codigoMulta"] not in _CODIGOS_MULTA:
        raise MultaInvalida(f"codigoMulta invalido, valores aceitos: {_CODIGOS_MULTA.__str__()}")

    if multa["codigoMulta"] in ("VALORFIXO", "PERCENTUAL"):
        if not check_date(multa["data"]):
            raise MultaInvalida("formato de data invalido")
        if not multa["data"]:
            raise MultaInvalida(f"data obrigatoria quando codigoMulta = {multa['codigoMulta']}")
        if multa["data"] <= vencimento:
            raise MultaInvalida(f"data não pode ser menor ou igual ao vencimento")

        if multa["codigoMulta"] == "PERCENTUAL":
            if not multa["taxa"]:
                raise MultaInvalida(f"taxa precisa ser definada quando codigoMulta = {multa['codigoMulta']}")
        else:
            if not multa["valor"]:
                raise MultaInvalida(f"valor precisa ser definada quando codigoMulta = {multa['codigoMulta']}")
    else:
        if not multa["data"] == "":
            raise MultaInvalida(f"data precisa ser igual a \"\" quando codigoMulta = {multa['codigoMulta']}")
        if not multa["taxa"] == "":
            raise MultaInvalida(f"taxa precisa ser igual a \"\" quando codigoMulta = {multa['codigoMulta']}")
        if not multa["valor"] == "":
            raise MultaInvalida(f"valor precisa ser igual a \"\" quando codigoMulta = {multa['codigoMulta']}")


def check_mora(mora=None, vencimento=None):
    if mora is None:
        raise MoraInvalida("mora não pode ser vazia")
    if vencimento is None:
        MoraInvalida("informe o vencimento")

    if mora["codigoMora"] not in _CODIGOS_MORA:
        raise MoraInvalida(f"codigoMora invalido, valores aceitos: {_CODIGOS_MORA.__str__()}")

    if mora["codigoMora"] in ("VALORDIA", "TAXAMENSAL"):
        if not check_date(mora["data"]):
            raise MoraInvalida("formato de data invalido")
        if not mora["data"]:
            raise MoraInvalida(f"data obrigatoria quando codigoMora = {mora['codigoMora']}")
        if mora["data"] <= vencimento:
            raise MoraInvalida(f"data não pode ser menor ou igual ao vencimento")

        if mora["codigoMora"] == "TAXAMENSAL":
            if not mora["taxa"]:
                raise MoraInvalida(f"taxa precisa ser definada quando codigoMora = {mora['codigoMora']}")
        else:
            if not mora["valor"]:
                raise MoraInvalida(f"valor precisa ser definada quando codigoMora = {mora['codigoMora']}")
    else:
        if not mora["data"] == "":
            raise MoraInvalida(f"data precisa ser igual a \"\" quando codigoMulta = {mora['codigoMora']}")
        if not mora["taxa"] == "":
            raise MoraInvalida(f"taxa precisa ser igual a \"\" quando codigoMulta = {mora['codigoMora']}")
        if not mora["valor"] == "":
            raise MoraInvalida(f"valor precisa ser igual a \"\" quando codigoMulta = {mora['codigoMora']}")
