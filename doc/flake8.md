Flake8
==========================
1. Sobre o Flake8
---------------------------------
O Flake8 é uma ferramenta será utilizada somente com o intuito de verificar se o estilo do código respeita o padrão adotado pela comunidade, descrito na Python Enhancement Proposal 8 (Pep8).

2. Instalação do flake8 via terminal:
----------------------------------------
<pre> $ [sudo] pip2.7 install flake8 </pre>

Utiliza-se o 2.7, já que esta é a versão do python do Radar Parlamentar

3. Utilizando o flake8 via terminal:
-------------------------------------------------
**3.1 Para analisar um único arquivo**

<pre> $ flake8 path/to/code/to/check.py </pre>

exemplo:
<pre> $ flake8 radar_parlamentar/analises/analise.py </pre>

**3.2 Para analisar um diretório completo**

<pre> $ flake8 path/to/code/ </pre>

exemplo:
<pre> $ flake8 radar_parlamentar/ </pre>

4. Instalação do flake8 em um editor de texto
-------------------------------------------------
**4.1 Atom**
  - Baixar e instalar o arquivo .deb disponível no endereço: https://atom.io/
  - No menu superior encontre "Packages" -> "Settings View" e escolha a opção
  "Install Packages/Themes", será aberto um menu de busca de pacotes.
  - No menu digite "flake8" e assim aparecerá a opção para instalação.
  - Após instalado, quando qualquer arquivo do projeto for aberto aparecerão
  avisos sobre o que deve ser modificado para o padrão da comunidade python.
