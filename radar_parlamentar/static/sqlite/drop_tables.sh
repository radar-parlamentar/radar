#!/bin/bash
# Remove tabelas que não importam pra quem quer analisar os dados
# TODO: fazer um for =}

sqlite3 $1 "drop table analises_periodoanalise"
sqlite3 $1 "drop table analises_periodoanalise_posicoes"
sqlite3 $1 "drop table analises_posicaopartido"
sqlite3 $1 "drop table auth_group"
sqlite3 $1 "drop table auth_group_permissions"
sqlite3 $1 "drop table auth_permission"
sqlite3 $1 "drop table auth_user"
sqlite3 $1 "drop table auth_user_groups"
sqlite3 $1 "drop table auth_user_user_permissions"
sqlite3 $1 "drop table django_content_type"
sqlite3 $1 "drop table django_session"
sqlite3 $1 "drop table django_site"


