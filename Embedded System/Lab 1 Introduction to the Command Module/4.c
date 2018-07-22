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
void charToHex(char ch, char* hexStr);
char hexToChar(char* hexStr);


void main(void)
{
	uint8_t rx_data;
	char hexStr[2];
	Init_Uart();
	while(1)
	{
		charToHex(byteRx(), hexStr);     //change the data received to hex value
		writeChar(hexStr[0],USB);        //print high bit of hex value
		writeChar(hexStr[1],USB);        //print low bit of hex value
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
	while(!(UCSR0A & 0x80)) ;
	/* wait until a byte is received */
	return UDR0;
}

void charToHex(char ch, char* hexStr)     //a function to transfer char first to its ASCII, then transfer it to hex number
{
	int p=(int)ch;                        //get the ASCII of the char
	char hextable[]="0123456789ABCDEF";   //create char table for transferring
	hexStr[0]=hextable[p/16];             //get the hex value of high bit
	hexStr[1]=hextable[p%16];             // get the hex value of low bit

}
