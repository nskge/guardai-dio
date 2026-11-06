# Roteiro de demonstração — GuardAI / DIO

## Objetivo

Demonstrar análise defensiva guiada por contexto, correção de SQLi e revalidação, sem confundir laboratório com produção. A melhoria escolhida é **relatório padronizado + testes de regressão locais**.

Este documento é um roteiro, não uma transcrição de execução. Prompts, respostas esperadas e critérios abaixo não comprovam resultados. Não foram incluídos logs, screenshots ou avaliações simuladas como se fossem reais.

## Preparação

- Usar uma cópia local do projeto, sem dados ou credenciais reais.
- Abrir `skills/vulnerability-analysis/SKILL.md` e `agent/knowledge/security-basics.md`.
- Conferir se existem `labs/app_vulneravel.py`, `app.py` e `tests/`; se faltar algum item, registrar a pendência e não improvisar saída.
- Manter a cópia vulnerável isolada, sem serviço público ou acesso a banco de produção.
- Explicar que as senhas fictícias em texto claro servem apenas para isolar SQLi; não são recomendação de autenticação real.
- Revisar os testes e efeitos de importação antes de executá-los. A autorização para ler código não autoriza automaticamente executá-lo.

## Cena 1 — Ativar a skill e mostrar contexto primeiro

**Prompt inicial:**

> Leia skills/vulnerability-analysis/SKILL.md e agent/knowledge/security-basics.md. Quero uma análise defensiva do meu projeto GuardAI. Comece pelo contexto e faça uma pergunta de cada vez. Não execute comandos antes de confirmar o escopo e a autorização.

**Comportamento esperado:** perguntar primeiro a informação ausente mais importante, como objetivo ou autorização, e aguardar. Não enviar uma bateria de perguntas. Não iniciar varredura.

Conforme solicitado, informar fatos verdadeiros: responsabilidade pelo laboratório, arquivo autorizado, revisão somente estática ou testes locais permitidos, exposição local, dados fictícios e controles conhecidos. Não usar respostas prontas que não correspondam ao ambiente real.

## Cena 2 — Analisar a cópia vulnerável

Depois de esclarecer contexto e autorização, usar:

> Analise estaticamente labs/app_vulneravel.py. A revisão autorizada se limita a esse arquivo e ao contrato de login necessário para entendê-lo. Não o execute. Mostre o fluxo entre entrada e consulta SQL, com localização verificada. Separe evidência e hipótese e preencha o relatório padronizado da skill. Justifique probabilidade, impacto e severidade pela matriz qualitativa 3x3, que não é CVSS.

**Pontos a observar:**

- O agente lê o arquivo real, em vez de concluir pelo nome.
- Identifica concatenação ou interpolação apenas se presente e explica por que a entrada pode mudar a instrução.
- Relaciona o achado a CWE-89 quando o fluxo observado sustenta isso.
- Não afirma que houve ataque, vazamento ou comprometimento real.
- Distingue impacto do laboratório de eventual impacto em produção.
- Registra a evidência dinâmica como não executada nesta etapa.

**Prompt sobre classificação:**

> Explique por que esse exemplo local não demonstra automaticamente MITRE ATT&CK T1190. Em que condições a associação seria cabível?

**Critério:** T1190 só deve ser considerado condicionalmente se a aplicação estiver acessível pela internet e sua exploração servir como caminho de acesso inicial. Não basta existir SQLi.

## Cena 3 — Explicar a correção sem apagar o controle do exercício

**Prompt:**

> Explique como uma consulta parametrizada separa código SQL de valores. Compare o padrão de labs/app_vulneravel.py com app.py, lendo ambos, sem editar nenhum arquivo. Não proponha blacklist de caracteres como solução principal e não trate as senhas fictícias em texto claro como adequadas para produção.

**Critério:** identificar parâmetros reais enviados separadamente ao driver, e não apenas uma string com aparência de parametrização. Manter a API comparável e a cópia vulnerável como controle didático. Se `app.py` ainda não estiver parametrizado, registrar a correção como pendente; não dizer que está corrigido.

## Cena 4 — Revalidar app.py e executar regressão local

**Prompt:**

> Revalide app.py com o modelo de relatório da skill. Autorizo a leitura de app.py, labs/app_vulneravel.py e dos testes locais e a execução da suíte unittest somente se ela usar SQLite em memória, dados fictícios e não fizer rede nem alterações fora do laboratório. Revise isso antes de rodar. Confirme quais casos existem: login válido, credenciais inválidas, usuário inexistente, apóstrofo literal e tentativa de SQLi. Se faltar cobertura, registre a lacuna, sem editar arquivos nesta etapa.

Com revisão concluída e as condições atendidas, o comando é executado **na raiz do projeto**:

```bash
python -B -m unittest discover -s tests -v
```

**Registro obrigatório:** comando realmente executado, ambiente observado, saída relevante, código de saída, número de testes descobertos, falhas, erros ou testes ignorados. Zero testes não comprova nada. Se o executor usar outro nome para o interpretador, confirmar a disponibilidade e registrar a substituição real. Se não houver ferramenta de execução, dizer “não executado” e pedir a saída real ao estudante.

**Como interpretar:**

- Testes da versão corrigida devem proteger comportamento legítimo e rejeitar a tentativa avaliada.
- Um teste de caracterização pode passar ao confirmar o defeito na cópia vulnerável; suíte aprovada não significa que ambos os arquivos sejam seguros.
- Uma falha deve ser investigada: pode ser defeito funcional, regressão, dependência ou preparação incorreta, não necessariamente SQLi.
- Não gerar um resultado “OK” de exemplo para substituir a execução.

**Prompt de encerramento:**

> Atualize o relatório com as evidências reais desta sessão e compare antes/depois. Indique o que foi corrigido e revalidado, o que continua como hipótese e o risco residual. Não prometa segurança total. Termine com uma pergunta para verificar meu entendimento.

**Conclusão aceitável, somente quando sustentada:** o vetor avaliado foi bloqueado nos testes locais registrados. Não afirmar ausência de todas as vulnerabilidades nem prontidão para produção.

## Cena 5 — Servidor Ubuntu de laboratório: perguntas antes de comandos

Este cenário demonstra postura defensiva; não pressupõe que exista servidor disponível nem que uma sessão remota tenha sido realizada.

**Prompt inicial:**

> Quero revisar a segurança de um servidor Ubuntu de laboratório. Antes de sugerir ou executar qualquer comando, faça uma pergunta de cada vez para entender objetivo, autorização, ativos, exposição, dados, controles e restrições. Não suponha versão, IP, acesso SSH, privilégios ou serviços instalados.

**Sequência de conversa esperada:** usar a próxima pergunta necessária e aguardar a resposta, sem apresentar a lista inteira como uma mensagem ao estudante.

1. Qual é o objetivo da revisão?
2. Você administra esse servidor ou tem autorização explícita?
3. Qual ativo está incluído no escopo?
4. Quais operações são permitidas?
5. Ele é isolado, interno ou acessível pela internet?
6. Que tipos de dados estão presentes?
7. Quais controles de acesso e proteção já existem?
8. Quais consequências de falha precisam ser evitadas?
9. Há restrições de disponibilidade ou horário?

Depois de responder com fatos reais, usar:

> Com o contexto confirmado, proponha apenas a primeira verificação de leitura, explique sua finalidade e quais informações ela pode revelar. Aguarde minha autorização específica antes de executá-la. Não instale ferramentas, não altere firewall, não reinicie serviços e não faça varredura de rede.

**Critério:** somente após a autorização, executar a verificação acordada no servidor correto. Um comando executado na máquina do agente não comprova o estado do Ubuntu remoto. Sem acesso ou autorização, permanecer em plano conceitual e registrar a limitação. Se surgir um novo ativo ou uma ação com efeitos diferentes, voltar à confirmação de escopo.

**Prompt para resultado parcial:**

> Com base apenas no que foi observado, separe fatos de hipóteses e use a matriz 3x3 quando houver dados suficientes. Caso contrário, deixe a classificação pendente. Proponha a próxima verificação sem executá-la.

## Evidências para apresentação e publicação

Se produzir capturas, capturar a tela real durante a demonstração e remover segredos antes de publicar. Não criar imagens que imitem terminal, testes ou análise executada. Um roteiro textual sem captura é preferível a evidência fabricada.

Para cada execução real, registrar:

```text
Cenário e escopo autorizado:
Ambiente observado:
Arquivo/função ou verificação:
Comando realmente executado (ou não executado):
Saída relevante e código de saída:
Quantidade de testes descoberta, se aplicável:
Conclusão sustentada:
Hipóteses e limitações:
Próximo passo autorizado:
```

## Checklist final

- [ ] Skill e base de conhecimento explicitamente carregadas.
- [ ] Perguntas individuais; contexto antes de ação.
- [ ] Análise de `labs/app_vulneravel.py` baseada em leitura real.
- [ ] Consulta parametrizada verificada em `app.py` ou pendência registrada.
- [ ] CWE-89 usada corretamente; T1190 apenas condicional.
- [ ] Matriz qualitativa 3x3 aplicada sem chamar de CVSS.
- [ ] Relatório padronizado preenchido sem inventar dados.
- [ ] Regressão local executada e documentada, ou motivo de não execução explícito.
- [ ] Cenário Ubuntu sem comandos antes das perguntas e autorização específica.
- [ ] Risco residual, limites didáticos e ausência de garantia total declarados.

Referências técnicas oficiais e seus limites de aplicação: `agent/knowledge/security-basics.md`.
