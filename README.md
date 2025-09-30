🚀 QA-Forge: Framework Híbrido de Automação de Testes para Fintechs

🌟 Visão Geral do Projeto
O QA-Forge é um Framework de Automação de Testes Híbrido desenvolvido para demonstrar a proficiência em Engenharia de Qualidade (QE) e práticas de Shift-Left Testing.

Foco: Garantir a integridade transacional e a segurança de dados em ambientes de Serviços Financeiros Digitais (Fintechs) através de testes automatizados de ponta a ponta e CI/CD.

💡 O Problema Resolvido (A Dor da Fintech)
O setor financeiro digital sofre com o alto risco de integridade de dados (erros em débito/crédito) e a lentidão nos lançamentos (Time-to-Market). A dependência de testes manuais caros e testes E2E instáveis aumenta o risco de bugs críticos chegarem à produção.

🎯 Solução do QA-Forge:

Implementação de Estratégia Híbrida para isolar o risco:

Testes de API (Pytest) validam a lógica de negócio e a persistência de saldos, que é o coração do sistema.

Testes E2E (Playwright) simulam a jornada do usuário na interface, focando na usabilidade e na correta exibição dos dados já validados.

🛠️ Tecnologias e Arquitetura

* Este projeto utiliza um stack de ferramentas moderno e escalável, seguindo o padrão Page Object Model (POM).

| Componente | Tecnologia/Padrão | Uso Estratégico |
| :--- | :--- | :--- |
| **Linguagem** | **Python** | Escolhida pela simplicidade, manutenibilidade e ecossistema robusto. |
| **Test Runner** | **Pytest** | Executor principal, usado para escrever os testes de API e gerenciar a estrutura. |
| **Web Automation** | **Playwright** | Automação rápida e estável da interface de usuário (E2E) e geração de evidências (screenshots). |
| **Padrão de Projeto** | **Page Object Model (POM)** | Essencial para criar código manutenível e escalável, separando a lógica de teste dos seletores de página. |
| **Reporting** | **Allure Reports** | Geração de relatórios visuais profissionais, facilitando a rastreabilidade e a comunicação de falhas. |
| **CI/CD** | **GitHub Actions** | Automatiza a execução dos testes a cada push de código, demonstrando proficiência em práticas DevOps. |

🧪 Casos de Teste Chave Implementados
Os testes são focados em simular o core business de uma Fintech:

| Tipo de Teste | Descrição do Cenário | Valor Agregado |
| :--- | :--- | :--- |
| **API Crítica** | **Validação da Transferência Financeira:** O teste garante que o débito na conta de origem e o crédito na conta de destino são simultâneos e corretos. | Garante a **integridade dos dados** e a estabilidade do **core business**. |
| **E2E Híbrido** | **Jornada de Login e Consulta de Saldo:** Utiliza a API para criar um usuário e depois verifica, via interface, se o saldo é exibido corretamente. | Garante a **experiência do usuário** (UX) e a corretude visual dos dados críticos. |

🏆 Desafios Técnicos Superados (O Diferencial)

Gerenciamento de Dados Complexos: Utilização de Pytest Fixtures em conjunto com a API para criar e destruir dados de teste on-the-fly, garantindo o isolamento dos cenários.

Transações Assíncronas: Implementação de um mecanismo de Polling na API para verificar o saldo, resolvendo o problema de flakiness e garantindo a validação apenas após a persistência da transação.

Segurança em CI/CD: Uso de GitHub Secrets para proteger credenciais de acesso durante a execução automatizada.

Autor: [Lucas Carvalho Cordeiro] - [https://www.linkedin.com/in/lucas-crvlh00/]
