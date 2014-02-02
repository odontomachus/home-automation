#include <stdlib.h>

#define F_CPU 10000000UL  // 1 MHz
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#define BAUDRATE 9600UL
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

#define PIN_TRIGGER PB3
#define PIN_LED PB4
#define PIN_SWITCH PB1

volatile static uint8_t status = 0;

unsigned int ubrr;

void USART_Init()
{
    /* Set baud rate (using u2x=1 doubles effective baud rate) */
    ubrr = (unsigned long) (F_CPU/16UL/BAUDRATE) - 1;
    UBRRH = (unsigned char) ubrr>>8;
    UBRRL = (unsigned char) ubrr;
    /* Enable receiver, transmitter and rx complete interrupt */
    UCSRB = (1<<RXEN)|(1<<TXEN)|(1<<RXCIE);
    /* Set frame format: 
     * 8 bit data (UCSZ2:0 = 0b011) 
     * 1 stop bit (USBS = 0) 
     * Async. op (UMSEL = 0) 
     * No parity (UPM1:0 = 0b00)*/ 
    UCSRC = (3<<UCSZ0);
}

/**
 * Send a byte.
 */
void USART_Transmit( unsigned char data )
{
    /* Wait for empty transmit buffer */
    while ( !( UCSRA & (1<<UDRE)) )
        ;
    /* Put data into buffer, sends the data */
    UDR = data;
}

void USART_Flush( void )
{
    unsigned char dummy;
    while ( UCSRA & (1<<RXC) ) dummy = UDR;
}

/**
 * Toggle the status and two output pins.
 */
void toggle() {
    status ^= 1U;
    if (status) {
        PORTB |= (1<<PIN_TRIGGER)|(1<<PIN_LED);
    }
    else {
        PORTB &= ~((1<<PIN_TRIGGER)|(1<<PIN_LED));
    }
    // Prevent too fast switching
    _delay_ms(1500);
    USART_Flush();
}

/*
 * ISR RX complete
 * Receive a byte from serial and act on it.
 */
ISR(USART_RX_vect) {
    cli();
    uint8_t r = UDR;
    switch (r) {
    case '?':
        USART_Transmit(status ? *"1" : *"0");
        break;
    case 'T':
        // @TODO toggle switch
        toggle();
        break;
    default:
        USART_Transmit(*"?");
        USART_Transmit(r);
        break;
    }
    sei();
}

void init_main() {
    DDRB |= (1<<PIN_LED)|(1<<PIN_TRIGGER);
    PORTB |= (1<<PIN_LED);
    USART_Init(9600);
    // Give the bluetooth time to boot...
    _delay_ms(1500);
    USART_Transmit(*"O");
    USART_Transmit(*"K");
    PORTB ^= (1<<PIN_LED);
}

int main () {
    init_main();
    sei();
    while (1) {
        if (PINB & (1<<PIN_SWITCH)) {
            cli();
            toggle();
            sei();
        }
    }
}

