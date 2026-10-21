# 10 — Engenharia de Group Policy

GPO combina Group Policy Container no diretório e template no SYSVOL. Versões
devem permanecer consistentes. Central Store fornece ADMX/ADML versionados para
edição; templates devem corresponder aos produtos administrados.

## Design

- GPO pequena por responsabilidade e owner;
- nome/version/changelog claros;
- escopo por OU e security filtering previsíveis;
- WMI filter somente quando custo/necessidade justificam;
- loopback apenas para dispositivos de uso especial;
- backup e relatório XML/HTML antes de mudar;
- teste de Resultant Set of Policy por persona/dispositivo;
- rollback e remoção de links obsoletos.

## Evite

Default Domain Policy como depósito geral; permissões inconsistentes entre GPC
e GPT; script com segredo; filtros lentos; `Enforced` para resolver desenho;
mudança direta sem staging.

## Laboratório offline

Produza três GPOs como manifests de settings e calcule precedência em fixture.
Não há domínio nem aplicação real antes de redes.

