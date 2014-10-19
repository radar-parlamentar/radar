# License: GPL v3
# Author: Leonardo Leite (2013, 2014)

# Instala e configura Postgresql com a base de dados "radar"

include_recipe "database::postgresql"

postgresql_database 'radar' do
  connection(
    :host     => 'localhost',
    :port     => 5432,
    :username => 'postgres',
    :password => node['postgresql']['password']['postgres']
  )
  template 'DEFAULT'
  encoding 'DEFAULT'
  tablespace 'DEFAULT'
  connection_limit '-1'
  owner 'postgres'
  action :create
end

postgresql_connection_info = {
  :host     => 'localhost',
  :port     => node['postgresql']['config']['port'],
  :username => 'postgres',
  :password => node['postgresql']['password']['postgres']
}

postgresql_database_user 'radar' do
  connection postgresql_connection_info
  password node['radar']['database_user_password']
  action :create
end

postgresql_database_user 'radar' do
  connection postgresql_connection_info
  password node['radar']['database_user_password']
  database_name 'radar'
  privileges [:all]
  action :grant
end

