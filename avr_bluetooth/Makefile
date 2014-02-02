# write to device: sudo avrdude -p m48 -P usb -c DRAGON_ISP -U flash:w:a.hex

all: switch

switch.out: switch.c
	avr-gcc -mmcu=attiny2313 -Os switch.c -o switch.out

switch: switch.out
	avr-objcopy -j .text -j .data -O ihex switch.out switch.hex

# Set fuses for 10MHz external resonator, 14CK+65ms startup, no CKDIV8
fuse:
	avrdude -p t2313 -P usb -c DRAGON_ISP -U lfuse:w:0xcf:m -U hfuse:w:0xdf:m -U efuse:w:0xff:m

write: all
	avrdude -p t2313 -P usb -c DRAGON_ISP -U flash:w:switch.hex

clean:
	rm *.out
