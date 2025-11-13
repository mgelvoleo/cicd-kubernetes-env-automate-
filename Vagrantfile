Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.ssh.insert_key = false

  # Controller node
  config.vm.define "controller" do |controller|
    controller.vm.hostname = "controller"
    controller.vm.network "private_network", ip: "192.168.56.10"
    controller.vm.provider "virtualbox" do |vb|
      vb.name = "controller"
      vb.memory = 2048
      vb.cpus = 2
    end
    controller.vm.provision "shell", inline: <<-SHELL

      #Update system
      apt-get update && apt-get upgrade -y
      
      # Install Ansible
      apt-get install -y software-properties-common
      apt-add-repository --yes --update ppa:ansible/ansible
      apt-get install -y ansible


      # Generate SSH key for controller if not exists
      if [ ! -f /home/vagrant/.ssh/id_rsa ]; then
        ssh-keygen -t rsa -b 4096 -N "" -f /home/vagrant/.ssh/id_rsa
        chown vagrant:vagrant /home/vagrant/.ssh/id_rsa*
      fi
      
      # COPY THE PUBLIC KEY TO SHARED FOLDER (THIS IS THE FIX)
      cp /home/vagrant/.ssh/id_rsa.pub /vagrant/
      chmod 644 /vagrant/id_rsa.pub

      # Add host entries
      echo "192.168.56.11 master"  | sudo tee -a /etc/hosts
      echo "192.168.56.12 worker1" | sudo tee -a /etc/hosts
      echo "192.168.56.13 worker2" | sudo tee -a /etc/hosts
    SHELL
  end

  # Function to add controller's pubkey to other nodes
  def add_pubkey(node, hostname, ip)
    node.vm.hostname = hostname
    node.vm.network "private_network", ip: ip
    node.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-#{hostname}"
      vb.memory = 2048
      vb.cpus = 2
    end

    node.vm.provision "shell", inline: <<-SHELL
      mkdir -p /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh
      # Copy controller's public key (shared via /vagrant folder)
      if [ -f /vagrant/id_rsa.pub ]; then
        cat /vagrant/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
        chmod 600 /home/vagrant/.ssh/authorized_keys
        chown -R vagrant:vagrant /home/vagrant/.ssh
      else
        echo "WARNING: /vagrant/id_rsa.pub not found!"
      fi
    SHELL
  end

  # Master node
  config.vm.define "master" do |master|
    add_pubkey(master, "master", "192.168.56.11")
    master.vm.provider "virtualbox" do |vb|
      vb.memory = 3072
    end
  end

  # Worker1
  config.vm.define "worker1" do |worker|
    add_pubkey(worker, "worker1", "192.168.56.12")
  end

  # Worker2
  config.vm.define "worker2" do |worker|
    add_pubkey(worker, "worker2", "192.168.56.13")
  end
end