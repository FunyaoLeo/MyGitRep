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
	DDRC |= 0x0F;       //set PC0,PC1,PC2,PC3 as output
	DDRC &= ~0x30;
	DIDR0 |= 0x30;
	PRR &= ~0x01;
	ADCSRA = 0x87;
	ADMUX = 0x40;
	
	UBRR0 = 19;      
	UCSR0B = 0x18;   
	UCSR0C = 0x06;   
	DDRB = 0X10;     
	PORTB = 0X10;    
}

void intToChar(int meas_c4, char* Str)     
{
	int p=meas_c4;                        
	int i = 0; 
	char decitable[]="0123456789";   
	while(i != 4)
	{
		Str[i] = decitable[p%10];
		p = p/10;
		i++;
	}  
}

void intToBi(int k, char* Str)      //function that transfer integer to binary string
{
	char bitable[]="01";
	int i = 0;
	while(i!=4)
	{
		Str[i] = bitable[k%2];
		k=k/2;
		i++;
	}
	
}

void main(void)
{
	
	Init_Uart();
	uint64_t meas_c4;
	char Str[4];
	int i;
	int k;
	int p;
	k=0;
	PORTC &= 0xF0;                 //Initialize and mask different bits of port c       
	while(1)
	{

		if(k>15) k=0;             //If k reaches (10000)B, change k to (0000)B again. 
		PORTC |= k;               //Set PC 3,2,1,0 as k
		SendStringtoPC("The analog input voltage for ");
		intToBi(k, Str);          //change k into binary string
		i=3;
		while(i>=0)
		{
			writeChar(Str[i],USB); 
			i--;
		}
		k++;
		
		ADMUX &= ~0x0F;
		ADMUX |= 0x04;
		ADCSRA |= 0x40;
		while(ADCSRA & 0x40);
		SendStringtoPC(" is: ");
		meas_c4 = (uint64_t) ADC*5000/1023;
		intToChar(meas_c4, Str);
		
		i=3;
		while(i>=0)
		{
			writeChar(Str[i],USB); 
			if (i==3) writeChar('.', USB);
			i--;
		}
		writeChar('\n', USB);
		writeChar('\r', USB);
		for(p=0;p<100;p++)      //delay 1 second
		_delay_loop_2(46080);   
		PORTC &= 0xF0;         //clear PC 3,2,1,0 to zero
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

void SendStringtoPC(char *Message)
{
	while(*Message)
	{
	    while(!(UCSR0A & _BV(UDRE0))) ;
		UDR0 = *Message;
		Message++;
	}
}