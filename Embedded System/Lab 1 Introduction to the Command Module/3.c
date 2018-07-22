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
void WriteString(char str[]);

void main(void)
{
Init_Uart();

while(1)
{
	WriteString("Hello World!");   //print the string
}

}

void Init_Uart(void)
{
UBRR0 = 59;                        //change the baud rate to 19200
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

void WriteString(char str[])     //keep printing each char of the string until the string ends
{
	int i=0;
	while(str[i] != '\0')
	{
		writeChar(str[i],USB);
		i++;
	}
}
