# Resposta orientativa — timeline de autenticação

## Observações

- Duas falhas para `LAB\student` precedem um logon de rede bem-sucedido.
- Um evento 4672 aparece um segundo depois em outro host.
- A sessão é encerrada aproximadamente quatro minutos depois.

## Hipóteses, não conclusões

Pode haver erro de senha seguido de sucesso legítimo, credencial descoberta ou
automação com segredo desatualizado. O 4672 indica privilégios especiais, mas
não prova sozinho escalação nem ação maliciosa.

## Dados necessários

- campos completos dos eventos, especialmente logon ID e workstation;
- logs de EDR/process creation e autenticação do serviço de origem;
- contexto de change ticket e atividade esperada do usuário.

## Detecção e resposta proporcional

Correlacionar falhas seguidas de sucesso e privilégio, usando usuário, origem e
logon ID. Ajustar limiar por contas de serviço. Antes de bloquear, validar se a
origem pertence ao usuário e coletar os logs complementares.

