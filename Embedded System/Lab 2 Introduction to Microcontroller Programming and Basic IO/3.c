//Fangyao Liu  Exercise 3
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
#include "oi.h"

void Init_Uart(void)
{
	DDRB |= 0x05;     //sets pin B0 and B2 as outputs
	DDRC &=~0x08;
	
}

void main(void)
{
	Init_Uart();
	while(1)
	{
		if(PINC&0x08)
			PORTB |= 0x04;
		else
			PORTB &= ~0x04;
	}
}
