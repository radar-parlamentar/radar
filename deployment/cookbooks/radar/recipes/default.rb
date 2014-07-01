# License: GPL v3
# Author: Leonardo Leite (2013, 2014)

include_recipe "database::mysql"

mysql_database 'radar' do
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

mysql_database_user 'radar' do
  connection    mysql_connection_info
  password      node['radar']['database_user_password']
  database_name 'radar'
  host          '%'
  privileges    [:select,:update,:insert]
  action        :grant
end


