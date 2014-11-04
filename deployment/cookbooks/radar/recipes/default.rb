# License: GPL v3
# Author: Leonardo Leite (2014)
# Receita de instalação do Radar Parlamentar

user = node['radar']['user']
home = "/home/#{user}"
radar_folder = "#{home}/radar"
repo_folder = "#{home}/radar/repo"
venv_folder = "#{home}/radar/venv_radar"

#
# Instala e configura Postgresql como a base de dados "radar"
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

template "#{home}/.pgpass" do
  mode '0600'
  owner user
  group user
  source "pgpass.erb"
  variables({
    :senha => node[:postgresql][:password][:postgres]
  })
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

package "vim" do
  action :install
end

#
# Variáveis de ambiente
#

template "#{home}/.profile" do
  mode '0440'
  owner user
  group user
  source "profile.erb"
end

#
# Arquivos de configuração
#

directory "#{radar_folder}" do
  owner user
  group user
  mode '0775'
  action :create
end

template "#{radar_folder}/radar_nginx.conf" do
  mode '0440'
  owner user
  group user
  source "radar_nginx.conf.erb"
  variables({
    :user => user,
    :server_name => "localhost"
  })
end

template "#{radar_folder}/radar_uwsgi.ini" do
  mode '0440'
  owner user
  group user
  source "radar_uwsgi.ini.erb"
  variables({
    :user => user
  })
end

template "#{radar_folder}/uwsgi.conf" do
  mode '0440'
  owner user
  group user
  source "uwsgi.conf.erb"
  variables({
    :user => user
  })
end

template "#{radar_folder}/uwsgi_params" do
  mode '0440'
  owner user
  group user
  source "uwsgi_params.erb"
end

link "/etc/nginx/sites-enabled/radar_nginx.conf" do
  to "#{home}/radar/radar_nginx.conf"
end

file "/etc/nginx/sites-enabled/default" do
  action :delete
end

#
# Código do Radar
#

python_virtualenv "#{venv_folder}" do
  owner user
  group user
  action :create
end

git "#{repo_folder}" do
  repository "git://github.com/leonardofl/radar_parlamentar.git"
  reference "master"
  user user
  group user
  action :sync
end

python_pip "" do
  virtualenv "#{venv_folder}"
  options "-r #{repo_folder}/requirements.txt"
end

#
# Radar <--> Uwsgi <--> Nginx
#

#python_pip "uwsgi" do
#  virtualenv "#{home}/radar/venv_radar"
#end


