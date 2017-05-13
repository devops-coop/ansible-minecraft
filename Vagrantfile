# Defines our Vagrant environment
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

$setupScript = <<SCRIPT
echo provisioning docker...
sudo apt-get update
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-trusty main'
sudo apt-get update
sudo apt-get -o Dpkg::Options::="--force-confnew" install --force-yes -y docker-engine=1.10.2-0~trusty
sudo usermod -a -G docker vagrant
sudo apt-get install python3-pip -y && sudo pip3 install --upgrade pip
sudo pip install docker-compose==1.6.2

docker version

docker-compose version
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/ubuntu-14.04"
  config.vm.define "server" do |host|
    host.vm.hostname = "server"
    host.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = "1"
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
    end
    host.vm.provision :shell, :inline => $setupScript
  end
end
