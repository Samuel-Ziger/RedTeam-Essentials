# Redes, sistemas e identidade: base mínima

## Redes

Uma conexão pode ser descrita por **origem**, **destino**, **protocolo** e
**porta**. DNS traduz nomes em registros; ele não prova que o serviço está
disponível. TCP estabelece uma sessão confiável; UDP não possui handshake
equivalente. HTTP transporta requisições e respostas, enquanto HTTPS adiciona
TLS para confidencialidade, integridade e autenticação do servidor.

Perguntas que devem preceder qualquer ferramenta:

1. Qual endereço está explicitamente no escopo?
2. O nome resolve para um endereço permitido?
3. A porta representa qual protocolo esperado?
4. A ação é passiva, ativa ou potencialmente destrutiva?

### Prática local segura

```bash
python3 -m http.server 8000 --bind 127.0.0.1
curl -v http://127.0.0.1:8000/
```

Em outro terminal, identifique método, caminho, código de status, cabeçalhos,
IP e porta. Encerre o servidor com `Ctrl+C`.

## Sistemas

Antes de estudar privilege escalation, domine inventário e permissões:

| Pergunta | Linux | PowerShell |
|----------|-------|------------|
| Quem sou? | `id` | `whoami /all` |
| Onde estou? | `pwd` | `Get-Location` |
| Quais processos existem? | `ps aux` | `Get-Process` |
| Quais conexões escutam? | `ss -lntup` | `Get-NetTCPConnection -State Listen` |
| Hash de evidência | `sha256sum arquivo` | `Get-FileHash arquivo -Algorithm SHA256` |

Execute apenas em sua VM. Registre o comando, horário UTC e finalidade, evitando
copiar tokens, hashes de senha ou dados pessoais para notas públicas.

## Identidade

- **Identificação:** a identidade alegada, como um nome de usuário.
- **Autenticação:** como a identidade é comprovada, por exemplo senha + MFA.
- **Autorização:** quais ações a identidade autenticada pode realizar.
- **Privilégio:** permissão específica atribuída direta ou indiretamente.
- **Sessão/token:** estado ou artefato usado após a autenticação.

O princípio do menor privilégio reduz tanto o impacto de um erro quanto um
caminho de ataque. Em exercícios, prefira contas descartáveis e dados canário.

## Critério de conclusão

Produza um diagrama com cliente, DNS, alvo local, porta e protocolo; depois
explique onde autenticação e autorização ocorreriam em uma aplicação web.

