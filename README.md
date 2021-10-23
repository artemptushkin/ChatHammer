### Requirements

`python=3.9.6` or higher

### How to run locally

One time:

```shell
pip3 install -r requirements.txt
```

Run:
```shell
python3 main.py
```

### How to run as service on linux (debian)

1. Setup python env

```shell
pip install pipenv

pipenv install
```

2. Create linux system service file:

```text
[Unit]
Description=Telegram ChatHammer service
After=multi-user.target

[Service]
Type=simple
ExecStart=/home/pi/your/path/python /home/pi/your/path/project/main.py
Restart=on-abort

[Install]
WantedBy=multi-user.target

```

2. Move it to `/etc/systemd/system/`

```shell
sudo cp example.service /etc/systemd/system/
```
   
3. Setup service

```shell
#Reload the service files to include the new service
sudo systemctl daemon-reload

#Start your service
sudo systemctl start example.service

#To check the status of your service
sudo systemctl status example.service

#To enable your service on every reboot
sudo systemctl enable example.service

#To disable your service on every reboot
sudo systemctl disable example.service
```

### FAQ

#### How to find chat-id

Add `@RawDataBot` to the group, it should print the raw data