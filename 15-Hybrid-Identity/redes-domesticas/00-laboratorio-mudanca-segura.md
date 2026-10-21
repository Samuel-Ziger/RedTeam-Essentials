# 00 — Laboratório e mudança segura

Configurar um roteador pode derrubar conectividade, telefonia ou automação.
Antes de mudar, registre modelo, firmware, responsável, configuração atual,
porta de administração, credenciais sob gestão segura e procedimento de reset.

Use um fixture JSON para todos os primeiros laboratórios. Em equipamento real,
faça uma mudança por vez, mantenha acesso por cabo quando possível, exporte um
backup compatível e defina janela/rollback. Não altere dispositivo da operadora
sem saber como restaurar Internet, voz e TV.

## Registro de mudança

- objetivo e risco;
- estado anterior sanitizado;
- alteração prevista;
- validação local, Internet, DNS, Wi-Fi e serviços essenciais;
- gatilho e passos de rollback;
- resultado e evidência.

## Limite

Não teste senhas, clientes ou redes de vizinhos. Potência, canal e largura
devem respeitar regulamentação local e capacidades do equipamento.
