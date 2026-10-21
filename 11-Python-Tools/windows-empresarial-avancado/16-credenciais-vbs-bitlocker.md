# 16 — Credenciais, VBS, Windows Hello e BitLocker

Credenciais devem ser reduzidas, isoladas e não reutilizadas. Windows Hello for
Business usa chave protegida no dispositivo em vez de enviar senha para cada
autenticação; modelos de trust dependem da arquitetura de identidade.

## Proteções

- LSA protection protege o processo LSA;
- Credential Guard usa VBS para determinados secrets corporativos;
- Remote Credential Guard/Restricted Admin pertencem ao estudo de acesso remoto;
- Windows Hello for Business reduz dependência de senha;
- BitLocker protege dados at rest e recovery precisa de governança;
- Secure Boot/TPM medem/protegem a cadeia.

Credential Guard não protege contas locais, todos os vaults ou o banco AD em DC.
No Windows Server 2025, defaults e exceções dependem de papel/hardware; confirme
a documentação atual antes do rollout.

## BitLocker empresarial

Defina algoritmo/política, escrow de recovery key, rotação, acesso auditado,
preboot, removable media, suspend/resume para firmware e processo de descarte.
Nunca valide escrow exibindo a chave em relatório.

## Exercício

Crie matriz controle × segredo protegido × limite × requisito × recovery.

