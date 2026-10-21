# Respostas orientativas

## Correlação da fixture

Os eventos `req-7f2` ligam autenticação, aplicação, DNS, flow e endpoint por
chaves independentes. O IP `198.51.100.27` isolado não identifica uma pessoa;
ele é apenas parte da sessão sintética. A ação administrativa exige correlação
com conta, dispositivo e request ID.

## NAT/CGNAT

Sem porta de origem, protocolo, instante/fuso e mapeamento válido, múltiplos
assinantes ou dispositivos continuam plausíveis. Mesmo com o mapeamento, a
conclusão alcança conectividade/assinatura, não necessariamente autoria humana.

## Lacuna

Interrupção de EDR perto do incidente pode ser falha, manutenção ou adulteração.
Procure saúde do agente, eventos centrais e sequência anterior; preserve a
hipótese alternativa.

## Confiança

Alta confiança requer fontes independentes e coerentes. “Mesmo IP” ou “mesma
ferramenta” sozinho permanece baixo. Roubo de credencial e sessão deve ser
considerado antes de atribuir ação ao titular da conta.

## Privacidade

Colete somente o necessário ao incidente, restrinja acesso, registre consultas,
aplique retenção e envolva jurídico/privacidade para comunicação obrigatória.

