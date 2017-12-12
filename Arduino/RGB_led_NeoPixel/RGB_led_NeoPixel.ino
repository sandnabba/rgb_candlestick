#include <Adafruit_NeoPixel.h>

#define PIN 6

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(7, PIN, NEO_GRB + NEO_KHZ800);


void setup() {
  Serial.begin(57600);
  randomSeed(analogRead(0));
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}


const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;
unsigned long last_ping = millis();

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

        //showGroupsOfBytes();
        set_led_new();
        newData = false;
    }
}

void set_led_new() {
  strip.setPixelColor(0, receivedBytes[1], receivedBytes[2], receivedBytes[0]);
  strip.setPixelColor(1, receivedBytes[4], receivedBytes[5], receivedBytes[3]);
  strip.setPixelColor(2, receivedBytes[7], receivedBytes[8], receivedBytes[6]);
  strip.setPixelColor(3, receivedBytes[10], receivedBytes[11], receivedBytes[9]);
  strip.setPixelColor(4, receivedBytes[13], receivedBytes[14], receivedBytes[12]);
  strip.setPixelColor(5, receivedBytes[16], receivedBytes[17], receivedBytes[15]);
  strip.setPixelColor(6, receivedBytes[19], receivedBytes[20], receivedBytes[18]);
  strip.show();
}

// Ping every 30 seconds just to tell python that we're alive
void ping() {
  unsigned long now = millis();
  if (now > last_ping + 30000) {
    unsigned long uptime = now / 1000;
    String string = "Ping, Uptime: ";
    string += uptime;
    Serial.println(string);
    last_ping = now;
  }
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
  ping();
  recvBytesWithStartEndMarkers();
  showNewData();
}
