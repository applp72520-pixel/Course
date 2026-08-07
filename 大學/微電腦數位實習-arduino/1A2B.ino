#include <Arduino.h>
#include "PinDefinitionsAndMore.h"
#define IR_USE_AVR_TIMER3
#include <IRremote.hpp>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
int answer[4], guess[4], length = 0;

void setans()
{
    for (int i = 0; i < 4; i++)
    {
        answer[i] = random(10);

        for (int j = 0; j < i; j++)
        {
            if (answer[i] == answer[j])
            {
                i--;
                break;
            }
        }
    }
}

void setup()
{
    Serial.begin(115200);
    Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
    Serial.print(F("Ready to receive IR signals of protocols: "));
    printActiveIRProtocols(&Serial);
    Serial.println(F("at pin " STR(IR_RECEIVE_PIN)));
    lcd.init();
    lcd.backlight();
    randomSeed(analogRead(0));
    setans();
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
}

void loop()
{
    if (length < 4)
    {
        if (length == 0)
        {
            lcd.setCursor(0, 0);
            lcd.print("ENTER NUMBER:");
            lcd.setCursor(0, 1);
            lcd.print("----");
        }

        if (IrReceiver.decode())
        {
            for (int i = 0; i < 4; i++)
            {
                Serial.print(answer[i]);
            }

            Serial.println();
            IrReceiver.printIRResultShort(&Serial);
            IrReceiver.printIRSendUsage(&Serial);

            if (IrReceiver.decodedIRData.protocol == UNKNOWN)
            {
                Serial.println(F("Received noise or an unknown (or not yet enabled) protocol"));
                IrReceiver.printIRResultRawFormatted(&Serial, true);
            }

            Serial.println();
            IrReceiver.resume();

            int number = -1;

            if (IrReceiver.decodedIRData.command == 0x16) // 0
            {
                number = 0;
            }
            else if (IrReceiver.decodedIRData.command == 0xC) // 1
            {
                number = 1;
            }
            else if (IrReceiver.decodedIRData.command == 0x18) // 2
            {
                number = 2;
            }
            else if (IrReceiver.decodedIRData.command == 0x5E) // 3
            {
                number = 3;
            }
            else if (IrReceiver.decodedIRData.command == 0x8) // 4
            {
                number = 4;
            }
            else if (IrReceiver.decodedIRData.command == 0x1C) // 5
            {
                number = 5;
            }
            else if (IrReceiver.decodedIRData.command == 0x5A) // 6
            {
                number = 6;
            }
            else if (IrReceiver.decodedIRData.command == 0x42) // 7
            {
                number = 7;
            }
            else if (IrReceiver.decodedIRData.command == 0x52) // 8
            {
                number = 8;
            }
            else if (IrReceiver.decodedIRData.command == 0x4A) // 9
            {
                number = 9;
            }

            if (number == -1)
            {
                return;
            }

            for (int i = 0; i < length; i++)
            {
                if (guess[i] == number)
                {
                    return;
                }
            }

            lcd.setCursor(length, 1);
            lcd.print(number);
            guess[length] = number;
            length++;
        }
    }
    else
    {
        int a = 0, b = 0;

        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < 4; j++)
            {
                if (answer[i] == guess[j])
                {
                    if (i == j)
                    {
                        a++;
                    }
                    else
                    {
                        b++;
                    }
                }
            }
        }

        if (a == 4)
        {
            lcd.setCursor(0, 0);
            lcd.print("YOU WIN      ");
            IrReceiver.stop();
            tone(3, 440.00, 500);
            digitalWrite(5, HIGH);
            delay(3000);
            digitalWrite(5, LOW);
            setans();
            IrReceiver.start(8000);
            length = 0;
        }
        else
        {
            lcd.setCursor(0, 0);
            lcd.print(a);
            lcd.setCursor(1, 0);
            lcd.print("A");
            lcd.setCursor(2, 0);
            lcd.print(b);
            lcd.setCursor(3, 0);
            lcd.print("B         ");
            IrReceiver.stop();
            tone(3, 261.63, 500);
            digitalWrite(4, HIGH);
            delay(1500);
            digitalWrite(4, LOW);
            IrReceiver.start(8000);
            length = 0;
        }

        IrReceiver.resume();
    }
}
