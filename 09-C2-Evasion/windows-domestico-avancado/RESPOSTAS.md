# Respostas orientativas e critérios de raciocínio

Estas respostas não substituem evidência do laboratório. Compare sua explicação, identifique lacunas e repita o experimento quando necessário.

## Toda API Win32 gera uma syscall?

Não. Uma API pode validar e transformar parâmetros, responder inteiramente em modo usuário, usar outra biblioteca ou causar várias operações no kernel. O contrato documentado tende a ser mais estável que essa implementação.

## Processo é o programa?

O programa é o código/arquivo; processo é uma instância em execução com espaço virtual, handles, token e pelo menos uma thread. Duas instâncias do mesmo executável possuem PIDs e estado diferentes.

## Grupo presente no token significa acesso concedido?

Não. Considere se o grupo está habilitado, DACL, MIC, privilégios, deny ACEs aplicáveis e o objeto solicitado. Um privilégio disponível também pode estar desabilitado.

## Page fault significa leitura do disco?

Não. Pode ser resolvido por zero page, standby list, compartilhamento ou mapeamento já residente. Hard fault indica backing mais caro, mas ainda exige correlação para explicar impacto.

## RVA é offset dentro do arquivo?

Não. RVA é relativo à base da imagem carregada. A conversão para offset depende da seção, de seu RVA, de `PointerToRawData`, tamanhos e alinhamento. Sempre valide limites.

## DLL executa sozinha?

Não como um programa convencional. Ela é mapeada no contexto de um processo carregador, e suas funções rodam em threads chamadoras. O loader chama o entry point em condições específicas; por isso `DllMain` deve permanecer mínimo.

## Caminho absoluto torna qualquer DLL confiável?

Não. Ele reduz ambiguidade de busca. Confiança ainda depende de origem, permissões, integridade, assinatura quando aplicável e compatibilidade da ABI.

## `NAME NOT FOUND` no ProcMon é a causa?

Não necessariamente. Aplicações sondam locais opcionais e seguem fallback. É causal quando corresponde a recurso necessário, alinha-se ao fluxo, antecede a falha e restaurar aquela variável recupera o cenário.

## Serviço em estado `Stopped` está quebrado?

Não. Pode ter início manual ou por gatilho e estar corretamente ocioso. Analise modo, trigger, dependências, código de saída, eventos e resultado esperado.

## Assíncrono é sempre mais rápido?

Não. Ele permite continuar enquanto uma operação aguarda e escala concorrência, mas adiciona coordenação. Uma única operação pequena pode não melhorar. Meça a carga real.

## Um trace sem o evento esperado prova ausência?

Não. Provider, keyword, level, janela, buffers, perda e esquema precisam ser verificados. Ausência na coleta só é significativa quando a cobertura é demonstrada.

## Média basta para comparar desempenho?

Não. Preserve amostras, controle carga e informe mediana, p95, máximo e dispersão. Com vinte execuções, o p95 é uma estimativa didática, não generalização estatística ampla.

## Assinatura digital prova segurança?

Não. Ela liga bytes protegidos a um signatário e cadeia de confiança e detecta modificação conforme o formato. Código assinado ainda pode conter vulnerabilidade ou comportamento inadequado.

## Execution Policy impede um adversário?

Não. É controle operacional contra execução acidental e expressão de política, não sandbox robusta. Assinatura, privilégio mínimo, logging e Application Control cobrem outras partes.

## VBS, HVCI e Credential Guard são iguais?

Não. VBS cria a fronteira baseada no hipervisor; HVCI usa essa fronteira para fortalecer integridade de código; Credential Guard protege categorias específicas de credenciais. Nenhuma substitui backup, atualização ou segurança da aplicação.

## `SecurityServicesConfigured` prova que a proteção roda?

Não. Compare disponibilidade, configuração e `SecurityServicesRunning`, além do status de VBS. Interprete os arrays conforme a documentação da versão.

## `!analyze -v` encontrou a causa?

Ele produziu uma análise automatizada inicial. Confirme símbolos, exception code, contexto, stack, primeiro frame próprio, fonte, logs e reprodução. Um mini dump pode omitir o dado necessário.

## Quando o diagnóstico está concluído?

Quando uma hipótese explica mecanismo e evidência, uma intervenção focal restaura o resultado, um teste impede regressão, efeitos colaterais foram medidos e outra pessoa reproduz. Se isso não for possível, a conclusão correta declara o que foi descartado e o próximo teste.

