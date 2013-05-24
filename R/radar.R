# Copyright (C) 2013, Saulo Trento
#
# This file is part of Radar Parlamentar.
# 
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

require("wnominate")

load("rollcall_lulaII.Rdata")
dados <- rollcall_lulaII

# Corrigir nome da deputada Luciana Costa:
dados$name[dados$name=="LUCIANA COSTA\r\n\r\nLUCIANA COSTA\r\n\r\n\r\nLUCIANA COSTA"] <- "LUCIANA COSTA"
# Tirar os acentos, porque o wnominate não aceita:
dados$name[dados$name=="EMILIANO JOS\xc9"] <- "EMILIANO JOSE"
dados$name[dados$name=="JO\xc3O HERRMANN"] <- "JOAO HERRMANN"
dados$name[dados$name=="JOS\xc9 EDMAR"] <- "JOSE EDMAR"
dados$name[dados$name=="MAJOR F\xc1BIO"] <- "MAJOR FABIO"
dados$name[dados$name=="JOS\xc9 MAIA FILHO"] <- "JOSE MAIA FILHO"

# Criar uma coluna com nome+partido (identificador único de quem vota)
dados$nomepartido <- paste(dados$name," (",dados$party,")",sep="")

# Codificar votos:
dados$voto[dados$vote == "Y"] <- 1
dados$voto[dados$vote == "N"] <- -1
dados$voto[dados$vote == "A"] <- 0
dados$voto[dados$vote == "O"] <- 0


# Inicializar lista de dados que será argumento para rollcall().
dadoslist <- list()
dadoslist$desc <- "Camara dos Deputados 53a legislatura (2o mandato Lula)"
dadoslist$votes <- with(dados, tapply(voto,list(nomepartido,rollcall),c))
dadoslist$legis.names <- dimnames(dadoslist$votes)[1][[1]]
dadoslist$vote.names <- dimnames(dadoslist$votes)[2][[1]]
dadoslist$legis.data <- as.matrix(with(dados,tapply(party,nomepartido,max)))

dadoslist$votes[is.na(dadoslist$votes)] <- 0 # Transforma NA em 0.

# Criar o objeto de tipo rollcall:
rcdados <- rollcall(dadoslist, yea=1, nay=-1, missing=0, notInLegis=NA, legis.data=dadoslist$legis.data, source="Dados obtidos com Ricardo Ceneviva.")


por.partido <- function(rcobject){
  # Pega um objeto da classe rollcall e agrega votações por partido.
  # A codificação deve ser 1 para sim, -1 para não, e 0 para o resto.
  if (!class(rcobject) == "rollcall") 
    stop("O argumento rcobject deve ser da classe 'rollcall'.")

  v <- rcobject$votes
  dimnames(v)[[1]] <- as.vector(rcobject$legis.data)
  vv <- t(sapply(by(v,dimnames(v)[[1]],mean),identity))
  rcobject$legis.data <- NULL
  rcobject$votes <- vv

  return(rcobject)
}


pca <- function(rcobject) {
  # Pega um objeto da classe rollcall, porém necessariamente com
  # votos codificados entre -1 e 1, podendo ser qualquer número real
  # neste intervalo (caso de votos agregados por partido), e faz
  # a análise de componentes principais.
  x <- rcobject$votes
  resultado <- list()
  resultado$pca <- prcomp(x,scale=FALSE,center=TRUE)
  resultado$rcobject <- rcobject
  return(resultado)
}


plotar <- function(resultado) {
  # plota resultado de uma PCA.
  xx <- resultado$pca$x[,1]
  yy <- resultado$pca$x[,2]
  symbols(xx,yy,circles=rep(1,length(xx)),inches=0.2)
  text(xx,yy,dimnames(resultado$pca$x)[[1]])
  return
}

# exemplo:
r <- pca(rcdados)
xx <- r$pca$x[,1]
yy <- r$pca$x[,2]
partido <- factor(r$rcobject$legis.data)
num.partidos <- length(levels(partido))
paleta <- colorRampPalette(c("darkblue","blue","yellow","green","darkmagenta","cyan","red","black","aquamarine"),space = "Lab")(num.partidos)
cor <- paleta[as.integer(partido)]
symbols(xx,yy,circles=rep(1,length(xx)),inches=0.05,fg=cor)
legend("topright",levels(partido),col=paleta[1:22],pch=19)
#plot(r$pca$x[,1],r$pca$x[,2]) # gráfico em preto e branco

# por partido:
#rr <- pca(por.partido(rcdados))
#plotar(rr)

# para fazer um wnominate basta utilizar o objeto rcdados:
#
#   wn <- wnominate(rcdados,polarity=c(1,1))
#
# e para ver os resultados, use summary ou plot:
#
#   summary(wn)
#   plot(wn)
#
# note que não é possível fazer o wnominate em dados agregados
# por partido, pois neste caso as votações não são "sim" ou "não",
# e sim um valor numérico que resume o voto médio do partido.

# OBSERVAÇÕES:

# Se um parlamentar muda de partido, ele é considerado como
# um parlamentar diferente. Ou seja, o par (nome,partido) define
# o parlamentar.

# Nos dados rollcall_lulaII, a
# coluna 'id' não é concebida dessa forma, havendo 1 id por nome,
# exceto para o deputado 'BARBOSA NETO', que aparece com dois ids
# diferentes, a saber id=2646 e id=4372. Logo este id não será usado.

# Na matriz de votações, usaremos a codificação do radar.
# Abaixo a comparação com a de Poole e Rosenthal e a do pacote pscl:
#
# Yea : 1 2 3 (pscl:1)  (usaremos 1)
# Nay : 4 5 6 (pscl:0)  (usaremos -1)
# Abs.: 7 8 9 (pscl:NA) (usaremos 0)
# não está na legislatura: 0 (pscl:9) (usaremos 0)
#
