#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
#include "oi.h"

#define USB 1
#define CR8 2

void setSerial(uint8_t com);
uint8_t getSerialDestination(void);
void writeChar(char c, uint8_t com);
void delay(void);
void byteTx(uint8_t value);
void Init_Uart(void);
uint8_t byteRx(void);


void main(void)
{
uint8_t rx_data;   //create a variable to hold the char sent back
Init_Uart();
while(1)
	{
rx_data = byteRx();  //get the char sent back
writeChar(rx_data,USB);
	}
}


void Init_Uart(void)
{
UBRR0 = 19;
UCSR0B = 0x18;
UCSR0C = 0x06;
DDRB = 0X10;
PORTB = 0X10;
}

void delay(void)
{
int i=0,j=0;

	for(i=1;i<=1000;i++)
	{
		for(j=1;j<=1000;j++)
		{
		} 
	}

}

uint8_t getSerialDestination(void)
{
	if (PORTB & 0x10)
	return USB;
	else
	return CR8;
}

void setSerial(uint8_t com)
{
	if(com == USB)
	PORTB |= 0x10;
	else if(com == CR8)
	PORTB &= ~0x10;
}

void writeChar(char c, uint8_t com)
{
	uint8_t originalDestination = getSerialDestination();
	if (com != originalDestination)
	{
	setSerial(com);
	delay();
	}

	byteTx((uint8_t)(c));
	if (com != originalDestination)
	{
		setSerial(originalDestination);
		delay();
	}
}

void byteTx(uint8_t value)
{
	while(!(UCSR0A & 0x20)) ;
	UDR0 = value;
}

uint8_t byteRx(void)
{
	while(!(UCSR0A & 0x80)) ;   //wait until the serial transmit buffer is empty
	/* wait until a byte is received */
	return UDR0;                //return the data received
}
