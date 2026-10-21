# 28 — Engenharia de automação e ferramentas de segurança

Aqui a base de programação vira ferramental operacional: interfaces seguras,
validação de entrada, modo de simulação, logs, formatos de saída, testes e
documentação que permitam auditar cada execução.

## Contrato do módulo

| Campo | Definição |
|---|---|
| Público | Desenvolvimento, automação, AppSec, Red e Blue Team. |
| Pré-requisitos | Módulo `27` e a formação-base `00`–`26`. |
| Tempo estimado | 40–60 horas. |
| Linguagens | Python, Bash, PowerShell e Java. |
| Foco | Engenharia, qualidade e uso autorizado; não automação indiscriminada. |
| Ambiente | Fixtures locais, hosts próprios e laboratório isolado. |
| Evidência final | Ferramenta empacotada, testada, documentada e com saída reproduzível. |
| Critério de conclusão | Ferramenta aprovada nos testes, threat model e demonstração offline. |

## Conteúdo curricular

- [Automação e ferramentas](automacao-e-ferramentas/README.md)
- [Automação de inventário AD](acervo/automacao/ad_recon.sh)
- [Pós-instalação Linux](acervo/automacao/linux_postinstall.sh)
- [Organização de logs](acervo/automacao/organize_logs.ps1)
- [Preparação Windows](acervo/automacao/windows_setup_clean.ps1)
- [Ferramentas Python](acervo/python/LEGADO-PYTHON-TOOLS.md)
- [Ferramentas Java](acervo/java/LEGADO-JAVA.md)

Os utilitários existentes são tratados como estudos de caso: o objetivo é
entender suas decisões, testar seus limites e evoluí-los com segurança.

Próximo: [Módulo 29 — Reconhecimento e OSINT](../29-Reconhecimento-OSINT/README.md).
