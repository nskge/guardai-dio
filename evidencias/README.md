# Evidências reais de execução

Os arquivos desta pasta registram execuções reais no Hermes CLI e no Python. Não são respostas simuladas nem prints montados. Os arquivos TXT são transcrições, não capturas de tela.

## 1. Contexto antes de comandos

- Entrada: [prompt-contexto.txt](prompt-contexto.txt)
- Saída: [hermes-contexto.txt](hermes-contexto.txt)
- Execução: `hermes chat --oneshot -Q --max-turns 8 --run-budget 180 --query-file evidencias/prompt-contexto.txt`
- Resultado observado: o agente informa que ainda não avaliou a configuração e pergunta quais serviços precisam ficar acessíveis pela internet. Não fornece comandos. É evidência da primeira pergunta, não de uma avaliação completa do servidor. Nenhum servidor real foi testado.

## 2. Análise e revalidação AppSec

- Entrada: [prompt-analise.txt](prompt-analise.txt)
- Saída: [hermes-analise.txt](hermes-analise.txt)
- Execução: `hermes chat --oneshot -Q --max-turns 15 --run-budget 240 --query-file evidencias/prompt-analise.txt`
- Resultado observado: leitura da skill e do código, explicação de SQLi, CWE-89, T1190 condicional, avaliação de risco e revalidação com 9 testes aprovados. O agente avalia a correção que já está em `app.py`; não se alega que esse processo escreveu a correção.

## 3. Testes executados diretamente

- Saída: [testes.txt](testes.txt)
- Comando: `python -m unittest discover -s tests -v`
- Resultado: 9 testes aprovados, inclusive controle positivo que demonstra a falha intencional na cópia vulnerável.
- Ambiente local: Python 3.14.9 em Windows. O CI usa Python 3.12 em Ubuntu.

## Como obter seus prints

Abra o terminal do VS Code na raiz do projeto e reproduza os comandos acima, sem redirecionamento para arquivo. Capture a pergunta de contexto, a análise e o resultado dos testes. Não exponha tokens ou informações pessoais. O [roteiro](../docs/roteiro-demonstracao.md) detalha a demonstração.

As respostas de IA podem variar; os arquivos Markdown orientam o comportamento, não constituem uma barreira técnica de segurança. Os testes da aplicação são determinísticos e não dependem do modelo.
