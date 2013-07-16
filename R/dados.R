# Copyright (C) 2013, Leonardo Leite
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


# setup:
# install.packages('RMySQL')
# RMySQL documentation: http://rss.acs.unt.edu/Rdoc/library/RMySQL/html/RMySQL-package.html

# input:
nome_curto_casa_leg = 'sen'

require("RMySQL")
con <- dbConnect(MySQL(), user="root", password="123mudar", dbname="radar", host="localhost")

casas_legislativas <- dbReadTable(con, "modelagem_casalegislativa")
votacoes <- dbReadTable(con, "modelagem_votacao")
votos <- dbReadTable(con, "modelagem_voto")

rollcall <- data.frame(rollcall=votos$votacao_id, vote=votos$opcao, names(votos))  

