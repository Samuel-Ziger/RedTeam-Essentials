# 00 — Escopo ético e método

Privacidade é um direito e uma disciplina de engenharia. As mesmas tecnologias
que protegem uma pessoa em Wi-Fi público também podem aparecer em incidentes.
Por isso, este curso separa três atividades:

- **proteção legítima:** reduzir coleta, exposição e acesso indevido aos próprios
  dados;
- **pesquisa autorizada:** testar sistemas próprios ou cobertos por regras de
  engajamento;
- **investigação defensiva:** analisar telemetria que a organização está
  autorizada a tratar.

Ficam fora do escopo instruções para apagar ou adulterar evidência, contornar
ordens legais, assediar pessoas, usar contas fraudulentas, ocultar malware ou
operar infraestrutura de terceiros. Entender que um invasor usa proxy ou tenta
remover logs é útil à defesa; ensinar como fazê-lo de forma furtiva não é
necessário para alcançar o objetivo pedagógico.

## Método em seis passos

1. Declare o objetivo em uma frase.
2. Liste os dados e relações que precisam de proteção.
3. Nomeie observadores e capacidades realistas.
4. Desenhe o caminho completo, incluindo endpoint e aplicação.
5. Escolha controles e testes mensuráveis.
6. Registre falhas possíveis e risco residual.

Exemplo: “impedir que outros clientes do mesmo Wi-Fi leiam o conteúdo de uma
sessão web” é testável. “Ficar invisível na internet” não define observador,
ativo, prazo nem critério de sucesso.

## Prática segura

Escreva um objetivo pessoal legítimo e uma exclusão. Exemplo: proteger tráfego
administrativo em uma rede não confiável; não tentar ocultar abuso ou acessar
sistemas sem autorização. Essa declaração acompanha todos os laboratórios.

