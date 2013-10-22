# License: GPL v3
# Author: Leonardo Leite (2013)

include_recipe "mysql::server"
include_recipe "database::mysql"

mysql_database 'radarparlamentar' do
  connection(
    :host     => 'localhost',
    :username => 'root',
    :password => node['mysql']['server_root_password']
  )
  action :create
end

mysql_connection_info = {
  :host     => 'localhost',
  :username => 'root',
  :password => node['mysql']['server_root_password']
}

mysql_database_user 'radarparlamentar' do
  connection    mysql_connection_info
  password      node['radar']['database_user_password']
  database_name 'radarparlamentar'
  host          '%'
  privileges    [:select,:update,:insert]
  action        :grant
end

#application 'radar_parlamentar' do
#  path       '$HOME/radar_parlamentar'
#  owner      'nobody'
#  group      'nogroup'
#  repository 'https://github.com/leonardofl/radar_parlamentar.git'
#  revision   'master'
#
#  django do
#    settings_template 'settings.py.erb'
#    debug             true
#    collectstatic     'build_static --noinput'
#    database do
#      database  'radarparlamentar'
#      adapter   'mysql'
#      username  'radarparlamentar'
#      password  node['radar']['database_user_password']
#    end
#  end
#
#  gunicorn do
#    only_if { node['roles'].include? 'packaginator_application_server' }
#    app_module :django
#    port 8080
#  end
#
#end


