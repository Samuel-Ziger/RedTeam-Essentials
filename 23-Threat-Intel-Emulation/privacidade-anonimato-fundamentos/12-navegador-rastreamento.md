# 12 — Estado do navegador e rastreamento

Navegadores mantêm cookies, local storage, cache, service workers, permissões,
histórico e sessões. Esses mecanismos habilitam autenticação e desempenho, mas
também podem ligar visitas.

## Modo privativo

Uma janela privativa cria armazenamento temporário separado e normalmente o
descarta ao fechar a sessão. Ela não esconde tráfego da rede, do empregador, do
ISP ou do site, nem impede que uma conta revele identidade. Downloads e
favoritos também podem permanecer no dispositivo.

## Particionamento e terceiros

Bloqueio de cookies de terceiros e particionamento de armazenamento reduzem
rastreamento entre sites. Links decorados, pixels, logins federados e
fingerprinting ainda podem criar associações. Controles mudam com versões;
consulte documentação do navegador e teste o comportamento atual.

## Extensões

Cada extensão adiciona código privilegiado, permissões e características ao
navegador. Instalar muitas extensões “de privacidade” pode aumentar superfície
de ataque ou unicidade. Prefira mecanismo integrado, origem oficial, poucas
permissões e manutenção ativa.

## Prática segura

Em um perfil descartável próprio, inventarie cookies e armazenamento de uma
aplicação local. Compare sessão normal e privativa sem inserir dados pessoais.

