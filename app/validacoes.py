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
    return bool(nome_regex.match(nome))

#----------------------validação de nome ????

def nome_nao_comeca_com_numero(nome):
    return bool(nome) and not nome[0].isdigit()


#----------------------validação de email

def validar_email(email):  
    email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$')
    return bool(email_regex.match(email))

