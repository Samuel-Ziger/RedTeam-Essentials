# Respostas orientativas

Use depois de tentar explicar com suas palavras. Estas respostas mostram o nível
de precisão esperado; não substituem a evidência da sua VM.

## “Windows 11” identifica o sistema?

Não completamente. Edição, versão, build/revisão, arquitetura e canal influenciam
recursos, compatibilidade e suporte. O inventário precisa registrar essas camadas
e consultar o ciclo de vida atual.

## Secure Boot, TPM e BitLocker fazem a mesma coisa?

Não. Secure Boot valida componentes na cadeia de inicialização; TPM oferece
medições e proteção de chaves; BitLocker cifra volumes e pode usar o TPM para
liberar material de chave. Nenhum substitui backup.

## Por que não contornar OOBE ou requisito de hardware?

O contorno cria uma instalação fora do fluxo suportado e prejudica manutenção,
segurança e reprodutibilidade. Use edição, licença, hardware e provisionamento
oficiais compatíveis com o laboratório.

## Extensão prova o tipo de arquivo?

Não. Ela orienta associação. Conteúdo/formato, hash, assinatura e origem fornecem
evidências diferentes. `documento.pdf.exe` ilustra por que exibir extensões é útil.

## `Healthy` prova que o conteúdo do volume está íntegro?

Não. É um estado reportado pelo subsistema. Integridade de dados exige leitura,
manifesto, hash e restauração testada conforme o objetivo.

## ReadOnly e ACL de leitura são equivalentes?

Não. ReadOnly é atributo; ACL é usada na autorização com token, ACEs e herança.
A mesma conta pode contornar comportamentos do atributo, mas não recebe um
direito ausente apenas porque o atributo mudou.

## UAC transforma administrador em usuário comum?

Não. Em configuração comum, aplicações usam token filtrado e elevação gera
consentimento ou credencial para um contexto administrativo. A recomendação de
conta cotidiana comum permanece.

## Serviço parado está quebrado?

Não necessariamente. Serviços sob demanda ou acionados por evento ficam parados
por design. Compare modo de início, dependências, eventos e função esperada antes
de mudar estado.

## Assinatura válida significa software seguro?

Ela vincula o artefato ao signatário e detecta alteração posterior no contexto
da validação. Não prova ausência de vulnerabilidade, intenção benigna, licença ou
adequação ao sistema.

## Por que não usar `Win32_Product` para inventário rotineiro?

Além de cobertura limitada a produtos MSI, a consulta pode acionar verificações
de consistência/reparo e ter custo alto. Use fontes adequadas e documente lacunas.

## Por que não limpar o Registro?

Entradas consideradas “órfãs” raramente geram benefício mensurável ao serem
removidas, e classificação errada quebra aplicativos ou servicing. Edite apenas
uma configuração documentada, com exportação e rollback.

## ID de evento identifica a causa?

Não. O ID precisa de provider, canal, horário e payload. Mesmo assim, o evento é
uma observação; causalidade requer contexto, mecanismo e teste discriminador.

## Snapshot ou sincronização é backup?

Isoladamente, não. Snapshot depende do ambiente; sincronização pode replicar
exclusão e corrupção. Backup precisa de independência, retenção e restore testado.

## Por que `robocopy` retornou 1 e o script não falhou?

Os códigos são bitmasks: valores de 0 a 7 podem representar sucesso com cópias
ou diferenças; 8 ou mais indicam falha. Ainda é preciso validar conteúdo.

## Quick scan recente prova que o computador está seguro?

Não. É uma observação limitada por escopo, engine, inteligência e momento.
Segurança depende também de atualização, origem de software, identidade, firmware,
configuração e backup.

## Execution Policy é fronteira de segurança?

Não. Ajuda a controlar condições de execução e reduzir acidentes, mas pode ser
contornada por quem já consegue executar código. Origem, revisão, assinatura,
privilégio mínimo e isolamento continuam necessários.

## DISM, SFC e CHKDSK devem rodar para qualquer problema?

Não. Eles verificam objetos diferentes e modos de reparo alteram estado. Use-os
quando a hipótese envolver Component Store, arquivos protegidos ou filesystem,
com backup, logs e validação do sintoma original.

## Se o problema sumiu após reiniciar, a causa foi provada?

Não. Reiniciar altera processos, caches, locks e fases de servicing. Ele demonstra
recuperação temporária; a causa permanece incerta sem evidência adicional.
