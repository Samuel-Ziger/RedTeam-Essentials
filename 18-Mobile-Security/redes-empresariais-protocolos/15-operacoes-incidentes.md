# 15 — Ciclo de mudança e resposta a incidentes

Mudança normal requer objetivo, impacto, dependências, diff, teste, janela,
comunicação, validação e rollback. Emergencial reduz tempo, não evidência nem
revisão posterior. Mudanças pequenas e canários reduzem blast radius.

Resposta a incidente de rede:

1. declarar impacto e coordenador;
2. preservar acesso/evidência e linha do tempo;
3. conter com mudança mínima reversível;
4. restaurar serviço e validar do ponto de vista do usuário;
5. erradicar causa quando compreendida;
6. comunicar fatos e incertezas;
7. fazer postmortem sem culpa e rastrear ações.

Evite reiniciar tudo ou limpar logs no início. Capture configuração, estado de
vizinhos/rotas, contadores, telemetria e mudanças com horário. Privacidade e
cadeia de custódia dependem do contexto.
