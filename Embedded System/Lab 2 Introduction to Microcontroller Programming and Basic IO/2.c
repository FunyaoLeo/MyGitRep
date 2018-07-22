//Fangyao Liu  Exercise 2
#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
#include "oi.h"

void Init_Uart(void)
{
	DDRB |= 0x04;
	DDRC &= ~0x08;              //sets pin C3 as an input
}                              
                               
void main(void)                
{                              
	Init_Uart();               
                               
	while(1)                   
	{                          
		if(PINC&0x08)           //if the state of pin C3 is high
			PORTB &= ~0x04;     //sets the state of pin B2 to low
			
		else                    //if the state of pin C3 is low
			PORTB |= 0x04;      //sets the state of pin B2 to high
	}
}