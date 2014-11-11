# License: GPL v3
# Author: Leonardo Leite (2014)
# Receita de instalação do Radar Parlamentar

user = node['radar']['user']
home = "/home/#{user}"
radar_folder = "#{home}/radar"
repo_folder = "#{home}/radar/repo"
venv_folder = "#{home}/radar/venv_radar"
cache_folder = "/tmp/django_cache"
log_folder = "/var/log/radar"
log_file = "#{log_folder}/radar.log"
uwsgi_log_folder = "/var/log/"
uwsgi_log_file = "/var/log/uwsgi.log"

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
# Código e configuração do Radar
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

directory "#{cache_folder}" do
  owner user
  group user
  mode '666'
  action :create
end

template "#{repo_folder}/radar_parlamentar/settings/production.py" do
  mode '0440'
  owner user
  group user
  source "production.py.erb"
  variables({
    :dbname => 'radar',
    :dbuser => 'radar',
    :dbpassword => node['postgresql']['password']['postgres'],
    :cache_folder => cache_folder,
    :log_file => log_file
  })
end

directory log_folder do
  owner user
  group user
  mode '0755'
  action :create
end

execute "syncdb" do
  command "#{venv_folder}/bin/python manage.py syncdb --noinput"
  environment ({"DJANGO_SETTINGS_MODULE" => "settings.production"})
  cwd "#{repo_folder}/radar_parlamentar"
  user user
  group user
  action :run
end

execute "migrate" do
  command "#{venv_folder}/bin/python manage.py migrate"
  environment ({"DJANGO_SETTINGS_MODULE" => "settings.production"})
  cwd "#{repo_folder}/radar_parlamentar"
  user user
  group user
  action :run
end

#
# Uwsgi
#

python_pip "uwsgi" do
end

directory uwsgi_log_folder do
  owner user
  group user
  mode '0755'
  action :create
end

template "/etc/init/uwsgi.conf" do
  mode '0440'
  owner 'root'
  group 'root'
  source "uwsgi.conf.erb"
  variables({
    :uwsgi_log_file => uwsgi_log_file,
    :radar_folder => radar_folder
  })
end

service "uwsgi" do
  provider Chef::Provider::Service::Upstart
  action :restart
end

#
# Nginx
#

service "nginx" do
  action :restart
end



