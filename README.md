# Raspberry Pi 5 + Penta Sata Hat PWM controller for ATX case/fan

I built a small NAS by recycling an old ATX case & power supply.
I've thrown away the motherboard & CPU which were busted, 
and replaced them by a Pi 5 8GB + a Penta Sata Hat and two 3.5" HDDs (should become three soon to enable RAID 5).

This repo holds my experiments to control the fans integrated in my ATX case.


## TODO list

- [x] Make a PoC work on my setup
- [ ] Post some photos of said setup when I get the time to
- [ ] Wrap this python script as an executable service that can be run at startup, restarted, stopped etc...
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
    that caused me a lot of headaches because on the newer [wiki page](https://docs.radxa.com/en/accessories/penta-sata-hat/sata-hat-top-board) only pin 33 is mentioned.
- [rpi-lgpio doc](https://rpi-lgpio.readthedocs.io) : Drop-in replacement for lgpio for Raspberry Pi 5
- [rockpi-sata github](https://github.com/radxa/rockpi-sata)
