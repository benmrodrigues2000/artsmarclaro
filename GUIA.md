# Guia de manutenção — Marclaro

## Estrutura e atualização

- `build.py` contém os modelos partilhados, os textos PT/EN, o catálogo e o portefólio.
- `legal_content.py` contém os textos PT/EN das quatro páginas legais e os avisos de preparação.
- `python3 build.py` regenera as **11 páginas HTML**, o sitemap e o robots.txt. Não editar só os HTML: serão substituídos na próxima geração.
- `css/style.css` define o visual: branco, tons neutros, retângulos e linhas finas. Sem arcos, círculos decorativos ou animações contínuas. Os ícones funcionais e o logótipo mantêm a sua identidade.
- `js/main.js` controla idioma, menu, carrinho, formulários, filtros, visualização de fotografias e limpeza do armazenamento local.
- `img/` contém as fotografias existentes. Não foram geradas nem substituídas fotografias de trabalhos.

### Pré-visualização

```sh
python3 build.py
python3 -m http.server 8000 --bind 0.0.0.0
```

O site é estático, sem dependências de produção. O Node é utilizado apenas para os testes opcionais.

## Fotografias

Substituir uma fotografia por outra com o mesmo nome em `img/` atualiza todas as utilizações. Recomenda-se JPG até 1600 px e, se possível, menos de 400 KB. O catálogo usa `object-fit: contain` para mostrar a peça inteira; fotografias com enquadramentos semelhantes dão maior consistência. O portefólio usa enquadramentos retangulares e abre a fotografia completa ao selecionar um trabalho.

## Portefólio

- A secção «O meu percurso» utiliza apenas a história que já existia na página Sobre, sem inventar datas, prémios ou formação.
- Editar essa secção na função `portfolio()` quando houver novos dados biográficos confirmados. Atualizar também Sobre, se necessário.
- A lista `PORT` contém fotografia, categorias (`ceramica`, `porcelana`, `personalizadas`, `aulas`) e legendas PT/EN.
- Filtros, legendas permanentes e visualização ampliada funcionam por rato, toque e teclado.

## Catálogo e carrinho

Editar `PRODUCTS` em `build.py`: identificador, fotografia, nome PT/EN, preço, descrição PT/EN. A contagem de peças é automática.

**Os preços e dimensões existentes são exemplos: confirmar antes de publicar comercialmente.** Não foram alterados nesta revisão. Disponibilidade, impostos aplicáveis, portes, condições de sinal e prazos devem ser confirmados pelo ateliê.

O carrinho está em todas as páginas, conserva peças e quantidades no navegador e prepara um pedido por WhatsApp. Não cobra pagamentos nem conclui contratos automaticamente. O botão de encomenda deve continuar a distinguir um pedido de uma compra concluída. Mantêm-se MB WAY e transferência bancária como métodos a confirmar diretamente.

## Formulários

Os formulários de contacto e marcação validam os campos e abrem uma mensagem no WhatsApp; o visitante tem de confirmar o envio nesse serviço. O reconhecimento de leitura da privacidade não autoriza marketing. Não existe envio para servidor de formulários na configuração atual.

A possibilidade técnica de definir `data-endpoint` num formulário continua no JavaScript, mas **não a ativar sem rever a política de privacidade, a informação junto do formulário, a mensagem de confirmação e os contratos com o prestador**. Confirmar também retenção, segurança, subcontratantes e transferências internacionais.

## Privacidade por defeito

- Retirados Plausible Analytics, Google Fonts externos, mapa Google incorporado e formulário de newsletter não integrado.
- São usadas fontes disponíveis no dispositivo, imagens locais e ligações normais para mapas e redes sociais. Nenhum serviço externo é carregado pelo código do site antes de o visitante abrir uma ligação.
- Não existe banner de consentimento, pois não há estatísticas, publicidade ou armazenamento opcional. Não adicionar um banner meramente decorativo.
- `mc-lang`: idioma escolhido; `mc-cart`: peças e quantidades; ambos locais ao navegador e sem expiração automática. A antiga chave `mc-consent` é apagada, mesmo se o visitante tinha aceite estatísticas na versão anterior.
- A página Cookies explica a finalidade e duração e permite apagar o idioma guardado e esvaziar o carrinho. O idioma da página atual mantém-se até sair; na próxima navegação volta ao português.
- Com armazenamento bloqueado, o site continua a funcionar na página atual, sem prometer persistência.
- O alojamento pode manter registos técnicos ou acrescentar ferramentas. Confirmar a configuração real e atualizar a política; os testes verificam o código do site, não a infraestrutura de produção.

## Obrigatório confirmar antes de publicação comercial

As políticas são uma base editorial e técnica, **não uma certificação de conformidade nem substituto de revisão jurídica**. Os avisos públicos «Versão de preparação» em Termos e Envios são intencionais: não ocultar lacunas com dados inventados.

- [ ] Confirmar nome/denominação legal do operador, NIF e morada profissional completa.
- [ ] Identificar explicitamente a morada de devolução e de reclamações.
- [ ] Aprovar preços, dimensões, disponibilidade, enquadramento de IVA, portes e condições de pagamento/sinal.
- [ ] Confirmar política comercial de aulas/cancelamentos, incluindo o tratamento de sinais, sem limitar direitos legais.
- [ ] Confirmar inscrição e ligação apropriada no Livro de Reclamações Eletrónico. A ligação atual é apenas para o portal geral; não afirma registo do operador.
- [ ] Confirmar entidade(s) de resolução alternativa de litígios competente(s), âmbito territorial/material, contactos e eventual adesão. Publicar os dados corretos, sem presumir um centro.
- [ ] Confirmar alojamento, fornecedores de email/WhatsApp, acesso, segurança, retenção efetiva por finalidade e eventuais transferências internacionais/salvaguardas. Rever a política com essa informação.
- [ ] Confirmar o responsável pelo tratamento e um procedimento para pedidos de direitos RGPD, eliminação e cumprimento dos prazos legais.
- [ ] Rever os textos com apoio jurídico adequado à atividade e aos destinos de venda; confirmar versões legais em vigor no lançamento.
- [ ] Depois da validação, substituir os parágrafos provisórios e remover as flags `draft` em `legal_content.py`. Atualizar a data da revisão em `legal_page()` e regenerar tudo.

### Referências usadas na revisão

- Livre resolução, reembolso e exceção para bens personalizados: Decreto-Lei n.º 24/2014, a consultar na redação atual. [1](https://diariodarepublica.pt/dr/detalhe/decreto-lei/24-2014-572450)
- Responsabilidade por falta de conformidade de bens móveis novos, em regra três anos: Decreto-Lei n.º 84/2021. [1](https://diariodarepublica.pt/dr/detalhe/decreto-lei/84-2021-172938301)
- Para a aplicação concreta, verificar também RGPD, legislação nacional de proteção de dados, informação comercial, reclamações e RAL junto das autoridades competentes e do apoio jurídico.

## Testes

```sh
npm ci
npx playwright install --with-deps chromium
# Noutro terminal, manter o servidor estático acima em execução.
npm test
```

A suite cobre todas as páginas em desktop e num viewport móvel: imagens, erros JavaScript/HTTP, ausência de pedidos externos automáticos, links e âncoras, idiomas, filtros, teclado da galeria, carrinho entre páginas, mensagem WhatsApp, limpeza/indisponibilidade do armazenamento e formulário de contacto. Não envia mensagens reais nem encomendas.

Pode usar `SITE_URL` para um servidor local diferente e `CHROMIUM_PATH` para um Chromium já instalado. O teste de ausência de pedidos externos está preparado para um servidor local (`localhost` ou `127.0.0.1`).

## Publicação

Confirmar primeiro os pontos acima. Publicar os HTML gerados, `css/`, `js/`, `img/`, `sitemap.xml` e `robots.txt` num alojamento estático com HTTPS. Confirmar o domínio em `SITE` antes da geração; o domínio atual no código é `marclaroarts.pt` e não constitui confirmação de registo. Não publicar `node_modules/`, relatórios de testes ou ficheiros temporários.
