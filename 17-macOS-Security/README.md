# 17 - Segurança de macOS

> Auditoria e resposta defensiva em endpoints macOS próprios ou gerenciados.
> Este módulo não ensina bypass de TCC, malware ou persistência ofensiva.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Analistas de endpoint, DFIR e Purple Team. |
| Pré-requisitos | Módulos 00 e 05; administração básica de macOS. |
| Tempo estimado | 6 horas de leitura e 4 horas em máquina de teste. |
| Ambiente | Mac/VM autorizado, sem dados pessoais, ou estudo conceitual offline. |
| Evidência final | Baseline sanitizada, hipótese de detecção e plano de resposta. |
| Critério de conclusão | Explicar cinco controles/artefatos e registrar cleanup. |

## Controles e superfícies

- **SIP e Signed System Volume:** protegem componentes do sistema; não devem ser
  desabilitados para facilitar exercícios.
- **Gatekeeper, notarização e XProtect:** compõem camadas de confiança de código;
  uma assinatura válida não equivale a software benigno.
- **TCC:** controla acesso a câmera, microfone, contatos e Full Disk Access.
- **FileVault e Secure Enclave:** reduzem exposição de dados em repouso.
- **MDM:** distribui configurações, certificados, atualizações e inventário;
  perfis excessivos também ampliam impacto administrativo.

## Artefatos de triagem

Colete de forma proporcional: unified logs, quarantine attributes, LaunchAgents
e LaunchDaemons, itens de login, extensões, perfis MDM e histórico de processos
do EDR. Preserve timestamps e hashes; não copie Keychain ou dados pessoais sem
necessidade e autorização explícitas.

## Exercício seguro

Em um Mac de teste, inventarie somente metadados de itens de login e agentes.
Classifique cada entrada como sistema, software conhecido, desconhecida ou
necessita contexto. Proponha uma consulta de detecção e um falso positivo.

## Cleanup

O inventário não deve alterar controles. Remova apenas arquivos derivados e
confirme que SIP, Gatekeeper, FileVault, TCC e perfis permaneceram inalterados.

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Como instalar e usar o PGP no MacOS da Apple e ter muito mais privacidade!!](https://www.youtube.com/watch?v=wF31ZbACEIc) — **Tribo Tecno**.
2. [Curso Apple Mac - Navegação Privada](https://www.youtube.com/watch?v=zxLAYaY4gm8) — **Doctor Apple**.
3. [Curso Apple Mac - Navegar com Segurança no Safari](https://www.youtube.com/watch?v=7P3n1Fadq5M) — **Doctor Apple**.
4. [Como melhorar a proteção do Mac](https://www.youtube.com/watch?v=BQgAL7ge0Bo) — **Canal da Lu - Magalu**.
5. [4 Pilares Importantes de Segurança no Mac - Passo a Passo!](https://www.youtube.com/watch?v=EDvnYX4KmoI) — **Super Apple**.
