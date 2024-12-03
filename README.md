# Flask Blog


## Installation

Install Poetry:
https://python-poetry.org/docs/#installation


Install all dependencies using Poetry:
```
poetry install --no-root
```


If you're getting this error while installing dependencies:
```
ModuleNotFoundError: No module named 'distutils.util'
```
You will need to install distutils package first(https://askubuntu.com/questions/1239829/modulenotfounderror-no-module-named-distutils-util):
```
sudo apt install python3-distutils
```


Create `config.json` file in the project root directory. The sample file is `config_sample.json`.


Create database:
```
poetry run python
# Next lines are executed in the Python interpreter.
from flask_blog import db, create_app
app = create_app()
app.app_context().push()
db.create_all()
```


Install Make:
```
sudo apt install make
```


To run the application in the development mode:
```
make run_dev
```


To run the application in the development mode on the unspecified host(might be used on the remote server):
```
make run_dev ARGS="--host 0.0.0.0"
```


To run the application in the production mode using Gunicorn:
```
make run_prod
```


## Deployment server setup (Linode Ubuntu server)

First of all, create an Ubuntu server on Linode. They should create a `root` user for you with the password you specified. Let's say that the ip address they gave is `10.10.100.100`.


SSH to the server:
```
ssh root@10.10.100.100
```


Upgrage all software:
```
apt update && apt upgrade
```


Set hostname:
```
hostnamectl set-hostname flask-blog-server
```


Now `hostname` command should output `flask-blog-server`.


Set hostname in the `/etc/hosts` file:
```
127.0.0.1       localhost
10.10.100.100   flask-blog-server # Add this line.
...
```


Add a user with limited privileges. It will be used instead of the `root` user because it's a lot safer:
```
adduser johndoe
# You will be prompted to set the password.
```


Add `johndoe` user to `sudo` group. It will allow `johndoe` to run commands with `sudo`:
```
adduser johndoe sudo
```


SSH to the server as `johndoe` user:
```
exit
ssh johndoe@10.10.100.100
```


Set the SSH key based authentication(it's safer than the password one), so that you could SSH to the server without typing the password every time. Create `.ssh` directory in the `johndoe` user home directory:
```
mkdir ~/.ssh
```


Create an SSH key on your local machine if you don't have one:
https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/connecting-to-github-with-ssh


Copy the SSH public key from your local machine to the remote server. Let's say that your SSH public key is `id_rsa.pub`:
```
# This command must be executed on the local machine.
scp ~/.ssh/id_rsa.pub johndoe@10.10.100.100:~/.ssh/authorized_keys
```


Now your SSH public key should be copied to `~/.ssh/authorized_keys` file on the remote server.


Set the permissions for the `.ssh` directory on the remove server:
```
sudo chmod 700 ~/.ssh   # Owner of the .ssh directory will have read, write and execute permissions.
sudo chmod 600 ~/.ssh/* # Owner of the files in .ssh directory will have read and write permissions.
```


Now you should be able to SSH to the server without typing the password:
```
exit
ssh johndoe@10.10.100.100
# No password prompt.
```


You should disallow `root` user login over SSH(it's dangerous to login as `root` user) and disallow password authentication(you already have SSH key base authentication which is safer). To do that, edit `/etc/ssh/sshd_config` to have:
```
...
PermitRootLogin no # It will be set to 'yes' before editing.
...
PasswordAuthentication no # It will be set to 'yes' before editing, and might be commented.
...
```


Restart the SSH service:
```
sudo systemctl restart ssh
```


Install Uncomplicated Firewall:
```
sudo apt install ufw
```


Set firewall rules:
```
sudo ufw default allow outgoing # By default, allow all outgoing traffic.
sudo ufw default deny incoming # By default, deny all incoming traffic.
sudo ufw allow ssh # Allow SSH port in order to be able to login.
sudo ufw allow 5000 # Allow port 5000 for testing purpose.
sudo ufw enable # Enable all the rules.
sudo ufw status # Show the rules.
```


Clone the repository:
```
git clone https://github.com/vetalpaprotsky/flask_blog.git
```


Install the project using commands from [the installation section](#Installation).


Run the application in the development mode on the unspecified host in order to test it:
```
make run_dev ARGS="--host 0.0.0.0"
```


After testing, install Nginx:
```
sudo apt install nginx
```


Gunicorn should have been installed by Poetry.


Remove the default Nginx configuration file:
```
sudo rm /etc/nginx/sites-enabled/default
```


Create `/etc/nginx/sites-enabled/flask_blog` Nginx configuration file. The sample file is `nginx_config_sample` and it is located in the root of the project.


Change firewall rules:
```
sudo ufw allow http/tcp # Allow port 80.
sudo ufw delete allow 5000 # Do not allow port 5000 any more.
sudo ufw enable # Enable all the rules.
```


Restart Nginx:
```
sudo systemctl restart nginx
```


Run Gunicorn in the foreground to make sure that production setup works properly:
```
make run_prod
```


The application should be run the background. The software Supervisor is going to help with that.


Install Supervisor:
```
sudo apt install supervisor
```


Create `/etc/supervisor/conf.d/flask_blog.conf` Supervisor configuration file. The sample file is `supervisor_config_sample.conf` and it is located in the root of the project.


Create empty log files for Supervisor:
```
sudo mkdir -p /var/log/flask_blog
sudo touch /var/log/flask_blog/flask_blog.err.log
sudo touch /var/log/flask_blog/flask_blog.out.log
```


Restart Supervisor:
```
sudo supervisorctl reload
```


The application should have been started in the background. Check the log files if something goes wrong.


By default, the maximum file upload size in Nginx is 2 megabytes. Set it to 5 megabytes in the `/etc/nginx/nginx.conf` configuration file:
```
...
http {
...
    client_max_body_size 5M;
...
}
...
```


Restart Nginx:
```
sudo systemctl restart nginx
```


Now the setup should be done!
