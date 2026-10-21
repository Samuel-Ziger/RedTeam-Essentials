# 15 — Defender empresarial, ASR e operação

Microsoft Defender Antivirus protege localmente. Defender for Endpoint adiciona
capacidades de endpoint detection/response, vulnerability management e operação
conforme plano/licença. Onboarding e integração aguardam redes; o desenho de
política, sinais e resposta pode ser feito offline.

## Camadas

- antivirus/behavior/cloud protection;
- tamper protection;
- ASR rules;
- network protection (apenas após redes);
- controlled folder access;
- exploit protection;
- EDR e automated investigation conforme serviço;
- security settings management/MDM/GPO com uma autoridade definida.

## ASR

Cada regra tem GUID, modo e compatibilidade. Use warn/audit quando disponível,
analise eventos por persona e trate exclusões como risco com owner/expiração.
Nunca use exclusão global para acelerar rollout.

## Operação

Defina severidade, triagem, device isolation (futuro), coleta, preservação,
remediação, comunicação e fechamento. Teste com simulações oficiais benignas,
não malware.

## Exercício

Modele rollout de três ASR rules por anéis e consultas de evidência local.

