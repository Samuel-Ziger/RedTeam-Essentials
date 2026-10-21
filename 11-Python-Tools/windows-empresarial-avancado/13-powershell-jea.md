# 13 — PowerShell governado, JEA e logging

PowerShell em escala precisa de source control, code review, CI, assinatura,
versão, owner, rollout, rollback e telemetria. Script ad hoc elevado não é
administração em escala.

## Just Enough Administration

JEA usa session configuration e role capability para oferecer cmdlets/funções
limitados, com virtual account ou identidade definida e transcrição. O endpoint
normalmente usa PowerShell remoting; por isso o lab apenas valida arquivos
`.pssc`/`.psrc` localmente, sem registrar endpoint.

## Design de capability

- comandos específicos, não linguagem irrestrita;
- parâmetros e valores limitados;
- funções proxy revisadas;
- nada de executável genérico ou caminho gravável;
- identidade, filesystem e secrets modelados;
- logging, transcript e retenção testados;
- escape paths revisados.

## Logging

Module logging, script block logging e transcription têm cobertura/volume e
podem capturar dados sensíveis. Proteja o destino e não escreva secrets no
pipeline. AMSI integra conteúdo de script a antimalware; não é controle isolado.

## Exercício

Crie role capability que permite somente executar baseline do curso e consultar
serviços. Valide sintaxe e revise caminhos, sem habilitar remoting.

