# Fundamentos de segurança — GuardAI

Base didática para conversar sobre segurança com contexto, autorização e evidências. O exemplo do projeto usa Python, SQLite em memória e credenciais fictícias. Não representa uma aplicação pronta para produção.

## Vulnerabilidade, ameaça e risco

- **Ativo:** algo que precisa de proteção, como uma aplicação, conta, servidor, dado ou serviço.
- **Vulnerabilidade:** fragilidade que pode permitir um resultado indesejado. Exemplo: entrada do usuário concatenada a uma consulta SQL de autenticação.
- **Ameaça:** circunstância ou agente capaz de causar dano. Exemplo: alguém tentar explorar essa consulta para obter acesso indevido.
- **Risco:** possibilidade de uma ameaça explorar uma fragilidade e causar consequências no contexto real. Depende da probabilidade e do impacto, não apenas da existência do defeito.
- **Controle:** medida que reduz a probabilidade ou as consequências, como parametrização, menor privilégio ou recuperação testada.
- **Risco residual:** o que permanece após os controles; não desaparece porque um teste passou.

Analogia: uma fechadura defeituosa é uma vulnerabilidade; a possibilidade de alguém tentar entrar é uma ameaça; o risco depende do acesso à porta, dos bens protegidos e das demais proteções. A analogia não substitui evidências técnicas.

## Tríade CIA

CIA significa *Confidentiality, Integrity, Availability*. Em português:

| Propriedade | Pergunta orientadora | Exemplo de consequência |
|---|---|---|
| Confidencialidade | Quem pode conhecer os dados? | Leitura não autorizada de informações |
| Integridade | Quem pode modificar dados ou decisões? | Alteração indevida de registros ou da decisão de autenticação |
| Disponibilidade | O serviço está acessível quando necessário? | Interrupção de uma função importante |

Avaliar cada consequência separadamente. Um bypass demonstrado não comprova, sozinho, leitura de toda a base, alteração arbitrária ou indisponibilidade. Registrar tais consequências como hipóteses se não houver evidência.

## Evidência não é hipótese

**Evidência estática** é o que foi observado em código ou configuração, com localização verificável. **Evidência dinâmica** é o comportamento registrado em uma execução real. **Hipótese** é uma explicação ou consequência ainda dependente de confirmação.

Exemplo de redação disciplinada:

- “A função observada interpola entrada na instrução SQL”: conclusão estática, se o trecho foi realmente lido.
- “O teste retornou um usuário com credenciais inválidas”: evidência dinâmica, somente se ocorreu e foi registrada.
- “Se essa função estiver exposta sem proteção, poderia permitir acesso indevido”: hipótese condicional; exposição e caminho precisam ser verificados.

Não inventar execução, contagem de testes, saída, versão instalada, número de linha, screenshot ou incidente. Usar “não executado” e “não verificado” sempre que necessário.

## SQL injection e a correção principal

SQL injection ocorre quando uma entrada influencia a estrutura de uma instrução SQL, em vez de ser tratada apenas como dado. A CWE-89 descreve essa classe de fraqueza. Referência: [CWE-89](https://cwe.mitre.org/data/definitions/89.html).

Consultas parametrizadas separam a instrução dos valores enviados ao banco. No SQLite do laboratório, `?` representa um valor e a tupla é passada separadamente ao driver. Não substituir esse mecanismo por concatenação, interpolação ou uma blacklist de caracteres. Validação de entrada é complementar. Nomes dinâmicos de tabelas ou colunas não são valores: preferir estrutura fixa ou mapeamento por lista permitida. Referência: [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).

A aula mantém senhas fictícias em texto claro apenas para isolar SQLi. Não reutilizar esse padrão em produção. Uma futura autenticação real exige revisão específica de armazenamento de senhas, sessões, autorização, transporte e recuperação de contas; esses aspectos não ficam resolvidos pela parametrização.

## CWE, ATT&CK e CVSS não são intercambiáveis

- **CWE-89:** classifica a fraqueza de construção de comandos SQL. Não é um identificador de incidente nem uma CVE específica.
- **MITRE ATT&CK T1190 — Exploit Public-Facing Application:** descreve exploração de aplicação ou sistema acessível pela internet para acesso inicial (*Initial Access*). É uma referência comportamental, não sinônimo de SQLi. Só relacionar ao projeto condicionalmente, quando exposição pública e caminho de acesso inicial estiverem presentes. O exemplo local isolado não demonstra T1190. Referência: [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/).
- **CVSS:** não é utilizado neste projeto. Não apresentar a matriz abaixo como pontuação ou vetor CVSS.

## Avaliação qualitativa de risco: matriz 3x3

Esta é uma convenção educativa do projeto, não uma matriz oficial da OWASP, MITRE ou DIO. A severidade corresponde à prioridade contextual resultante dos dois eixos.

**Probabilidade:** baixa quando o caminho é restrito e controles verificados criam barreiras efetivas; média quando o caminho é plausível, mas depende de condições relevantes; alta quando é alcançável com poucas barreiras e há evidência forte ou reprodução.

**Impacto:** baixo para consequência limitada e reversível em ativo pouco crítico ou com dados fictícios; médio para acesso ou alteração de alcance limitado ou interrupção recuperável de função importante; alto para dados sensíveis, alteração crítica ou perda relevante de serviço sustentada pelo contexto.

| Probabilidade ↓ / Impacto → | Baixo | Médio | Alto |
|---|---|---|---|
| Baixa | Baixa | Baixa | Média |
| Média | Baixa | Média | Alta |
| Alta | Média | Alta | Alta |

Justificar exposição, dados, controles e alcance. A confiança é registrada à parte, conforme a qualidade da evidência. Informação ausente significa avaliação pendente ou provisória com premissas; não significa automaticamente risco baixo.

**Exemplo hipotético:** caso um bypass seja reproduzido em um laboratório isolado, sem dados reais nem efeitos externos, pode-se justificar probabilidade alta dentro daquele laboratório e impacto baixo; a matriz resulta em severidade média. Isso não é resultado de teste deste documento. Se houver dados sensíveis e exposição pública, reavaliar os eixos em outro cenário, sem transportar a classificação automaticamente.

## Boas práticas para esta análise

1. Confirmar autorização e escopo antes de agir. Fazer uma pergunta por vez.
2. Inventariar ativos, exposição, dados e controles antes de atribuir severidade.
3. Preferir laboratório isolado, dados fictícios e testes reversíveis.
4. Aplicar menor privilégio e separar o ambiente vulnerável do uso real.
5. Revisar atualizações, configurações, logs e recuperação conforme o ambiente; não presumir seu estado.
6. Não incluir senhas, tokens ou dados pessoais em relatórios ou capturas.
7. Revisar o código dos testes antes de executar e limitar efeitos ao escopo autorizado.
8. Usar relatório padronizado e testes de regressão locais para comparar antes/depois.
9. Revalidar após a mudança; registrar risco residual e partes não avaliadas.
10. Nunca prometer segurança total. Um teste demonstra somente o comportamento verificado nas condições descritas.

## Melhoria aplicada ao processo

O par **relatório padronizado + regressão local** conecta uma afirmação a uma evidência repetível. O relatório registra localização, hipótese, risco, correção e resultado; a regressão verifica login legítimo, credenciais inválidas e o vetor adversarial avaliado. Consultar `skills/vulnerability-analysis/SKILL.md` para o modelo e `docs/roteiro-demonstracao.md` para conduzir a apresentação.

## Fontes oficiais e como utilizá-las

- [OWASP — SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html): fundamenta a separação entre instruções e valores e as defesas contra SQLi.
- [MITRE CWE — CWE-89](https://cwe.mitre.org/data/definitions/89.html): fundamenta a classificação da fraqueza de SQL injection.
- [MITRE ATT&CK — T1190](https://attack.mitre.org/techniques/T1190/): delimita o cenário de exploração de aplicações públicas para acesso inicial.

Essas referências não certificam o projeto. Conferir a versão vigente quando a análise depender de detalhes mutáveis e manter a distinção entre conteúdo da fonte e decisões locais da matriz.
