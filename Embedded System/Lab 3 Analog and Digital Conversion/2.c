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
void SendStringtoPC(char *Message);


void Init_Uart(void)
{
	DDRC &= ~0x30;
	DIDR0 |= 0x30;
	PRR &= ~0x01;
	ADCSRA = 0x87;
	ADMUX = 0x40;
	
	UBRR0 = 19;      //set the baud rate to 57600
	UCSR0B = 0x18;   //enable the transmit and receive functions of the serial port
	UCSR0C = 0x06;   //selects 8-bit data
	DDRB = 0X10;     //set pin B4 as an output
	PORTB = 0X10;    //set pin B4 to high
}

void intToChar(int meas_c4, char* Str)     //a function to transfer char first to its ASCII, then transfer it to hex number
{
	int p=meas_c4;                        //get the ASCII of the char
	int i = 0; 
	char decitable[]="0123456789";   //create char table for transferring
	while(i != 4)
	{
		Str[i] = decitable[p%10];
		p = p/10;
		i++;
	}
}

void main(void)
{
	
	Init_Uart();
	uint64_t meas_c4;
	char Str[4];
	int i;
	while(1)
	{
		i=3;
		ADMUX &= ~0x0F;
		ADMUX |= 0x04;
		ADCSRA |= 0x40;
		while(ADCSRA & 0x40);
		meas_c4 = (uint64_t) ADC*5000/1023;
		intToChar(meas_c4, Str);
		SendStringtoPC("The analog input voltage is:");
		while(i>=0)
		{
			writeChar(Str[i],USB); //transmit char 'A' to computer
			if (i==3) writeChar('.', USB);
			i--;
		}
		writeChar(' ', USB);
		writeChar('\n', USB);
		writeChar('\r', USB);
	}
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

void SendStringtoPC(char *Message)
{
	while(*Message)
	{
	    while(!(UCSR0A & _BV(UDRE0))) ;
		UDR0 = *Message;
		Message++;
	}
}