# 17 — Advanced Audit Policy, Sysmon e evidência

Advanced Audit Policy oferece subcategorias granulares. Sysmon, componente
Sysinternals, registra telemetria adicional conforme configuração. Ele não
analisa ou bloqueia por si só.

## Engenharia de evento

Pergunta → fonte/provider → evento/campos → volume → filtro/enriquecimento →
retenção → detecção → playbook → teste → revisão.

## Sysmon

Configuração deve declarar schema version, includes/excludes justificadas e
changelog. Excluir ruído sem hipótese pode apagar sinal. Instalação roda como
serviço/driver privilegiado: use binário oficial assinado e lab.

## PowerShell

Script block/module/transcription ampliam visibilidade, mas podem registrar
conteúdo sensível. Controle acesso aos logs e ensine scripts a não transportar
segredos em texto.

## Tempo e integridade

Linha do tempo empresarial depende de sincronização de tempo, timezone/UTC,
sequência e preservação. O módulo de redes cobrirá distribuição/coleta.

## Exercício

Escreva configuração Sysmon mínima para fixtures em audit lab, estime volume e
valide XML; não instale no host principal.

