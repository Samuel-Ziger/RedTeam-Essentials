# Automação e ferramentas de segurança

Use os artefatos existentes como estudos de caso de engenharia. Leia o contrato
de cada ferramenta, execute primeiro em modo seguro e acrescente testes antes
de ampliar seu comportamento.

## Sequência

1. Compare padrões de CLI, validação, logs e erros no
   [acervo Python](../acervo/python/LEGADO-PYTHON-TOOLS.md).
2. Revise `hash_identifier.py`, `jwt_analyzer.py`, `port_scanner.py` e
   `subdomain_enum.py` no [diretório Python](../acervo/python/).
3. Compare empacotamento e tipagem com o
   [acervo Java](../acervo/java/LEGADO-JAVA.md) e seu
   [código-fonte](../acervo/java/src/).
4. Estude idempotência e simulação nos scripts
   [Linux](../acervo/automacao/linux_postinstall.sh) e
   [Windows](../acervo/automacao/windows_setup_clean.ps1).
5. Analise saídas reproduzíveis em
   [organize_logs.ps1](../acervo/automacao/organize_logs.ps1) e limites de
   escopo em [ad_recon.sh](../acervo/automacao/ad_recon.sh).

## Projeto

Evolua uma ferramenta escolhida com `--help`, validação estrita, dry-run,
timeout, saída estruturada, logs sem segredos, testes com fixtures e um modelo
de ameaça curto. A demonstração deve usar apenas dados locais.
