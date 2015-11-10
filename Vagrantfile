# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 25565, host: 25565
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
  end
  config.vm.provision "ansible" do |ansible|
    ansible.playbook  = "tests/site.yml"
    ansible.sudo      = true
    ansible.verbose   = "v"
  end
end
