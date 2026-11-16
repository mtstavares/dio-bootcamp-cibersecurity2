# Laboratório educativo: ransomware e keylogger simulados

Projeto didático em Python para observar dois comportamentos em ambiente local. A criptografia atua somente sobre três nomes de arquivos fictícios em `laboratorio/dados_demo/`. O registrador grava eventos apenas quando o usuário digita no campo visível da janela; não monitora outros aplicativos nem envia dados pela rede.

## Requisitos e execução

Python 3.10 ou superior e Tkinter. Instale a dependência e inicie a aplicação:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python laboratorio_seguro.py
```

Na janela, use **Preparar exemplos**, digite texto fictício no campo para ver o registro consentido, e experimente **Simular criptografia** e **Restaurar arquivos**. Os arquivos de teste e a chave ficam dentro de `laboratorio/`; não coloque dados reais nesse diretório. A chave é necessária para restaurar os exemplos. O log fica em `laboratorio/logs/eventos_digitacao.jsonl`.

## O que observar

- O simulador cria uma chave Fernet local e criptografa somente `anotacoes.txt`, `clientes_ficticios.csv` e `relatorio.txt` em `dados_demo/`.
- A restauração descriptografa esses arquivos com a chave local. Fernet autentica os dados e rejeita chave/token inválido.
- O registro de teclas tem indicação visível e pode ser desligado pelo checkbox. Os eventos são exibidos na janela e salvos localmente para inspeção.
- `AVISO_SIMULACAO.txt` identifica o exercício; nenhum pagamento ou envio de dados é implementado.

## Defesa e prevenção

Mantenha backups separados e teste a restauração; atualize sistema e aplicativos; use antivírus e firewall; limite permissões de aplicativos; desconfie de anexos e downloads inesperados; e execute análises desconhecidas em uma máquina virtual isolada com snapshot. Em uma investigação, mudanças rápidas em muitos arquivos, extensões novas e processos incomuns podem justificar análise, mas são sinais heurísticos e podem gerar falsos positivos.

## Limites

Este protótipo é uma demonstração, não um antivírus nem uma ferramenta de proteção. A chave local serve apenas para o exercício e não deve ser usada para proteger dados reais. Não há persistência, ocultação, captura global de teclado ou envio por e-mail.
