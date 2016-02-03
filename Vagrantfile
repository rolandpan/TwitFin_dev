# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.ssh.insert_key = false

  config.vm.provider :virtualbox do |vb|
    # vb.name = "twitfin_dev"
    vb.memory = 1024
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.provision "shell", inline: <<-EOF
    sudo apt-get install -y python-pip python-dev python-pandas
    sudo pip install future
    sudo pip install quandl
  EOF
  # python-virtualenv gcc python-gdbm

end
