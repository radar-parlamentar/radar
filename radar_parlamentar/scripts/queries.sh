Algumas queries SQL úteis

Lista de parlamentares de uma casa legislativa:
select par.nome, par.genero, leg.inicio, leg.fim, leg.localidade, part.nome from (modelagem_legislatura as leg join modelagem_partido as part on leg.partido_id = part.id) join modelagem_parlamentar as par on par.id = leg.parlamentar_id where leg.casa_legislativa_id = ID_CASA_LEGISLATIVA;
