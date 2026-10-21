# 03 — Tempo, fuso e clock skew

Timeline sem tempo normalizado cria causalidade falsa. Preserve o timestamp
original, fuso/offset, precisão, fonte do relógio, momento de ingestão e
transformação para UTC.

## Tipos de tempo

- tempo do evento no dispositivo;
- tempo de recebimento pelo serviço;
- tempo de ingestão no SIEM;
- tempo escrito no arquivo;
- tempo corrigido pelo analista.

Nunca substitua o original. Acrescente `normalized_at` e `clock_offset_ms` com a
justificativa.

## Medir skew

Compare evento conhecido entre duas fontes, estado NTP e métricas do agente.
Uma janela de correlação deve considerar precisão e atraso. Ampliar demais gera
falsos vínculos; estreitar demais perde eventos.

## Horário de verão e formatos

Prefira ISO 8601 com offset, por exemplo `2026-10-01T15:04:05-03:00`, e normalize
para `Z`. Epoch exige unidade explícita. Strings sem fuso são ambíguas.

## Ordem versus causalidade

Mesmo timestamps próximos não provam causa. Use IDs de requisição, sequência de
protocolo e evidência do processo para sustentar relações.

## Prática

Normalize cinco eventos sintéticos com offsets diferentes. Registre tolerância
e mostre como um skew de 90 segundos mudaria a conclusão.

