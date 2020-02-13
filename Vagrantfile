Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.network "forwarded_port", guest: 8080, host: 8888, host_ip: "127.0.0.1"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "setup.yml"
  end
end