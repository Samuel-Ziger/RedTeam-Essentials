# 00 - Fundamentos e segurança do laboratório

> Ponto de entrada para quem ainda não domina redes, sistemas, terminal e as
> regras de uma atividade de segurança autorizada.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Pessoas iniciantes em segurança ofensiva ou retornando aos fundamentos. |
| Pré-requisitos | Saber instalar software e administrar a própria máquina. |
| Tempo estimado | 8 a 12 horas de estudo e 4 horas de prática. |
| Ambiente | Uma VM descartável ou o `docker-lab`, nunca uma rede de terceiros. |
| Evidência final | Checklist preenchido, diagrama do lab e relatório do exercício integrador. |
| Critério de conclusão | Obter pelo menos 8/10 na autoavaliação e concluir o cleanup. |

## Objetivos observáveis

Ao concluir este módulo, você deverá conseguir:

- explicar IP, porta, protocolo, DNS, HTTP e TLS sem depender de ferramentas;
- navegar, criar arquivos e inspecionar processos em Linux e Windows;
- reconhecer a diferença entre autenticação, autorização e privilégio;
- escrever um escopo simples e identificar uma ação fora de escopo;
- subir, verificar e destruir o laboratório local com segurança;
- preservar evidências sem armazenar segredos reais no repositório.

## Ordem de estudo

1. [Redes, sistemas e identidade](redes-sistemas-identidade.md).
2. [Ética, escopo e Rules of Engagement](etica-escopo-roe.md).
3. [Operação segura do laboratório](laboratorio-seguro.md).
4. Exercício integrador e autoavaliação deste README.

## Exercício integrador

### Cenário

Você recebeu autorização para estudar apenas os containers locais publicados
em `127.0.0.1`. O host, a rede doméstica e qualquer endereço público estão fora
do escopo.

### Tarefas

1. Escreva uma tabela com alvo, endereço, janela, técnica permitida e exclusão.
2. Execute `bash docker-lab/lab-doctor.sh --config-only`.
3. Se Docker estiver disponível, suba apenas o lab e registre `docker compose ps`.
4. Acesse uma URL local com `curl -I` e explique status e cabeçalhos observados.
5. Salve somente dados sintéticos, destrua o lab e registre o cleanup.

### Resultado esperado

- Nenhum pacote é enviado a IP público ou a outro dispositivo da rede.
- A evidência identifica horário UTC, comando, alvo e resultado.
- O relatório diferencia claramente observação de inferência.
- `docker compose down -v` remove containers, rede e volumes do exercício.

## Autoavaliação

Marque somente depois de demonstrar cada item:

- [ ] Sei explicar por que `127.0.0.1` não é o mesmo que `0.0.0.0`.
- [ ] Sei diferenciar resolução DNS de conexão TCP.
- [ ] Sei identificar método, caminho, status e cabeçalhos HTTP.
- [ ] Sei explicar autenticação versus autorização.
- [ ] Consigo reconhecer um segredo antes de fazer commit.
- [ ] Tenho uma autorização e um escopo documentados para o exercício.
- [ ] Defini critérios de parada e contato de emergência.
- [ ] Coletei apenas a evidência mínima necessária.
- [ ] Validei o estado do laboratório.
- [ ] Executei e documentei o cleanup.

## Próximos passos

- Trilha geral: [01 Recon](../01-Recon/README.md) e [02 OSINT](../02-OSINT/README.md).
- Trilha AppSec: [07 Web AppSec](../07-Web-AppSec/README.md).
- Trilha defensiva: [05 DFIR](../05-DFIR/README.md).

