Vagrant.configure("2") do |config|
  
  config.vm.box = "ubuntu/focal64"

  config.vm.hostname = "flask-chat-app"
  config.vm.define "flask-chat-app"

  config.vm.network "forwarded_port", guest: 5000, host: 5000 
  config.vm.network "forwarded_port", guest: 27017, host: 27017 

  config.vm.synced_folder ".", "/home/vagrant/app"

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv mongodb

    cd /home/vagrant/app

    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

    sudo systemctl start mongodb
    sudo systemctl enable mongodb

    export FLASK_ENV=development
    nohup python3 app.py &
  SHELL
end