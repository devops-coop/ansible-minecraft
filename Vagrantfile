# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

DEFAULT_BOX = :trusty64
BOXES = {
  :centos7  => "centos/7",
  :jessie64 => "debian/jessie64",
  :trusty64 => "ubuntu/trusty64",
}

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  BOXES.each do |name, code|

    primary = (name == DEFAULT_BOX)
    autostart = primary

    config.vm.define name, primary: primary, autostart: autostart do |machine|
      machine.vm.box = code
      machine.vm.network "forwarded_port", guest: 25565, host: 25565
      machine.vm.provider "virtualbox" do |v|
        v.memory = 2048
      end

      machine.vm.provision "ansible" do |ansible|
        ansible.playbook  = "vagrant/vagrant.yml"
        ansible.sudo      = true
      end

      machine.vm.provision "ansible" do |ansible|
        ansible.playbook  = "tests/site.yml"
        ansible.sudo      = true
        ansible.verbose   = "v"
      end

    end
  end
end
