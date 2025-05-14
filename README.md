# Raspberry Pi 5 + Penta Sata Hat PWM controller for ATX case/fan

I built a small NAS by recycling an old ATX case & power supply.
I've thrown away the motherboard & CPU which were busted,
and replaced them by a Pi 5 8GB + a Penta Sata Hat and two 3.5" HDDs (should become three soon to enable RAID 5).

This repo holds my experiments to control the fans integrated in my ATX case.


## Installing the script as a systemd service

### Installation

```sh
# install scripts
sudo mkdir /usr/local/src/pi-fan-control
sudo cp *.py /usr/local/src/pi-fan-control/
sudo cp -r controllers /usr/local/src/pi-fan-control/
sudo chmod 755 /usr/local/src/pi-fan-control/main.py

# install config
sudo cp ./pi-fan-control.config /usr/local/etc/pi-fan-control.config
sudo chmod 644 /usr/local/etc/pi-fan-control.config

# install service
sudo cp ./pi-fan-control.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/pi-fan-control.service
sudo systemctl daemon-reload
sudo systemctl enable pi-fan-control.service
```

### Extra command to manage the service

```sh
# start / stop a service
sudo systemctl start pi-fan-control.service
sudo systemctl stop pi-fan-control.service

# get logs from journal
journalctl -u pi-fan-control.service

# restart a service (after configuration change)
sudo systemctl restart pi-fan-control.service
# reload a service (after service's configuration change)
sudo systemctl reload pi-fan-control.service

# enable / disable a service
sudo systemctl enable pi-fan-control.service
sudo systemctl disable pi-fan-control.service

# get the status log of a service
systemctl status pi-fan-control.service
```


## TODO list

- [x] Make a PoC work on my setup
- [ ] Post some photos of said setup when I get the time to
- [x] Wrap this python script as an executable service that can be run at startup, restarted, stopped etc...
- [ ] Read back actual fan speed using TACH signal
- [ ] Integrate disk temperature in duty cycle computation, if available
- [ ] Improve the PWM controller to avoid oscillating when at the boundary between 2 temperatures
- [ ] Add a way to stop/restart the HDDs as Radxa do it in their repo
- [ ] Stop/Restart HDDs as the Pi goes to sleep
- [ ] Stop/Restart HDDs after some time with no activity


## Interesting links

- [Pinout for Raspberry Pi 5](https://pinout.xyz)
- [Radxa Penta Hat wiki](https://wiki.radxa.com/Penta_SATA_HAT) :
    This is the old wiki page, which holds the _small_ detail that
    **pin 8 of the Penta Hat can be wired to 2 different Raspberry pins, depending on the board** (physical pins 13 and 33).
    Out of these 2, only pin 33 supports hardware PWM.
    My hat is wired to pin 13, so I had to use software PWM ;
    that caused me a lot of headaches because on the newer [wiki page](https://docs.radxa.com/en/accessories/penta-sata-hat/sata-hat-top-board)
    only pin 33 is mentioned.
- [rockpi-sata github](https://github.com/radxa/rockpi-sata)

- [ATX power supply connector pinout](http://www.submm.caltech.edu/kids_html/DesignLog/DesignLog179/MillerMUSICReadoutDocs/Roach%20board/ATX12V_24.pdf)
- [4-wire fans pinout](http://www.pavouk.org/hw/fan/en_fan4wire.html)

- [rpi-lgpio doc](https://rpi-lgpio.readthedocs.io) : Python library, meant to be drop-in replacement for lgpio for Raspberry Pi 5
- [gpiozero library](https://gpiozero.readthedocs.io/en/latest) : Python library that allows controls GPIO ; interface cleaner than rpi-lgpio
- [rpi_hardware_pwm](https://github.com/Pioreactor/rpi_hardware_pwm) : Python library that allows to control HW PWM, as opposed to most libraries that only expose SW PWM
