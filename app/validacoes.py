import re

#----------------------validação de cpf


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove pontuação

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[i]):
            return False

    return True


#----------------------validação de nome


def validar_nome(nome):
    nome_regex = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$')
    return bool(nome) and nome_regex.fullmatch(nome)


#----------------------validação de email

def validar_email(email):  
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$')
    return bool(email_regex.fullmatch(email))

#----------------------validação de telefone

def validar_telefone(telefone):
    # Expressão regular para validar número de telefone no formato (XX) XXXXX-XXXX
    padrao_telefone = r'^\(\d{2}\) \d{5}-\d{4}$'
    
    if re.match(padrao_telefone, telefone):
        return True
    else:
        return False

#----------------------validação de telefone

def formatar_telefone(telefone):
    # Remover qualquer caractere que não seja número
    telefone = re.sub(r'\D', '', telefone)
    
    # Verifica se o número tem o tamanho correto
    if len(telefone) == 11:  # Telefone no formato celular com DDD (XX XXXXX-XXXX)
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    else:
        return None  # Ou você pode retornar um erro ou mensagem



