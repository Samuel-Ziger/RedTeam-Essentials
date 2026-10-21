# Runbook do Study Desk

## Objetivo

Diagnosticar a aplicação local sem apagar dados na tentativa e sem solicitar
informação pessoal. Preserve uma exportação quando a interface ainda permitir.

## Linha de base

Na pasta `projetos/study-desk`:

```bash
npm test
python3 -m http.server 8000
```

Abra `http://127.0.0.1:8000`, não o arquivo diretamente. Confirme:

1. console sem erro no carregamento;
2. cadastro, filtro e exclusão funcionam;
3. recarregar preserva a sessão;
4. exportar gera JSON com `schemaVersion: 1`;
5. teclado alcança todas as ações;
6. zoom de 400% mantém reflow e leitura.

## Evidência mínima

Registre versão do navegador/Node, URL completa, passos, resultado esperado,
resultado real e primeira mensagem. Não anexe o conteúdo real das sessões.
Prefira fixture sintética ou exportação sanitizada.

## Matriz de falhas

| Sintoma | Verificação segura | Recuperação |
|---|---|---|
| página sem estilo/script | confirme HTTP 200 e caminhos relativos | sirva a raiz correta |
| dados não carregam | aviso de modo volátil, console e chave `study-desk:sessions:v1` | preserve a string original; exporte a sessão volátil antes de fechar; valide em cópia |
| falha ao salvar | quota/permissão/modo privado | exporte, libere espaço conscientemente, reimporte |
| importação recusada | tamanho, JSON, versão, campos e datas | corrija uma cópia; preserve original |
| versão futura | leia `schemaVersion` sem forçar alteração | use versão compatível ou migração documentada |
| interface lenta | número de sessões e gravação/filtragem no profiler | reduza fixture; meça antes de otimizar |
| foco/teclado falha | sequência Tab/Shift+Tab e zoom | registre controle e estado exatos |
| tema não persiste | acesso à chave de tema | funcionalidade principal continua em tema claro |

## Corrupção local

Não limpe todo `localStorage` como primeiro passo. Copie o valor da chave de
sessões, calcule seu hash se for evidência e teste `parseDocument` numa cópia.
Se o documento for irrecuperável, só remova a chave após autorização explícita e
com backup. Limpar dados do site também pode afetar outras aplicações do origin.

## Quota

`localStorage.setItem` pode lançar erro. Reproduza com perfil descartável e dados
sintéticos. Confirme que a interface informa falha e que o estado anterior volta
após reload. Não tente preencher disco ou perfil principal.

## Rollback de versão

O artefato é estático. Para voltar:

1. preserve exportação compatível;
2. sirva a versão anterior conhecida;
3. importe somente schema suportado;
4. execute smoke test e compare invariantes;
5. documente por que a versão nova foi retirada.

Código antigo não deve sobrescrever documento de versão futura. Uma migração
precisa ser testada nos dois sentidos previstos ou oferecer exportação de
recuperação.

## Encerramento

Um incidente termina quando há causa, impacto, recuperação verificada, teste que
reproduz a falha e ação preventiva com responsável. “Limpei o navegador” não é
diagnóstico suficiente.
