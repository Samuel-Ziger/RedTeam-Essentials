# 02 — Modo usuário, modo kernel, APIs e chamadas de sistema

A CPU separa níveis de privilégio para impedir que aplicações comuns executem
instruções ou acessem memória privilegiada diretamente. Chamadas de sistema são
transições controladas, mas aplicativos devem preferir APIs documentadas e não
depender de números ou stubs internos.

## Objetivos

- explicar proteção entre user mode e kernel mode;
- distinguir API Win32, Native API, ABI e syscall;
- interpretar `GetLastError`, `HRESULT` e `NTSTATUS` sem conversão cega;
- entender handles e direitos como contrato de acesso;
- observar I/O de uma fixture sem enumerar números de syscall.

## Fronteira de privilégio

Código em user mode possui espaço virtual isolado e não acessa diretamente a
memória do kernel. Uma instrução de transição entra por ponto controlado; o kernel
valida parâmetros, modo anterior, endereços, handles e autorização antes de
operar. Bug em kernel tem impacto maior porque compartilha o domínio privilegiado.

Uma syscall não “torna confiável” a entrada. Ponteiros e tamanhos vindos de user
mode continuam não confiáveis e precisam ser verificados. Esse princípio explica
por que drivers e kernel usam padrões rigorosos de validação.

## Contrato e implementação

API Win32 documentada é o contrato recomendado para aplicações. Ela pode validar
ou transformar dados, trabalhar inteiramente em user mode ou chamar funções da
Native API em `ntdll`. Stubs de `ntdll` participam de várias transições, porém
números de serviço e estruturas internas variam entre builds e arquiteturas.

ABI inclui calling convention, registradores, layout de tipos, alinhamento,
representação de retorno e ownership. API é uma interface de programação mais
ampla. Uma assinatura C pode parecer igual e ainda ter ABI incompatível quando
arquitetura ou estrutura muda.

WOW64 fornece ambiente para processos x86 em sistema x64. A passagem envolve
thunks e componentes próprios; paths e Registro também podem ter visualizações
diferentes. Não misture DLL x64 num processo x86.

## Erros em camadas

Muitas funções Win32 retornam `BOOL`, ponteiro ou `HANDLE`. Quando a documentação
manda, capture `GetLastError` imediatamente, antes que outra chamada altere o
estado por thread:

```c
HANDLE file = CreateFileW(
    path,
    GENERIC_READ,
    FILE_SHARE_READ,
    NULL,
    OPEN_EXISTING,
    FILE_ATTRIBUTE_NORMAL,
    NULL
);
if (file == INVALID_HANDLE_VALUE) {
    DWORD error = GetLastError();
    fwprintf(stderr, L"open_failed=%lu path=%ls\n", error, path);
    return 1;
}
```

`HRESULT` codifica sucesso/falha e facility; `NTSTATUS` é usado por interfaces
nativas/kernel. Conversões existem, mas podem perder detalhe. Preserve domínio,
valor hexadecimal, operação e contexto. Não chame `GetLastError` quando a
documentação não diz que ele é significativo.

## Handles e direitos

Handle é uma referência no contexto do processo para um objeto, associada aos
direitos concedidos na abertura. Valor numérico não é ponteiro portátil nem
identidade global. O kernel valida o handle e o acesso pedido em operações
posteriores. Feche exatamente uma vez e defina ownership no código.

Pedindo o mínimo de direitos, o programa reduz impacto e melhora compatibilidade.
Não solicite “all access” por conveniência. Handles podem ser herdáveis quando
explicitamente configurados; o curso não explora handles de outros processos.

## I/O síncrono observado

Compile uma fixture que abra, leia e feche um arquivo sintético. Use Process
Monitor filtrado pelo PID e caminho para observar `CreateFile`, `ReadFile` e
`CloseFile`. Esses nomes são abstrações exibidas pela ferramenta; não conclua que
cada linha é exatamente uma syscall.

Relacione resultado como `SUCCESS`, `NAME NOT FOUND` ou `ACCESS DENIED` à ação da
fixture. Uma sondagem ausente pode ser fallback normal. Correlacione ordem e
efeito visível.

## Exercícios

1. Compare API, ABI, Native API e syscall em uma tabela.
2. Explique por que número de syscall não é dependência aceitável do aplicativo.
3. Revise o snippet e marque retorno, captura de erro e ownership do handle.
4. Observe uma leitura própria no ProcMon e evite correspondência linha=syscall.
5. Modele o que WOW64 precisa compatibilizar e o que permanece arquitetura nativa.

## Checklist de domínio

- [ ] Explico a transição como fronteira validada, não acesso irrestrito.
- [ ] Aplicações dependem de APIs documentadas, não números internos.
- [ ] Distingo API, ABI e implementação.
- [ ] Capturo erros no domínio e momento corretos.
- [ ] Handle inclui contexto e direitos, não é endereço global.
- [ ] Código pede direitos mínimos e fecha recursos uma vez.
- [ ] Tracing fica limitado à fixture e não enumera mecanismos ofensivos.
