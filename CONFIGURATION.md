## Set up the W5500 Ethernet Controller

### Enable The W5500 SPI Overlay

Add:

```
dtoverlay=anyspi,spi0-0,dev="w5500",speed=30000000
dtoverlay=w5500
```

To the bottom of `/boot/config.txt`


### Assign a consistent MAC Address

```
sudo nano /lib/systemd/system/setmac.service
```
Add the following contents:

```
[Unit]
Description=Set MAC address for W5500
Wants=network-pre.target
Before=network-pre.target
BindsTo=sys-subsystem-net-devices-eth0.device
After=sys-subsystem-net-devices-eth0.device
[Service]
Type=oneshot
ExecStart=/sbin/ip link set dev eth0 address <MAKE UP A MAC ADDRESS>1
ExecStart=/sbin/ip link set dev eth0 up
[Install]
WantedBy=multi-user.target
```

Save and exit. then:

```
sudo chmod 644 /lib/systemd/system/setmac.service
sudo systemctl daemon-reload
sudo systemctl enable setmac.service
```

Reboot
