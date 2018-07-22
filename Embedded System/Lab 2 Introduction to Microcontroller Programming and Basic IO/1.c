//Fangyao Liu  Exercise 1
//include necessary head file into the code.
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
#include "oi.h"


//sets pin B2 as an output
void Init_Uart(void)
{
	DDRB |= 0x04;
}


void main(void)
{
	Init_Uart();
	
	while(1)
	{
		PORTB |= 0x04;           //sets the state of pin B2 to high
		for(int i=0;i<100;i++)   //loop delay function for 100 times
		_delay_loop_2(46080);    //delay 1 ms
		PORTB &= ~0x04;          //sets the state of pin B2 to low
		for(int i=0;i<100;i++)
		_delay_loop_2(46080);
	}
}

