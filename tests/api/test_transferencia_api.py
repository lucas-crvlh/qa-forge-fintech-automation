"""
Testes de API para funcionalidades de transferência e consulta de saldo.
"""
import pytest
import allure
from typing import Dict, Any


# =============================================================================
# CENÁRIOS DE CONSULTA E CADASTRO
# =============================================================================

@allure.feature("Consulta de Saldo")
@allure.story("Consulta de saldo de usuário cadastrado")
def test_01_consulta_saldo_usuario_cadastrado(fintech_api, usuario_teste, anexar_payload_api):
    """
    Pré-requisito para o E2E: Verifica se a conta criada pela fixture pode ser 
    consultada com sucesso (Mock 200).
    """
    with allure.step("Arrange - Preparar dados do teste"):
        conta_id = usuario_teste['conta_id']
        allure.attach(conta_id, name="Conta ID", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Act - Consultar saldo da conta"):
        response = fintech_api.consultar_saldo(
            conta_id=conta_id,
            scenario_name="Saldo Encontrado 200"
        )
        
        # Anexar payloads ao relatório
        anexar_payload_api(
            request_payload={"conta_id": conta_id},
            response_data=response.json(),
            endpoint="/saldo",
            method="GET"
        )
    
    with allure.step("Assert - Validar resposta de sucesso"):
        assert response.status_code == 200, f"Status code esperado 200, mas recebido {response.status_code}"
        
        data = response.json()
        
        # Validação da estrutura do JSON
        assert 'conta_id' in data, "Campo 'conta_id' não encontrado na resposta"
        assert 'saldo' in data, "Campo 'saldo' não encontrado na resposta"
        
        # Validação dos valores
        assert data['conta_id'] == conta_id, f"conta_id esperado '{conta_id}', mas recebido '{data['conta_id']}'"
        assert isinstance(data['saldo'], (int, float)), f"Saldo deve ser numérico, mas recebido {type(data['saldo'])}"
        assert data['saldo'] >= 0.00, f"Saldo deve ser >= 0, mas recebido {data['saldo']}"
        
        # Validação de campos obrigatórios
        expected_fields = ['conta_id', 'saldo']
        actual_fields = list(data.keys())
        assert all(field in actual_fields for field in expected_fields), \
            f"Campos esperados {expected_fields}, mas recebidos {actual_fields}"
    
@allure.feature("Cadastro de Usuário")
@allure.story("Validação de CPF duplicado")
def test_02_cadastro_com_cpf_duplicado_deve_falhar(fintech_api, anexar_payload_api):
    """
    Verifica a Regra de Negócio: Não deve permitir CPF duplicado (Mock 409).
    """
    with allure.step("Arrange - Preparar dados de cadastro com CPF duplicado"):
        dados_cadastro = {
            "nome": "Duplicado",
            "cpf": "111.111.111-11",
            "senha": "dupsenha"
        }
        allure.attach(str(dados_cadastro), name="Dados de Cadastro", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Act - Tentar cadastrar usuário com CPF duplicado"):
        response = fintech_api.cadastrar_usuario(
            nome=dados_cadastro["nome"],
            cpf=dados_cadastro["cpf"],
            senha=dados_cadastro["senha"],
            scenario_name="Cadastro Falha CPF Duplicado 409"
        )
        
        # Anexar payloads ao relatório
        anexar_payload_api(
            request_payload=dados_cadastro,
            response_data=response.json(),
            endpoint="/cadastro",
            method="POST"
        )
    
    with allure.step("Assert - Validar erro de CPF duplicado"):
        assert response.status_code == 409, f"Status code esperado 409, mas recebido {response.status_code}"
        
        data = response.json()
        
        # Validação da estrutura do JSON de erro
        assert 'status' in data, "Campo 'status' não encontrado na resposta de erro"
        assert 'mensagem' in data, "Campo 'mensagem' não encontrado na resposta de erro"
        
        # Validação dos valores de erro
        assert data['status'] == "FALHA_NEGOCIO", f"Status esperado 'FALHA_NEGOCIO', mas recebido '{data['status']}'"
        assert isinstance(data['mensagem'], str), f"Mensagem deve ser string, mas recebido {type(data['mensagem'])}"
        assert "CPF já cadastrado" in data['mensagem'], \
            f"Mensagem deve conter 'CPF já cadastrado', mas recebido: '{data['mensagem']}'"
        
        # Validação de campos obrigatórios de erro
        expected_error_fields = ['status', 'mensagem']
        actual_fields = list(data.keys())
        assert all(field in actual_fields for field in expected_error_fields), \
            f"Campos de erro esperados {expected_error_fields}, mas recebidos {actual_fields}"

# =============================================================================
# CENÁRIOS DE TRANSFERÊNCIA
# =============================================================================

@allure.feature("Transferência")
@allure.story("Transferência com sucesso")
def test_03_transferencia_deve_ser_concluida_com_sucesso(fintech_api, usuario_teste, anexar_payload_api):
    """
    Teste de Fumaça/Sucesso: Verifica o fluxo principal de transferência (Mock 200).
    """
    with allure.step("Arrange - Preparar dados da transferência"):
        conta_origem = usuario_teste['conta_id']
        dados_transferencia = {
            "origem": conta_origem,
            "destino": "45678",
            "valor": 100.00
        }
        allure.attach(str(dados_transferencia), name="Dados da Transferência", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Act - Realizar transferência"):
        response = fintech_api.realizar_transferencia(
            origem=dados_transferencia["origem"],
            destino=dados_transferencia["destino"],
            valor=dados_transferencia["valor"],
            scenario_name="Transferencia Sucesso 200"
        )
        
        # Anexar payloads ao relatório
        anexar_payload_api(
            request_payload=dados_transferencia,
            response_data=response.json(),
            endpoint="/transferencia",
            method="POST"
        )
    
    with allure.step("Assert - Validar sucesso da transferência"):
        assert response.status_code == 200, f"Status code esperado 200, mas recebido {response.status_code}"
        
        data = response.json()
        
        # Validação da estrutura do JSON de sucesso
        assert 'status' in data, "Campo 'status' não encontrado na resposta"
        assert 'transacao_id' in data, "Campo 'transacao_id' não encontrado na resposta"
        
        # Validação dos valores de sucesso
        assert data['status'] == "SUCESSO", f"Status esperado 'SUCESSO', mas recebido '{data['status']}'"
        assert isinstance(data['transacao_id'], str), f"transacao_id deve ser string, mas recebido {type(data['transacao_id'])}"
        assert len(data['transacao_id']) > 0, "transacao_id não pode estar vazio"
        assert "T-QA" in data['transacao_id'], f"transacao_id deve conter 'T-QA', mas recebido: '{data['transacao_id']}'"
        
        # Validação de campos obrigatórios de sucesso
        expected_success_fields = ['status', 'transacao_id']
        actual_fields = list(data.keys())
        assert all(field in actual_fields for field in expected_success_fields), \
            f"Campos de sucesso esperados {expected_success_fields}, mas recebidos {actual_fields}"

@allure.feature("Transferência")
@allure.story("Transferência com saldo insuficiente")
def test_04_transferencia_com_saldo_insuficiente_deve_falhar(fintech_api, anexar_payload_api):
    """
    Verifica a Regra de Negócio: Transferência com saldo insuficiente deve falhar (Mock 400).
    """
    with allure.step("Arrange - Preparar dados de transferência com valor alto"):
        dados_transferencia = {
            "origem": "999",
            "destino": "888",
            "valor": 10000.00
        }
        allure.attach(str(dados_transferencia), name="Dados da Transferência", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Act - Tentar transferência com saldo insuficiente"):
        response = fintech_api.realizar_transferencia(
            origem=dados_transferencia["origem"],
            destino=dados_transferencia["destino"],
            valor=dados_transferencia["valor"],
            scenario_name="Falha Saldo Insuficiente 400"
        )
        
        # Anexar payloads ao relatório
        anexar_payload_api(
            request_payload=dados_transferencia,
            response_data=response.json(),
            endpoint="/transferencia",
            method="POST"
        )
    
    with allure.step("Assert - Validar erro de saldo insuficiente"):
        assert response.status_code == 400, f"Status code esperado 400, mas recebido {response.status_code}"
        
        data = response.json()
        
        # Validação da estrutura do JSON de erro
        assert 'status' in data, "Campo 'status' não encontrado na resposta de erro"
        assert 'codigo_erro' in data, "Campo 'codigo_erro' não encontrado na resposta de erro"
        
        # Validação dos valores de erro
        assert data['status'] == "FALHA_NEGOCIO", f"Status esperado 'FALHA_NEGOCIO', mas recebido '{data['status']}'"
        assert isinstance(data['codigo_erro'], str), f"codigo_erro deve ser string, mas recebido {type(data['codigo_erro'])}"
        assert data['codigo_erro'] == "ERR-SALDO-001", f"codigo_erro esperado 'ERR-SALDO-001', mas recebido '{data['codigo_erro']}'"
        
        # Validação de campos obrigatórios de erro
        expected_error_fields = ['status', 'codigo_erro']
        actual_fields = list(data.keys())
        assert all(field in actual_fields for field in expected_error_fields), \
            f"Campos de erro esperados {expected_error_fields}, mas recebidos {actual_fields}"
        
        # Validação adicional: verificar mensagem de erro (se presente)
        if 'mensagem' in data:
            assert isinstance(data['mensagem'], str), f"Mensagem deve ser string, mas recebido {type(data['mensagem'])}"
            assert len(data['mensagem']) > 0, "Mensagem de erro não pode estar vazia"

@allure.feature("Consulta de Saldo")
@allure.story("Consulta de conta inexistente")
def test_05_consulta_saldo_conta_inexistente(fintech_api, anexar_payload_api):
    """
    Testa se a API retorna 404 Not Found ao consultar uma conta que não existe.
    """
    with allure.step("Arrange - Preparar conta inexistente"):
        conta_id_inexistente = "00000"
        allure.attach(conta_id_inexistente, name="Conta ID Inexistente", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Act - Consultar saldo de conta inexistente"):
        response = fintech_api.consultar_saldo(
            conta_id=conta_id_inexistente,
            scenario_name="Saldo Nao Encontrado 404"
        )
        
        # Anexar payloads ao relatório
        anexar_payload_api(
            request_payload={"conta_id": conta_id_inexistente},
            response_data=response.json(),
            endpoint="/saldo",
            method="GET"
        )
    
    with allure.step("Assert - Validar erro 404"):
        assert response.status_code == 404, f"Status code esperado 404, mas recebido {response.status_code}"
        
        data = response.json()
        assert data['status'] == "ERRO", f"Status esperado 'ERRO', mas recebido '{data['status']}'"
        assert "não encontrada" in data['mensagem'], \
            f"Mensagem deve conter 'não encontrada', mas recebido: '{data['mensagem']}'"


@allure.feature("Transferência")
@allure.story("Transferência para conta destino inexistente")
def test_06_transferencia_conta_destino_inexistente_deve_falhar(fintech_api, usuario_teste, anexar_payload_api):
    """
    Testa se a transferência falha quando a conta de destino não está cadastrada (Mock 404).
    """
    with allure.step("Arrange - Preparar dados da transferência com destino inexistente"):
        conta_origem = usuario_teste['conta_id']
        conta_destino_ficticia = "00000"
        dados_transferencia = {
            "origem": conta_origem,
            "destino": conta_destino_ficticia,
            "valor": 50.00
        }
        allure.attach(str(dados_transferencia), name="Dados da Transferência", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Act - Tentar transferência para conta destino inexistente"):
        response = fintech_api.realizar_transferencia(
            origem=dados_transferencia["origem"],
            destino=dados_transferencia["destino"],
            valor=dados_transferencia["valor"],
            scenario_name="Conta Destino Invalida 404"
        )
        
        # Anexar payloads ao relatório
        anexar_payload_api(
            request_payload=dados_transferencia,
            response_data=response.json(),
            endpoint="/transferencia",
            method="POST"
        )
    
    with allure.step("Assert - Validar erro 404"):
        assert response.status_code == 404, f"Status code esperado 404, mas recebido {response.status_code}"
        
        data = response.json()
        assert data['status'] == "ERRO", f"Status esperado 'ERRO', mas recebido '{data['status']}'"
        assert "destino não existe" in data['mensagem'], \
            f"Mensagem deve conter 'destino não existe', mas recebido: '{data['mensagem']}'"