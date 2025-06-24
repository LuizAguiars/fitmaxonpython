import requests
from datetime import date, timedelta


def gerar_cobranca(usuario, plano):
    headers = {
        "Authorization": "Bearer SEU_TOKEN_AQUI",  # Coloque o token real
        "Content-Type": "application/json"
    }

    payload = {
        "items": [{
            "name": plano.nome_plano,
            "amount": 1,
            "value": int(plano.valor_plano * 100)
        }],
        "payment": {
            "banking_billet": {
                "expire_at": str(date.today() + timedelta(days=5)),
                "customer": {
                    "name": usuario.Nome_User,
                    "cpf": usuario.cpf_user,
                    "email": usuario.Email_user,
                    "birth": str(usuario.Data_Nascimento),
                    "phone_number": usuario.telefone_user
                }
            }
        }
    }

    response = requests.post(
        "https://api.gerencianet.com.br/v1/charge", headers=headers, json=payload)
    data = response.json()
    return data['data']['link'] if 'data' in data else "#"
