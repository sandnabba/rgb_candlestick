
#include <Wire.h>
#include <avr/wdt.h>


int aR = 3;
int aG = 5;
int aB = 6;
int bR = 9;
int bG = 10;
int bB = 11;

int all_pins[] = {3, 5, 6, 9, 10, 11};


void setup() {
  // wdt_enable(WDTO_2S);
  Serial.begin(57600);

  pinMode(aR, OUTPUT);
  pinMode(aG, OUTPUT);
  pinMode(aB, OUTPUT);
  pinMode(bR, OUTPUT);
  pinMode(bG, OUTPUT);
  pinMode(bB, OUTPUT);
  randomSeed(analogRead(0));
}


const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;

void recvBytesWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    byte startMarker = 0xff;
    byte endMarker = 0xfe;
    byte rb;


    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();

        if (recvInProgress == true) {
            if (rb != endMarker) {
                receivedBytes[ndx] = rb;
                ndx++;
                if (ndx >= numBytes) {
                    ndx = numBytes - 1;
                }
            }
            else {
                receivedBytes[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                numReceived = ndx;  // save the number for use when printing
                ndx = 0;
                newData = true;
            }
        }

        else if (rb == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        // Serial.print("This just in ... ");
        // for (byte n = 0; n < numReceived; n++) {
        //     Serial.print(receivedBytes[n], DEC);
        //     Serial.print(' ');
        // }
        // Serial.println();

        // showGroupsOfBytes();
        set_led_new();
        newData = false;
    }
}

void set_led_new() {
  // int x = 0; // LED 1 (Master arduino)
  int x = 3; // LED 2-3
  // int x = 9; // LED 4-5
  // int x = 15;   // LED 6-7
  analogWrite(aR, receivedBytes[0 + x]);
  analogWrite(aG, receivedBytes[1 + x]);
  analogWrite(aB, receivedBytes[2 + x]);
  analogWrite(bR, receivedBytes[3 + x]);
  analogWrite(bG, receivedBytes[4 + x]);
  analogWrite(bB, receivedBytes[5 + x]);
}

void showGroupsOfBytes() {
    for (byte n = 0; n < numReceived; n++) {
        Serial.print(receivedBytes[n], DEC);
        Serial.print(' ');
        if ((n + 1) % 3 == 0) {
            Serial.println();
        }
    }
    Serial.println();
}

void loop() {
  recvBytesWithStartEndMarkers();
  showNewData();
}
