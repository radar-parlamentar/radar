-- Algumas queries SQL úteis

-- Lista de parlamentares de uma casa legislativa:
SELECT par.nome, par.genero, leg.inicio, leg.fim, leg.localidade, part.nome FROM (modelagem_legislatura AS leg JOIN modelagem_partido AS part ON leg.partido_id = part.id) JOIN modelagem_parlamentar AS par ON par.id = leg.parlamentar_id WHERE leg.casa_legislativa_id = ID_CASA_LEGISLATIVA;

-- Conta quantos parlamentares existem em uma casa legislativa
SELECT count(*) FROM modelagem_legislatura AS leg JOIN modelagem_parlamentar AS par ON par.id = leg.parlamentar_id WHERE leg.casa_legislativa_id = ID_CASA_LEGISLATIVA;

-- Listar votações concatenadas a suas proposições de uma casa legislativa
SELECT vot.id_vot, vot.descricao, vot.data, prop.sigla, prop.numero, prop.ano FROM modelagem_votacao AS vot JOIN modelagem_proposicao AS prop ON vot.proposicao_id = prop.id WHERE prop.casa_legislativa_id = ID_CASA_LEGISLATIVA;

-- Conta quantas votações tem uma casa legsilativa
SELECT count(*) FROM modelagem_votacao AS vot JOIN modelagem_proposicao AS prop ON vot.proposicao_id = prop.id WHERE prop.casa_legislativa_id = ID_CASA_LEGISLATIVA;

-- Conta quantas votações tem em cada casa legislativa
SELECT prop.casa_legislativa_id, count(*) FROM modelagem_votacao AS vot JOIN modelagem_proposicao AS prop ON vot.proposicao_id = prop.id GROUP BY prop.casa_legislativa_id;


