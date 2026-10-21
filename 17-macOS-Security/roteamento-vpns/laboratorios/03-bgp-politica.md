# Lab 03 — BGP e política

Crie dois upstreams hipotéticos, seus prefixos autorizados, maximum-prefix,
LOCAL_PREF de saída e communities. Classifique anúncios sintéticos como aceitar,
rejeitar por prefixo, rejeitar por comprimento ou alertar por RPKI Invalid.

**Aceite:** nenhum `permit any`, seu próprio prefixo é bloqueado na entrada e a
mudança possui canário, contadores e rollback.
