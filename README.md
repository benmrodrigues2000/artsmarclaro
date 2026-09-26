# Marclaro

Site estático bilingue de Claudia Sousa Art´s Marclaro — cerâmica e porcelana fria em Vila Nova de Gaia.

- Conteúdo e modelos: `build.py`; políticas: `legal_content.py`.
- Gerar as 11 páginas: `python3 build.py`.
- Visual: `css/style.css`; interação: `js/main.js`; fotografias: `img/`.
- Pré-visualizar: `python3 -m http.server 8000 --bind 0.0.0.0`.
- Testes opcionais: `npm ci`, `npx playwright install --with-deps chromium` e `npm test`, com o servidor em execução.

Ver **GUIA.md** para manutenção, testes e a lista de dados comerciais/legais que precisam de confirmação antes de publicar. As condições legais assinaladas como versão de preparação não devem ser tratadas como documentação final aprovada.
