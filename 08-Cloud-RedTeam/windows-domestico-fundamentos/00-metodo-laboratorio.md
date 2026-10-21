# 00 — Método, laboratório e evidência

Administrar Windows não é decorar telas. É compreender estado, formular uma
hipótese, escolher a observação menos invasiva e provar o resultado. Este
capítulo estabelece o método usado no restante do módulo.

## Objetivos

Ao concluir, você será capaz de:

- construir uma VM descartável sem expor dados pessoais;
- diferenciar snapshot, backup, restauração e evidência;
- classificar uma atividade pelo impacto e preparar rollback;
- registrar um experimento que outra pessoa consiga reproduzir;
- separar fato observado, interpretação e próxima ação.

## Ambiente de referência

Use uma VM com firmware UEFI, TPM virtual quando o hipervisor oferecer, dois
processadores virtuais, 8 GiB de RAM, disco de sistema com pelo menos 80 GiB e
um segundo disco virtual vazio. O segundo disco é o único alvo dos exercícios
de particionamento. A VM deve começar sem adaptador de rede; conexão temporária
para ativação ou atualização só pode ocorrer fora dos experimentos, de forma
consciente e conforme a licença usada.

Instale mídia oficial em hardware compatível. Algumas edições e versões atuais
do Windows 11 exigem internet e conta Microsoft durante a configuração inicial.
Não use comandos de contorno. Para a rota offline, parta de uma VM oficial já
provisionada por um processo suportado, de uma imagem de avaliação adequada ou
da edição cujo fluxo documentado atenda ao laboratório.

Crie os checkpoints `00-base-vazia` e `01-sistema-limpo`. Snapshot captura o
estado da VM para rollback rápido, mas costuma depender do mesmo host e disco;
por isso não substitui cópia independente dos dados.

## O ciclo experimental

1. **Pergunta:** descreva o comportamento que deseja compreender.
2. **Estado inicial:** registre edição, build, horário, privilégio e snapshot.
3. **Hipótese:** escreva o resultado esperado e o que o refutaria.
4. **Risco:** determine alvo, impacto, pré-condições e forma de retorno.
5. **Observação:** consulte primeiro; não altere o estado para “ver se resolve”.
6. **Mudança única:** quando necessária, modifique uma variável por vez.
7. **Validação:** verifique efeito funcional e ausência de dano colateral.
8. **Rollback:** reverta e confirme explicitamente o estado anterior.
9. **Conclusão:** diferencie evidência, inferência, limitação e próxima dúvida.

Esse processo evita um erro frequente: executar várias correções, observar que
o sintoma sumiu e atribuir causalidade à última delas. Correlação temporal é uma
pista, não uma prova.

## Classes de risco

| Classe | Exemplo | Controle mínimo |
|---|---|---|
| A | consultar arquivo, processo, volume ou evento | conta comum e registro da saída |
| B | criar fixture, conta temporária ou chave própria | alvo isolado e procedimento de limpeza |
| C | alterar ACL, Registro, serviço, BitLocker ou partição | snapshot, exportação do estado e rollback ensaiado |
| D | instalar, redefinir ou recuperar o sistema | clone descartável, backup testado e mídia oficial |

Elevação administrativa não é sinônimo de autorização nem de segurança. Use-a
apenas no passo que realmente necessita do token elevado. Antes de uma operação
de classe C ou D, leia o comando completo, resolva caminhos e números de disco e
faça uma pausa de confirmação.

## Evidência reproduzível

Crie `C:\RTE-Lab\evidencias` e, para cada atividade, armazene um arquivo Markdown
com pergunta, comandos, saídas sanitizadas, interpretação e cleanup. Inclua
edição/build porque interfaces e propriedades mudam. Use texto ou JSON sempre
que possível: uma captura de tela isolada omite contexto e não é pesquisável.

Nunca registre nome real, e-mail, chave de produto, serial, recovery key ou
conteúdo pessoal. O identificador de uma VM pode ser substituído por um rótulo
como `vm-a`. Um hash de arquivo prova igualdade de bytes em dois momentos; não
prova autoria, legitimidade ou ausência de risco.

Um registro mínimo pode seguir este molde:

```text
Experimento: WIN08-P03
Estado: Windows <edição>, build <número>, usuário comum, snapshot <nome>
Hipótese: ...
Comando/ação: ...
Esperado: ...
Observado: ...
Interpretação: fato ...; inferência ...; limitação ...
Rollback: ...
Validação final: ...
```

## Primeira prática guiada

Abra PowerShell sem elevação e execute consultas inofensivas:

```powershell
$root = 'C:\RTE-Lab\evidencias'
New-Item -ItemType Directory -Path $root -Force | Out-Null
Get-ComputerInfo |
  Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
    OsArchitecture |
  ConvertTo-Json |
  Set-Content -LiteralPath (Join-Path $root 'estado-inicial.json') -Encoding UTF8
Get-FileHash -LiteralPath (Join-Path $root 'estado-inicial.json') -Algorithm SHA256
```

Leia o JSON e confirme que ele não contém identificadores desnecessários.
Registre o hash, restaure `01-sistema-limpo` e prove que o diretório desapareceu.
Depois recrie-o. O objetivo não é o diretório; é praticar previsão, evidência e
reversão antes de tarefas que tenham impacto real.

## Exercícios

1. Escreva por que desligar a VM não equivale a restaurar um snapshot.
2. Classifique criar um arquivo, trocar uma ACL, formatar o disco de dados e
   reinstalar o sistema. Justifique cada classe.
3. Produza uma hipótese falsa de propósito, execute uma consulta e registre
   como a evidência a refutou sem “corrigir” o texto original.
4. Faça uma tabela de dados permitidos e proibidos na documentação do curso.
5. Peça a outra pessoa para reproduzir a primeira prática apenas pelo diário.

## Checklist de domínio

- [ ] A VM, os dois discos e os checkpoints estão identificados.
- [ ] Sei qual edição/build estudo e não usei contorno de OOBE ou licença.
- [ ] Consigo explicar por que snapshot não é backup.
- [ ] Toda mudança tem alvo explícito, risco, validação e rollback.
- [ ] Evidências não contêm dados pessoais nem segredos de recuperação.
- [ ] Diferencio observação, inferência e causalidade.
- [ ] Outra pessoa consegue repetir um experimento usando apenas meu registro.
