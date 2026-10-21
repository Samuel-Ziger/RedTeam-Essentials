# 06 — Deployment rings, Autopilot e Intune

Autopilot registra identidade de hardware e orienta provisionamento; Intune
gerencia dispositivos/aplicativos/políticas. Ambos dependem de identidade e
conectividade, portanto o curso modela perfis e gates sem onboarding real.

## Anéis

| Anel | Perfil | Gate de saída |
|---|---|---|
| 0 | engenharia/lab | build, setup e rollback passam |
| 1 | TI voluntária | apps/segurança/telemetria saudáveis |
| 2 | piloto por persona | SLO e compatibilidade por workload |
| 3 | amplo | taxa de falha abaixo do limite |
| 4 | crítico | janela e aprovação específicas |

## Perfis e conflitos

Cada setting precisa de autoridade. GPO, MDM, script e configuração local podem
competir. Documente precedência/co-management e detecte drift; não aplique o
mesmo controle por mecanismos independentes sem desenho.

## Reset e reuso

Autopilot Reset/Fresh Start/Wipe têm efeitos distintos. Proteja BitLocker keys,
dados, ownership e registro do dispositivo antes de reaproveitar/aposentar.

## Exercício

Projete anéis e perfis para três personas. Defina métrica, halt condition,
rollback e comunicação; não conecte a tenant.

