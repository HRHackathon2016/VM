# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "hrhackathon"

  config.vm.network "forwarded_port", guest: 8080,    host: 8080
  config.vm.network "forwarded_port", guest: 3306,  host: 33306

  config.vm.network "private_network", ip: "10.4.4.58"

  config.vm.synced_folder "../position_matcher", "/var/www/position_matcher",
    owner: "www-data"

  config.vm.provider "virtualbox" do |vb|
   # Display the VirtualBox GUI when booting the machine
    vb.gui = false
 
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.customize ["modifyvm", :id, "--memory", "512"]
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "95"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y nginx mongodb

    apt-get install -y php5-cli php5-xdebug php5-fpm php5-mongo
    sed -i 's/sendfile on/sendfile off/g' /etc/nginx/nginx.conf
    sed -i 's/;date.timezone =/date.timezone = Europe\\/Berlin/g' /etc/php5/{fpm,cli}/php.ini 
    echo -e "zend_extension=xdebug.so\nxdebug.remote_enable=on\nxdebug.remote_host=127.0.0.1\nxdebug.remote_port=9000\n"|sudo tee /etc/php5/mods-available/xdebug.ini > /dev/null
    cp /vagrant/provisioning/position_matcher.nginx /etc/nginx/sites-available/position_matcher
    ln -fs /etc/nginx/sites-available/position_matcher /etc/nginx/sites-enabled/position_matcher
    nginx -s reload
  SHELL
end

