Vagrant.require_version ">= 1.7.0"

Vagrant.configure(2) do |config|
  config.vm.network "forwarded_port", guest: 25565, host: 25565
  config.vm.network "forwarded_port", guest: 25564, host: 25564
  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end

  config.vm.synced_folder ".", "/vagrant", type: "rsync",
      rsync__exclude: [".git/",".tox/"]

  config.vm.box = "centos/7"

  config.vm.provision "shell", inline: "yum -y install git unzip"
  config.vm.provision "ansible_local" do |ansible|
#    ansible.verbose = "v"
    ansible.become = true
    ansible.extra_vars = {
      user_accept_minecraft_eula: ENV['mc_accept_eula']
    }
    ansible.playbook = "playbook_configure_vagrent.yml"
  end
end
