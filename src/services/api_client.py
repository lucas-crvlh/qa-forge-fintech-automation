import requests
import os
import allure

class FintechAPI:
    def __init__(self):
        # A URL do seu Mock Server que você copiou do Postman
        self.base_url = os.environ.get("MOCK_API_URL", "https://38c7103a-8b55-4ca9-b297-4b802d0be29f.mock.pstmn.io")

    def _send_request(self, method, path, payload=None, scenario_name=None):
        url = f"{self.base_url}{path}"
        headers = {}
        
        # ESSENCIAL: Diz ao Mock Server qual cenário de resposta retornar
        if scenario_name:
            headers['x-mock-response-name'] = scenario_name
            allure.attach(scenario_name, name="QA Forge Fintech", attachment_type=allure.attachment_type.TEXT)
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=headers)
        else:
            raise ValueError("Método HTTP não suportado.")
            
        return response

    # --- Método 1: Cadastro ---
    def cadastrar_usuario(self, nome, cpf, senha, scenario_name=None):
        payload = {"nome": nome, "cpf": cpf, "senha": senha}
        return self._send_request("POST", "/cadastro", payload, scenario_name)

    # --- Método 2: Consulta de Saldo ---
    def consultar_saldo(self, conta_id, scenario_name=None):
        # O Path da URL no Mock Server é /saldo/{{conta_id}}, mas no código enviamos apenas /saldo/
        # O Postman fará o matching correto com a rota /saldo/...
        return self._send_request("GET", f"/saldo/{conta_id}", scenario_name=scenario_name)

    # --- Método 3: Transferência ---
    def realizar_transferencia(self, origem, destino, valor, scenario_name=None):
        payload = {"origem": origem, "destino": destino, "valor": valor}
        return self._send_request("POST", "/transferencia", payload, scenario_name)