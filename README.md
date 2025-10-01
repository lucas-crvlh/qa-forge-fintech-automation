# 🚀 QA-Forge: Framework de Automação Focado em API para Fintechs

### 🌟 Visão Geral do Projeto (API-First Testing)

O QA-Forge é um Framework de Automação de Testes desenvolvido para demonstrar a proficiência em Engenharia de Qualidade (QE) e práticas de **API-First Testing**.

Foco: Garantir a integridade transacional e a segurança de dados em ambientes de Serviços Financeiros Digitais (Fintechs) através de testes automatizados diretamente na **camada de lógica de negócio (API)**.

### 💡 O Problema Resolvido (A Dor da Fintech)

O setor financeiro digital exige velocidade e risco zero em transações. A dependência de testes manuais e a instabilidade em ambientes de teste são inaceitáveis.

🎯 **Solução do QA-Forge:**

Implementação de uma Estratégia Robusta para isolar o risco:

* **Testes de API (Pytest)** validam a lógica de negócio, a persistência de saldos e as regras transacionais.
* **Service Virtualization (Postman Mock Server)** garante a estabilidade e o isolamento dos cenários, simulando todas as respostas da aplicação e dependências externas.

---

### 🛠️ Tecnologias e Arquitetura

Este projeto utiliza um stack de ferramentas moderno e escalável:

| Componente | Tecnologia/Padrão | Uso Estratégico |
| :--- | :--- | :--- |
| **Linguagem** | **Python** | Escolhida pela simplicidade, manutenibilidade e ecossistema robusto. |
| **Test Runner** | **Pytest** | Executor principal para escrever os testes de API. |
| **Service Virtualization** | **Postman Mock Server** | Simulação de ambientes para forçar cenários de erro raros (saldo insuficiente, conta inexistente). |
| **Reporting** | **Allure Reports** | Geração de relatórios visuais profissionais **com anexos JSON (payloads e respostas)**, facilitando a rastreabilidade e a depuração. |
| **Estrutura UI** | **Playwright** | Estrutura modular de UI implementada para **futura expansão** dos testes E2E. |
| **CI/CD** | **GitHub Actions** | Automatiza a execução dos testes a cada *push* de código (Demonstração de DevOps). |

---

### 🧪 Casos de Teste Chave Implementados (API Core)

Os 6 testes implementados simulam o *core business* de uma Fintech:

| Tipo de Teste | Cenário de Teste Implementado | Valor Agregado |
| :--- | :--- | :--- |
| **API Crítica (200)** | **Transferência Financeira:** Garante que o débito na origem e o crédito no destino são corretos. | Garante a **integridade transacional** e estabilidade. |
| **API Crítica (400)** | **Transferência com Saldo Insuficiente.** | Validação da regra de negócio crítica para prevenir saldo negativo ou fraude. |
| **API Crítica (404)** | **Transferência para Conta Destino Inexistente.** | Validação do tratamento de erro para recursos não encontrados. |
| **API Funcional (400)** | Falha no Cadastro ao usar CPF duplicado. | Garante a unicidade e a criação correta de dados base. |

### 🏆 Desafios Técnicos Superados (O Diferencial de QE)

* **Service Virtualization e Cenários Negativos:** Utilização do **Postman Mock Server** integrado ao Pytest para forçar o backend a retornar status `400` e `404` (via `x-mock-response-name` header), provando a resiliência do sistema a falhas.
* **Rastreabilidade Profissional (Allure Attachments):** Integração do **Allure Reports** com `allure.attach()` no cliente API para anexar o JSON da **requisição (payload)** e o JSON da **resposta** de cada teste. Isso elimina a dependência de *logs* externos para depuração.
* **Gerenciamento de Dados Complexos:** Utilização de **Pytest Fixtures** em conjunto com a API para criar e destruir dados de teste *on-the-fly*, garantindo o isolamento dos cenários.

---

### ⚙️ Como Executar os Testes (Instruções)

1.  **Ative o Ambiente Virtual:**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

2.  **Execute os Testes e Gere o Relatório:**
    ```bash
    pytest tests/api --alluredir=reports/allure-results
    ```

3.  **Visualizar o Relatório Interativo:**
    ```bash
    allure serve reports/allure-results
    ```

Autor: Lucas Carvalho Cordeiro - https://www.linkedin.com/in/lucas-crvlh00/
