# Defines our Vagrant environment
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

my_machines={
# 'hostname' => ['IPAddress','Memory in MB','Number of CPUs'],
  'node1'  => ['10.1.15.10','1024','1']
}

$setupScript = <<SCRIPT
echo provisioning docker...
sudo apt-get update
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-trusty main'
sudo apt-get update
sudo apt-get -o Dpkg::Options::="--force-confnew" install --force-yes -y docker-engine=1.10.2-0~trusty
sudo usermod -a -G docker vagrant
curl -L "https://github.com/docker/compose/releases/download/1.6.2/docker-compose-$(uname -s)-$(uname -m)" > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker version

docker-compose version
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/ubuntu-14.04"

  my_machines.each do |short_name, array|

    config.vm.define short_name do |host|
      host.vm.network 'private_network', ip: array[0]
      host.vm.hostname = "#{short_name}"
      host.vm.provider "virtualbox" do |vb|
        vb.memory = "#{array[1]}"
        vb.cpus = "#{array[2]}"
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
        vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
      end
      host.vm.provision :shell, :inline => $setupScript
    end
  end
end
