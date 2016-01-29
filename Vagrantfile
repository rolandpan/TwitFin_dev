# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 80, host: 8888
  # config.vm.network :private_network, ip: "192.168.33.30"
  # config.ssh.insert_key = false

  config.vm.provider :virtualbox do |vb|
    # vb.name = "twitfin.dev"
    vb.memory = 1024
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  # Remove this after Vagrant 1.8.2+ https://github.com/mitchellh/vagrant/issues/6793
  config.vm.provision "shell", inline: <<-EOF
    sudo apt-get install -y python-pip python-dev && \
    sudo pip install ansible==1.9.2 && sudo cp /usr/local/bin/ansible /usr/bin/ansible
  EOF

  # Enable provisioning with Ansible.
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    # ansible.verbose = true
  end

  config.vm.provision "shell", privileged: false, inline: <<-EOF
    echo "Ready!"
    echo "open http://192.168.33.30"
  EOF

end
