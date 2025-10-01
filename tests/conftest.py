"""
Configurações e fixtures compartilhadas para testes de API.
"""
import pytest
import time
import allure
from typing import Dict, Any, Generator
from src.services.api_client import FintechAPI


# =============================================================================
# FIXTURES DE CONFIGURAÇÃO E CLIENTES
# =============================================================================

@pytest.fixture(scope="session")
def fintech_api() -> FintechAPI:
    """
    Fornece uma única instância do cliente FintechAPI para todos os testes da sessão.
    
    Returns:
        FintechAPI: Instância do cliente de API
    """
    return FintechAPI()


# =============================================================================
# FIXTURES DE DADOS DE TESTE
# =============================================================================

@pytest.fixture
def dados_usuario_unicos() -> Dict[str, str]:
    """
    Gera dados únicos para um usuário de teste baseado em timestamp.
    
    Returns:
        Dict[str, str]: Dados do usuário com nome, CPF e senha únicos
    """
    timestamp = str(int(time.time()))
    return {
        "nome": f"Tester {timestamp[-4:]}",
        "cpf": f"111.111.111-{timestamp[-2:]}",
        "senha": "secure_pass"
    }


@pytest.fixture
def usuario_cadastrado(fintech_api: FintechAPI, dados_usuario_unicos: Dict[str, str]) -> Dict[str, str]:
    """
    Cadastra um usuário e retorna os dados completos.
    
    Args:
        fintech_api: Cliente da API
        dados_usuario_unicos: Dados únicos do usuário
        
    Returns:
        Dict[str, str]: Dados completos do usuário cadastrado
    """
    dados = dados_usuario_unicos
    
    with allure.step("Cadastrar usuário de teste"):
        cadastro_response = fintech_api.cadastrar_usuario(
            nome=dados["nome"],
            cpf=dados["cpf"],
            senha=dados["senha"],
            scenario_name="Cadastro Sucesso 201"
        )
        
        # Anexar payload de resposta ao relatório Allure
        allure.attach(
            cadastro_response.text,
            name="Response - Cadastro Usuário",
            attachment_type=allure.attachment_type.JSON
        )
    
    conta_id = cadastro_response.json().get('conta_id', 'MOCK_ID_FAIL')
    
    return {
        "conta_id": conta_id,
        "cpf": dados["cpf"],
        "nome": dados["nome"],
        "senha": dados["senha"]
    }


# =============================================================================
# FIXTURES DE LIMPEZA E TEARDOWN
# =============================================================================

@pytest.fixture
def limpeza_usuario() -> Generator[callable, None, None]:
    """
    Fixture para gerenciar limpeza de dados de usuário.
    
    Yields:
        callable: Função para adicionar usuários à lista de limpeza
    """
    usuarios_para_limpar = []
    
    def adicionar_para_limpeza(conta_id: str) -> None:
        """Adiciona um usuário à lista de limpeza."""
        usuarios_para_limpar.append(conta_id)
    
    yield adicionar_para_limpeza
    
    # Teardown: Limpa todos os usuários registrados
    if usuarios_para_limpar:
        with allure.step("Limpeza de dados de teste"):
            allure.attach(
                str(usuarios_para_limpar),
                name="Usuários para Limpeza",
                attachment_type=allure.attachment_type.TEXT
            )
            # Em um ambiente real, aqui seria feita a chamada DELETE /usuario/{id}
            # for conta_id in usuarios_para_limpar:
            #     fintech_api.deletar_usuario(conta_id)


# =============================================================================
# FIXTURES PRINCIPAIS DE TESTE
# =============================================================================

@pytest.fixture
def usuario_teste(usuario_cadastrado: Dict[str, str], limpeza_usuario: callable) -> Generator[Dict[str, str], None, None]:
    """
    Fixture principal que fornece um usuário completo para testes.
    
    Args:
        usuario_cadastrado: Dados do usuário cadastrado
        limpeza_usuario: Função de limpeza
        
    Yields:
        Dict[str, str]: Dados completos do usuário de teste
    """
    # Registra o usuário para limpeza automática
    limpeza_usuario(usuario_cadastrado['conta_id'])
    
    with allure.step("Configurar usuário de teste"):
        allure.attach(
            str(usuario_cadastrado),
            name="Dados do Usuário de Teste",
            attachment_type=allure.attachment_type.JSON
        )
    
    yield usuario_cadastrado


# =============================================================================
# FIXTURES AUXILIARES PARA ANEXOS DO ALLURE
# =============================================================================

@pytest.fixture
def anexar_payload_api():
    """
    Fixture para anexar payloads de requisição e resposta ao relatório Allure.
    
    Returns:
        callable: Função para anexar payloads
    """
    def _anexar_payloads(
        request_payload: Dict[str, Any] = None,
        response_data: Any = None,
        endpoint: str = "",
        method: str = ""
    ) -> None:
        """
        Anexa payloads de requisição e resposta ao relatório Allure.
        
        Args:
            request_payload: Dados da requisição
            response_data: Dados da resposta
            endpoint: Endpoint da API
            method: Método HTTP
        """
        if request_payload:
            allure.attach(
                str(request_payload),
                name=f"Request Payload - {method} {endpoint}",
                attachment_type=allure.attachment_type.JSON
            )
        
        if response_data:
            allure.attach(
                str(response_data),
                name=f"Response Data - {method} {endpoint}",
                attachment_type=allure.attachment_type.JSON
            )
    
    return _anexar_payloads