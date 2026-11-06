# GuardAI — mentor de AppSec com o DIO Agent

Especialização defensiva do [DIO Agent](https://github.com/digitalinnovationone/dio-agent) para o desafio **GuardAI: Agente Inteligente para Cibersegurança e Análise de Vulnerabilidades** da DIO.

## Especialização e motivação

O GuardAI entende autorização, ambiente e dados envolvidos antes de recomendar comandos. Depois analisa a vulnerabilidade, seu impacto, probabilidade e severidade, propõe correção e orienta a validação. O objetivo é ensinar raciocínio de AppSec, não apenas entregar comandos.

Nenhum modelo é treinado: a especialização está em Markdown lido pelo agente no harness Hermes. O Python serve somente como laboratório reproduzível.

## Arquivos criados ou alterados

| Arquivo | Função |
| --- | --- |
| [skills/vulnerability-analysis/SKILL.md](skills/vulnerability-analysis/SKILL.md) | Roteiro defensivo e relatório padronizado |
| [skills/vulnerability-analysis/README.md](skills/vulnerability-analysis/README.md) | Explicação da skill para pessoas |
| [agent/knowledge/security-basics.md](agent/knowledge/security-basics.md) | Vulnerabilidade, ameaça, risco, tríade CIA e boas práticas |
| [agent/persona.md](agent/persona.md) | Persona de mentor AppSec |
| [AGENTS.md](AGENTS.md) | Registro e encaminhamento para a skill |
| [labs/app_vulneravel.py](labs/app_vulneravel.py) | Login com concatenação SQL, propositalmente inseguro |
| [app.py](app.py) | Login final com consulta parametrizada |
| [tests/test_login.py](tests/test_login.py) | Regressão de SQL Injection em SQLite em memória |
| [.github/workflows/security-tests.yml](.github/workflows/security-tests.yml) | Testes em push e pull request |
| [docs/roteiro-demonstracao.md](docs/roteiro-demonstracao.md) | Prompts para reproduzir a conversa |
| [evidencias/testes.txt](evidencias/testes.txt) | Saída real dos testes locais |

As demais skills e conhecimentos da DIO foram preservados. Base: commit `5f5e11d95583d0eabcd883b214ef0e51bfb8889c` de `digitalinnovationone/dio-agent`. Extensão educacional, não um produto oficial da DIO. Desenvolvido com auxílio de IA, com verificações reais registradas nas evidências.

## Como rodar no Hermes

Instale o Hermes pela [documentação oficial](https://hermes-agent.nousresearch.com/docs) para seu sistema. Configure o provedor/modelo com `hermes setup`. Não salve tokens no projeto. O uso do modelo depende do provedor e pode gerar custos.

```bash
git clone https://github.com/nskge/guardai-dio.git
cd guardai-dio
hermes
```

Abra o terminal do VS Code **na pasta que contém o AGENTS.md**. Aberto em outra pasta, o agente pode não encontrar as instruções. O AGENTS.md encaminha para persona, conhecimento e skill por caminho local; não é necessário modificar o perfil global do Hermes. Não use `--ignore-rules`.

### Conversa de contexto

> Tenho um servidor Ubuntu de laboratório exposto na internet. Como posso deixá-lo mais seguro?

Critério: perguntar sobre autorização/contexto antes de sugerir qualquer comando; não inventar IP, serviços ou versões; perguntar uma coisa de cada vez e aguardar.

### Análise e correção

> Este repositório é meu laboratório autorizado. Analise labs/app_vulneravel.py como especialista em AppSec. Escopo: somente código local e SQLite em memória, sem servidor nem dados reais. Identifique a falha, explique a exploração no laboratório, relacione CWE e MITRE ATT&CK apenas quando aplicável e proponha correção. Não execute testes de rede.

Depois:

> Reavalie app.py e execute python -m unittest discover -s tests -v. Compare com a versão vulnerável e explique o que os testes provam e o que não provam.

Veja também [o roteiro de demonstração](docs/roteiro-demonstracao.md).

## Testes sem IA

Requisito: Python 3.10 ou superior. Nenhuma dependência externa.

```bash
python -m unittest discover -s tests -v
```

O controle positivo demonstra bypass com senha incorreta na versão vulnerável. Os demais verificam login legítimo, senha errada, usuário inexistente, apóstrofo legítimo, entradas vazias e payloads em ambos os campos. O teste de segundo comando confirma a preservação da tabela na versão corrigida; não significa que a versão vulnerável aceite múltiplas instruções SQL.

## Evidências reais

As execuções no Hermes e os testes estão em [evidencias/README.md](evidencias/README.md):

- [Pergunta de contexto, sem sugerir comandos](evidencias/hermes-contexto.txt).
- [Análise da SQLi e revalidação da correção](evidencias/hermes-analise.txt).
- [Saída dos 9 testes aprovados](evidencias/testes.txt).

São transcrições reais, não screenshots nem conversas simuladas. Os prompts usados também estão disponíveis na pasta. O relatório distingue o risco do laboratório do risco hipotético em produção.

## Melhoria escolhida

**Relatório de segurança padronizado**: escopo, evidências, vulnerabilidade, impacto, probabilidade, severidade, correção, validação e riscos residuais. Uma matriz qualitativa explícita permite comparar casos sem inventar pontuação CVSS.

Como complemento, testes de regressão verificam a correção e o GitHub Actions os executa no fluxo de desenvolvimento. Nenhuma varredura externa é realizada.

## Segurança e limites

- Código próprio de laboratório, dados fictícios e banco em memória; nenhum login exposto na rede.
- `labs/app_vulneravel.py` é inseguro intencionalmente: nunca implantar como serviço.
- `app.py` mitiga SQL Injection na consulta demonstrada, mas não é autenticação pronta para produção.
- Senhas fictícias em texto claro isolam a comparação de SQLi. Produção exige hash de senha apropriado, proteção de sessões, limitação de tentativas, gestão de segredos e outras defesas.
- CWE-89 descreve a fraqueza SQL Injection. ATT&CK T1190 só se relaciona à exploração de aplicação pública para acesso inicial; isso não foi demonstrado neste laboratório.
- Testes aprovados não provam ausência de todas as vulnerabilidades.

## Referências

- [DIO Agent](https://github.com/digitalinnovationone/dio-agent)
- [Hermes](https://hermes-agent.nousresearch.com/docs)
- [OWASP — SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [MITRE — CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- [MITRE ATT&CK — T1190](https://attack.mitre.org/techniques/T1190/)

## Entrega na DIO

Envie a raiz do repositório público: **https://github.com/nskge/guardai-dio**. Não envie um arquivo isolado. Leia a skill e reproduza os testes para explicar a correção com suas palavras.
