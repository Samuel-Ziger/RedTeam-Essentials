# Lab 01 — Instalação suportada e inventário

**Classe: D — instalação/recuperação em clone descartável.**

Este gate valida método, ciclo de suporte, firmware, Setup/OOBE e navegação
administrativa. A instalação é feita somente em VM. Se a edição atual exigir
internet e conta Microsoft no OOBE, use um fluxo oficial compatível ou comece
com uma VM oficial já provisionada; nenhum bypass é permitido.

## Pré-requisitos e critérios de parada

Conclua os capítulos 00–04 e leia os exemplos. Tenha ISO oficial/licenciada ou
de avaliação, hipervisor com snapshots, disco vazio e segundo disco virtual.
Registre hash publicado quando disponível e a URL/data de obtenção.

Pare se houver disco real conectado ao alvo, se a mídia não tiver procedência,
se requisitos não forem atendidos, se a licença não permitir o uso ou se não
for possível criar/restaurar snapshot.

## Objetivo e hipótese

Entregar uma baseline reproduzível que identifique edição, versão/build,
arquitetura, firmware, volumes e proteções sem coletar nome de máquina, conta,
serial ou endereços. Escreva antes: quais partições o Setup deve criar, quais
consultas podem retornar `$null` e o que será considerado instalação concluída.

## Procedimento

1. Crie snapshot `lab01-antes-instalacao` e registre configuração da VM.
2. Inicialize a mídia oficial e identifique o disco vazio por capacidade.
3. Deixe o Setup preparar o primeiro disco. Não formate o disco de dados.
4. Registre finalidade de ESP, MSR, volume do sistema e recuperação.
5. Conclua o OOBE pelo caminho suportado da edição/build. Não capture e-mail.
6. Crie uma conta cotidiana comum, mantendo administração separada.
7. Reinicie duas vezes e confirme que servicing inicial terminou.
8. Verifique edição/build, dispositivos com erro, volumes, Secure Boot e TPM.
9. Execute a partir de `exemplos/`:

```powershell
Set-Location 'C:\RTE-Curso\exemplos'
.\Get-RteLocalInventory.ps1 -AsJson `
  -OutputPath 'C:\RTE-Lab\evidencias\lab-01\inventario.json'
Get-Content 'C:\RTE-Lab\evidencias\lab-01\inventario.json' -Raw |
  ConvertFrom-Json | Out-Null
```

10. Leia o código, confira schema, tipos e unidades. Procure manualmente campos
    proibidos. Calcule SHA-256 e crie snapshot `lab01-instalacao-validada`.

Adapte os caminhos ao local real e registre a adaptação. Não execute script de
diretório desconhecido nem eleve toda a sessão.

## Evidências

- ficha da mídia, licença e requisitos, sem chave de produto;
- diagrama das partições e explicação de cada função;
- decisões do OOBE e privacidade sem identificadores;
- comparação GUI versus PowerShell para edição, build e espaço;
- inventário JSON válido e seu hash;
- tabela `propriedade → valor/ausente/erro → interpretação`;
- prova dos dois snapshots e dos dois reinícios.

## Validação independente

Outra pessoa deve abrir o JSON, confirmar o schema e explicar ao menos cinco
propriedades sem acessar a VM. Ela também verifica por busca textual que não há
hostname, usuário, e-mail, serial, endereço ou recovery key. Divergência entre a
ficha e a VM reprova o gate até nova coleta.

## Cleanup e reversibilidade

Restaure `lab01-antes-instalacao` e prove que a instalação não existe. Depois
retorne a `lab01-instalacao-validada` para continuar o curso. Compare a build e
a topologia com o inventário; restaurar o snapshot errado deve ser detectado.

## Aprovação

O gate passa quando instalação e licença são suportadas, os volumes estão
explicados, a conta cotidiana não é administrativa, o JSON é válido/sanitizado e
os dois sentidos de restauração foram comprovados. Falha automática: selecionar
disco errado, usar bypass, publicar segredo ou chamar erro de consulta de
“desativado”.

## Questões de defesa

1. Por que área de trabalho visível não encerra a instalação?
2. Qual diferença entre TPM ausente, não consultável e desativado?
3. Por que letra de volume não é identidade estável?
4. Como a build altera a interpretação do inventário?
5. Por que snapshot ainda não é backup dos documentos?
