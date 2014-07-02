Radar Parlamentar
==================

[![Build Status](https://travis-ci.org/leonardofl/radar_parlamentar.png?branch=master)](https://travis-ci.org/leonardofl/radar_parlamentar)

Este projeto utiliza dados abertos para analisar os votos de parlamentares em diferentes casas legislativas do Brasil.

O Radar Parlamentar determina "semelhanças" entre partidos políticos baseado na análise matemática dos dados de votações de projetos de lei na casa legislativa. Essas semelhanças são apresentadas em um gráfico bi-dimensional, em que círculos representam partidos e a distância entre esses círculos representa o quão parecido esses partidos votam.

Site em produção: [Radar Parlamentar](http://radarparlamentar.polignu.org/ "Radar Parlamentar")

Código-fonte do Radar analisado pelo Sonar: http://analiseradar.cloudapp.net/

Licença do projeto: *AGPL v3*

Seja bem vindo,

Leonardo Leite

=

###TO DO


* Toda a lista de ToDo do **Radar Parlamentar** é controlada através das *Issues*: [Issues Radar Parlamentar](https://github.com/leonardofl/radar_parlamentar/issues)

=

###Questões

Algumas questões específicas que espero responder analisando os dados. Os resultados dessas análises se encontram na pasta "resultados"

1. Quais os tipos de proposições legislativas mais frequentes na casa?
2. Como foi a votação da mudança do código florestal?
3. Como foram as votações das PECs** em 2011?
4. Partidos da base aliada tendem a aprovar medidas provisórias? E os de oposição tendem a rejeitá-las?
5. Por ser um partido de oposição, será que em termos de votação o PSOL acaba se assemelhando a partidos de direita como o DEM?
6. Quais são as temáticas das proposições nas quais partidos ideologicamente antagônicos votam de acordo?
7. Análise de sensibilidade: será que uma votação diferente por afetar bastante o posicionamento dos partidos?

>Exemplo: será que se desconsiderarmos a votação do código florestal, o PV ficaria bem perto da base governista?

**propostas de emenda à constituição, a saber: *98/2007 e 61/2011* **

=

###Links

####Dados Abertos

* [Câmara dos deputados](http://www2.camara.gov.br/transparencia/dados-abertos)
* [Câmara municipal de São Paulo](http://www.camara.sp.gov.br/index.php?option=com_wrapper&view=wrapper&Itemid=219)
 
####Estilo de Programação Python do Google

* [Google PyGuide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html) **vamos *tentar* seguir**

####Deploy e Django

* [Instalar o django 1.4](http://blog.sudobits.com/2012/03/24/django-1-4-for-ubuntu-11-10-12-04/)
* Como criar um projeto do django e como fazer deploy (testes e producao)
    * https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/
    * http://nonantolando.blogspot.com.br/2012/04/django-14-for-ubuntu-1204.html (não consegui fazer funcionar - Diego)
* [Tutorial de Django](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
