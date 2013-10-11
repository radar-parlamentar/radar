/*
  Este Script refere-se ao commit de código: fb7510d9a7d83fad27e8214b1282891eecbe498c
  Acrescentado a cor no objeto partido.
  Atribuido cor preta (#000000) aos sem partido.
  Criado teste unitario test_get_sem_partido.
  Alteração do teste unitario test_partido.

  O script adiciona as cores de cada partido no banco de dados

  As últimas alterações foram feitas em 11/10/2013 nos arquivos:
  radar_parlamentar/radar_parlamentar/modelagem/models.py
  radar_parlamentar/radar_parlamentar/modelagem/test.py
  
 */

alter table modelagem_partido add cor varchar(7);

update modelagem_partido set cor = '#d7bf1f', numero = 51 where nome='PEN';

update modelagem_partido set cor = '#000000'  where numero = 0;
update modelagem_partido set cor = '#15c5ff'  where numero = 10;
update modelagem_partido set cor = '#203487'  where numero = 11;
update modelagem_partido set cor = '#6c85b1'  where numero = 12;
update modelagem_partido set cor = '#FF0000'  where numero = 13;
update modelagem_partido set cor = '#1f1a17'  where numero = 14;
update modelagem_partido set cor = '#CC0000'  where numero = 15;
update modelagem_partido set cor = '#c30909'  where numero = 16;
update modelagem_partido set cor = '#173495'  where numero = 17;
update modelagem_partido set cor = '#cd0600'  where numero = 18;
update modelagem_partido set cor = '#f2ed31'  where numero = 19;
update modelagem_partido set cor = '#25b84a'  where numero = 20;
update modelagem_partido set cor = '#800205'  where numero = 21;
update modelagem_partido set cor = '#110274'  where numero = 22;
update modelagem_partido set cor = '#fea801'  where numero = 23;
update modelagem_partido set cor = '#002664'  where numero = 25;
update modelagem_partido set cor = '#ffff6b'  where numero = 27;
update modelagem_partido set cor = '#312dc1'  where numero = 28;
update modelagem_partido set cor = '#610100'  where numero = 29;
update modelagem_partido set cor = '#65a4fb'  where numero = 31;
update modelagem_partido set cor = '#D51500'  where numero = 33;
update modelagem_partido set cor = '#0066ff'  where numero = 36;
update modelagem_partido set cor = '#ff8d00'  where numero = 40;
update modelagem_partido set cor = '#00CC00'  where numero = 43;
update modelagem_partido set cor = '#67a91e'  where numero = 44;
update modelagem_partido set cor = '#0059AB'  where numero = 45;
update modelagem_partido set cor = '#FFFF00'  where numero = 50;
update modelagem_partido set cor = '#004607'  where numero = 54;
update modelagem_partido set cor = '#80c341'  where numero = 55;
update modelagem_partido set cor = '#da251c'  where numero = 65;
update modelagem_partido set cor = '#2ba138'  where numero = 70;
update modelagem_partido set cor = '#226d2a'  where numero = 56;
update modelagem_partido set cor = '#114d12'  where numero = 71;
update modelagem_partido set cor = '#094196'  where numero = 26;
