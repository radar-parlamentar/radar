# License: GPL v3
# Author: Leonardo Leite (2014)

#
# Instala e configura Postgresql com a base de dados "radar"
#

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

#
# Instalando pacotes
#

package "python-pip" do
  action :install
end

package "libpq-dev" do
  action :install
end

package "python-dev" do
  action :install
end

package "git" do
  action :install
end

package "nginx" do
  action :install
end

package "python-virtualenv" do
  action :install
end

package "tmux" do
  action :install
end

package "postgresql-contrib" do
  action :install
end

package "uwsgi-plugin-python" do
  action :install
end

#
# Variáveis de ambiente
#

user = node['radar']['user']
home = "/home/#{user}"

template "#{home}/.profile" do
  mode '0440'
  owner 'vagrant'
  group 'vagrant'
  source "profile.erb"
end


