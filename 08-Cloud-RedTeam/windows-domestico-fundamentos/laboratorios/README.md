# Laboratórios e gates de progressão

Os laboratórios não são listas opcionais. Cada um valida um conjunto de
capítulos e libera o próximo na aplicação de estudos. Use somente a VM e dados
sintéticos. O adaptador permanece desconectado durante os experimentos; uma
janela anterior e controlada de provisionamento/atualização não faz parte do lab.

| Gate | Laboratório | Classe | Resultado verificável |
|---:|---|:---:|---|
| 01 | [Instalação e inventário](01-instalacao-inventario.md) | D | baseline suportada e JSON sanitizado |
| 02 | [Arquivos e permissões](02-arquivos-permissoes.md) | B/C | matriz de acesso e rollback de ACL |
| 03 | [Disco e recuperação](03-disco-recuperacao.md) | C | restore com manifests equivalentes |
| 04 | [Eventos e diagnóstico](04-eventos-diagnostico.md) | A | timeline e hipóteses refutáveis |
| 05 | [Defender e integridade](05-defender-integridade.md) | A/B | baseline de proteção e scan seguro |
| 06 | [Projeto de recuperação](06-projeto-recuperacao.md) | C | computador recuperável por terceiro |

## Regras comuns

Antes de começar, registre edição/build, conta, privilégio, horário UTC, snapshot,
discos e hipótese. Guarde comandos, saídas sanitizadas, interpretação e hash dos
artefatos. Captura de tela pode complementar, mas não substituir evidência
estruturada.

Pare se o alvo não for inequívoco, se a recovery key necessária não estiver
disponível, se o snapshot falhar ou se aparecer dado real. Elevação só ocorre no
passo identificado. Nunca desative proteção, limpe logs, use imagem modificada,
contorne OOBE/licença ou altere disco do sistema para cumprir um roteiro.

O laboratório termina somente depois do cleanup e da comparação com a baseline.
Se o rollback falhar, restaure o snapshot e registre a falha; não improvise no
estado parcialmente modificado.

## Estrutura da evidência

Crie uma pasta por gate:

```text
C:\RTE-Lab\evidencias\lab-0N\
├── plano.md
├── estado-inicial.json
├── comandos.txt
├── resultado.json
├── validacao.md
└── cleanup.md
```

Segredos, e-mail, nomes reais, hostname, serial e chaves de recuperação ficam
fora. Um colega deve avaliar o gate usando somente essa pasta e o runbook.

## Política de repetição

Falhou um critério? Preserve a evidência, identifique o erro de método, reverta e
repita apenas o gate afetado. Não edite o resultado antigo para fazê-lo parecer
correto. Comparar a primeira e a segunda execução demonstra aprendizagem.
