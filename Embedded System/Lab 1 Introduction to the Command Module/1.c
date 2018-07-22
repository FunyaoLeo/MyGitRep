//include the ncessary head files that will be used in this file

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
#include "oi.h"

//name certain ports 

#define USB 1
#define CR8 2

//declare functions that will be created later

void setSerial(uint8_t com);
uint8_t getSerialDestination(void);
void writeChar(char c, uint8_t com);
void delay(void);
void byteTx(uint8_t value);
void Init_Uart(void);

//main function, call Init_Uart() and keep writing the "AB1:"

void main(void)
{
Init_Uart();
while(1)   //use while to loop the transmission
	{
		writeChar('A',USB); //transmit char 'A' to computer
		writeChar('B',USB); //transmit char 'B' to computer
		writeChar('1',USB); //transmit char '1' to computer
		writeChar(':',USB); //transmit char ':' to computer
	}
}

//Preset the USART Baud Rate Register, UCSRnB Register, UCSRnC Register, Port B direction register and Port B data register.

void Init_Uart(void)
{
UBRR0 = 19;      //set the baud rate to 57600
UCSR0B = 0x18;   //enable the transmit and receive functions of the serial port
UCSR0C = 0x06;   //selects 8-bit data
DDRB = 0X10;     //set pin B4 as an output
PORTB = 0X10;    //set pin B4 to high
}

//Write a delay function to delay certain time before executing some commands.

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

//acquire the destination for WriteChar function

uint8_t getSerialDestination(void)
{
	if (PORTB & 0x10)
	return USB;
	else
	return CR8;
}

//set the communication interface

void setSerial(uint8_t com)
{
	if(com == USB)
	PORTB |= 0x10;
	else if(com == CR8)
	PORTB &= ~0x10;
}

//WriteChar function takes char and destination. It will use setSerial and getSerialDestination function to build communication interface
//and set com as USB, then transmit the byte. After that, 
 
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

//When UCSR0A is ready, set UDR0 as the char which will be transmitted

void byteTx(uint8_t value)
{
	while(!(UCSR0A & 0x20)) ;
	UDR0 = value;
}
