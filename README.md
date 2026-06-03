# QA-Forge — Framework de Testes API-First para Fintech

> Framework de automação de testes focado em validação de APIs financeiras, com service virtualization, rastreabilidade via Allure Reports e pipeline CI/CD no GitHub Actions.

[![CI Status](https://github.com/lucas-crvlh/qa-forge-fintech-automation/actions/workflows/main.yml/badge.svg)](https://github.com/lucas-crvlh/qa-forge-fintech-automation/actions/workflows/main.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![Pytest](https://img.shields.io/badge/Pytest-Framework-green)]()
[![Allure](https://img.shields.io/badge/Allure-Reports-orange)]()

---

## Índice

1. [Sobre o Projeto](#1-sobre-o-projeto)
2. [Problema de Negócio](#2-problema-de-negócio)
3. [Arquitetura do Framework](#3-arquitetura-do-framework)
4. [Estrutura de Pastas](#4-estrutura-de-pastas)
5. [Stack](#5-stack)
6. [Casos de Teste Implementados](#6-casos-de-teste-implementados)
7. [Como Executar](#7-como-executar)
8. [Rastreabilidade com Allure](#8-rastreabilidade-com-allure)
9. [CI/CD com GitHub Actions](#9-cicd-com-github-actions)
10. [Decisões Técnicas](#10-decisões-técnicas)

---

## 1. Sobre o Projeto

O QA-Forge é um framework de automação de testes de API desenvolvido para validar fluxos críticos de um serviço financeiro digital — cadastro de usuários, consulta de saldo e transferências.

O projeto demonstra uma abordagem **API-First**: os testes atacam diretamente a camada de lógica de negócio, sem depender de interface gráfica, garantindo velocidade, estabilidade e rastreabilidade das validações.

A combinação de **Pytest + Postman Mock Server + Allure Reports + GitHub Actions** forma um pipeline completo de qualidade, do teste local ao CI automatizado.

---

## 2. Problema de Negócio

Serviços financeiros exigem zero tolerância a falhas em transações. Os principais riscos que este framework cobre:

- transferências com saldo insuficiente sendo processadas
- contas inexistentes sendo aceitas como destino válido
- CPFs duplicados sendo cadastrados sem rejeição
- inconsistência nos campos de resposta da API
- regressões silenciosas após deploys

A abordagem de **service virtualization** resolve um problema clássico em ambientes de teste financeiro: forçar cenários de erro raros (como saldo insuficiente ou conta inexistente) sem depender de um backend real configurado para falhar.

---

## 3. Arquitetura do Framework

```
tests/
  └── api/
        └── test_transferencia_api.py   ← casos de teste (Arrange/Act/Assert)
              ↓
        conftest.py                     ← fixtures, setup e teardown
              ↓
src/services/
        └── api_client.py              ← cliente HTTP centralizado
              ↓
Postman Mock Server                    ← service virtualization
(x-mock-response-name header)
              ↓
Allure Reports                         ← rastreabilidade com payloads anexados
              ↓
GitHub Actions CI                      ← execução automática a cada push
```

**Fluxo de um teste:**

1. Fixture cria dados únicos baseados em timestamp
2. Teste executa a chamada via `FintechAPI` (cliente centralizado)
3. Header `x-mock-response-name` instrui o Mock Server a retornar o cenário específico
4. Allure anexa o payload da requisição e da resposta ao relatório
5. Assertions validam estrutura, tipos e valores da resposta
6. Fixture de teardown registra limpeza dos dados criados

---

## 4. Estrutura de Pastas

```
qa-forge-fintech-automation/
│
├── .github/
│   └── workflows/
│       └── main.yml              # Pipeline CI/CD GitHub Actions
│
├── src/
│   └── services/
│       └── api_client.py         # Cliente HTTP centralizado (FintechAPI)
│
├── tests/
│   ├── conftest.py               # Fixtures: setup, teardown, dados únicos
│   └── api/
│       └── test_transferencia_api.py  # 6 casos de teste documentados
│
├── reports/
│   ├── allure-results/           # Resultados brutos gerados pelo Pytest
│   └── allure-report/            # Relatório HTML gerado pelo Allure
│
├── requirements.txt
├── task.ps1                      # Script PowerShell para execução local
└── README.md
```

---

## 5. Stack

| Componente | Tecnologia | Função |
|-----------|-----------|--------|
| Linguagem | Python 3.10+ | — |
| Test runner | Pytest | Execução e organização dos testes |
| HTTP client | Requests | Chamadas às APIs |
| Service virtualization | Postman Mock Server | Simulação de respostas controladas |
| Relatórios | Allure Reports | Rastreabilidade com payloads e steps |
| CI/CD | GitHub Actions | Execução automática a cada push |
| Organização | Fixtures Pytest | Setup, teardown e dados de teste |

---

## 6. Casos de Teste Implementados

| # | Feature | Cenário | Endpoint | Status esperado |
|---|---------|---------|----------|----------------|
| 01 | Consulta de Saldo | Consulta de conta cadastrada | `GET /saldo/{conta_id}` | 200 |
| 02 | Cadastro | CPF duplicado deve ser rejeitado | `POST /cadastro` | 409 |
| 03 | Transferência | Transferência bem-sucedida | `POST /transferencia` | 200 |
| 04 | Transferência | Saldo insuficiente deve falhar | `POST /transferencia` | 400 |
| 05 | Consulta de Saldo | Conta inexistente retorna 404 | `GET /saldo/{conta_id}` | 404 |
| 06 | Transferência | Conta destino inexistente deve falhar | `POST /transferencia` | 404 |

Cada teste valida três camadas:
- **Status code** da resposta HTTP
- **Estrutura do JSON** (campos obrigatórios presentes)
- **Valores e tipos** dos campos retornados

### Exemplo de asserção (teste 04 — saldo insuficiente)

```python
assert response.status_code == 400
assert data['status'] == "FALHA_NEGOCIO"
assert data['codigo_erro'] == "ERR-SALDO-001"
```

---

## 7. Como Executar

### Pré-requisitos

- Python 3.10+
- Allure CLI instalado ([instruções](https://allurereport.org/docs/install/))

### Instalação

```bash
git clone https://github.com/lucas-crvlh/qa-forge-fintech-automation.git
cd qa-forge-fintech-automation
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### Executar os testes

```bash
pytest tests/api --alluredir=reports/allure-results
```

### Visualizar o relatório Allure

```bash
allure serve reports/allure-results
```

### Usando o task runner (PowerShell)

```powershell
.\task.ps1
```

### Variável de ambiente (opcional)

Por padrão, os testes apontam para o Postman Mock Server configurado no projeto. Para usar um servidor diferente:

```bash
set MOCK_API_URL=https://seu-mock-server.pstmn.io  # Windows
export MOCK_API_URL=https://seu-mock-server.pstmn.io  # Linux/Mac
```

---

## 8. Rastreabilidade com Allure

Cada teste anexa automaticamente ao relatório:

- **Request payload** — dados enviados na requisição
- **Response data** — resposta completa da API
- **Steps documentados** — Arrange, Act e Assert visíveis no relatório
- **Dados de fixtures** — conta criada, dados do usuário de teste

Isso elimina a dependência de logs externos para depuração e garante rastreabilidade completa de cada execução.

---

## 9. CI/CD com GitHub Actions

O pipeline executa automaticamente a cada `push` ou `pull request` na branch `main`:

```yaml
steps:
  - Checkout do código
  - Setup Python 3.10
  - Instalação das dependências
  - Execução do Pytest com geração de resultados Allure
  - Upload dos resultados como artefato da Action
```

Os resultados ficam disponíveis na aba **Actions** do repositório após cada execução.

---

## 10. Decisões Técnicas

**Por que Postman Mock Server em vez de um backend real?**
Service virtualization permite forçar cenários de erro que são difíceis de reproduzir em um ambiente real (saldo insuficiente, conta inexistente). O header `x-mock-response-name` instrui o mock a retornar exatamente o cenário desejado, garantindo estabilidade e isolamento dos testes.

**Por que API-First em vez de testes E2E com UI?**
Testes de UI são mais lentos, frágeis a mudanças de layout e não testam a lógica de negócio diretamente. Testes de API validam o contrato do serviço de forma mais rápida, estável e rastreável.

**Por que fixtures com teardown?**
Garantir isolamento entre testes. Cada teste cria seus próprios dados com timestamp único e os registra para limpeza automática, evitando dependência entre casos de teste.

**Por que Allure em vez de relatórios padrão do Pytest?**
Allure permite anexar payloads de requisição e resposta diretamente ao relatório, tornando a depuração de falhas significativamente mais rápida — especialmente em ambientes de CI onde não há acesso ao terminal.

---

*Autor: [Lucas Carvalho](https://www.linkedin.com/in/lucas-crvlh00/)*
