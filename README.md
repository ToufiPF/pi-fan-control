# Raspberry Pi 5 + Penta Sata Hat PWM controller for ATX case/fan

I built a small NAS by recycling an old ATX case & power supply.
I've thrown away the motherboard & CPU which were busted, 
and replaced them by a Pi 5 8GB + a Penta Sata Hat and 2 3.5" HDDs (should become 3 soon to enable RAID 5).

This repo holds my experiments to control the fans integrated in my ATX case.

Maybe I'll post some photos of my setup when I have the time.


## Interesting links

- [Pinout for Raspberry Pi 5](https://pinout.xyz)
- [Penta Hat wiki](https://wiki.radxa.com/Penta_SATA_HAT). 
    This is the old wiki page, which holds the _small_ detail that 
    **pin 8 of the Penta Hat can be wired to 2 different Raspberry pins, depending on the board** (physical pins 13 and 33). 
    Out of these 2, only pin 33 supports hardware PWM. 
    My hat is wired to pin 13, so I had to use software PWM ; 
    that caused me a lot of headaches because on the newer [wiki page](https://docs.radxa.com/en/accessories/penta-sata-hat/sata-hat-top-board) only pin 33 is mentioned.
- [rpi-lgpio doc](https://rpi-lgpio.readthedocs.io)
- [rockpi-sata github](https://github.com/radxa/rockpi-sata)

