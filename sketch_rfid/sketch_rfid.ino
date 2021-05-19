#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         22
#define SS_PIN          21

#define greenLed        12
#define redLed          32

MFRC522 mfrc522(SS_PIN, RST_PIN);

int incomingByte = 0; // for incoming serial data
unsigned int hex_num;

void setup() {
	Serial.begin(115200);		// Initialize serial communications with the PC
	while (!Serial);		// Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();		// Init MFRC522
	delay(4);				// Optional delay. Some board do need more time after init to be ready, see Readme
	mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details
	Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
}

void loop() {
	// Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if ( ! mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards
	if ( ! mfrc522.PICC_ReadCardSerial()) {
		return;
	}

  delay(100);

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 1)
    {
      // Dump debug info about the card; PICC_HaltA() is automatically called
      hex_num =  mfrc522.uid.uidByte[0] << 24;
      hex_num += mfrc522.uid.uidByte[1] << 16;
      hex_num += mfrc522.uid.uidByte[2] <<  8;
      hex_num += mfrc522.uid.uidByte[3];
        
      Serial.println(hex_num);
    } else if (incomingByte == 2) {
      digitalWrite(greenLed, HIGH);
      delay(1000);
      digitalWrite(greenLed, LOW);
    } else if (incomingByte == 3)
    {
      digitalWrite(redLed, HIGH);
      delay(1000);
      digitalWrite(redLed, LOW);
    }
  }

  
}
