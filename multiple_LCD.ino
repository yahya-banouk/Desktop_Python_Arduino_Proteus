  
  #include <Wire.h>
  #include <LiquidCrystal_I2C.h>
  #include <SoftwareSerial.h>
  #include <DS3231.h>
  #include <SPI.h>
  #include <MFRC522.h>

  SoftwareSerial BT(0, 1); 
  DS3231  rtc(SDA, SCL);  
  Time t;
  const int stepsPerRevolution = 10; 
  
  const int led_orange=4;
  const int led_vert=3;
  const int led_rouge=2;
  const int IR=8;
  const int BT1=A0;
  const int BT2=A1;
  const int POT=A3;
  const int buzzer=5; 
  // Moteur 1
  const int IN1 = 7;
  const int ENA = 6;
//  unsigned long t=120000 ;
//  unsigned long t1=105000 ;
  unsigned long t2=6000 ;
  unsigned long t1=4000 ;
  unsigned long first_time=0 ;
  unsigned long last_time=0 ;
  int compteur=0;
  int vitesse1=0;
  int vitesse=0;
  byte etat = 1;
  char cause = "cause 1";
  char a='a'; 
  
  LiquidCrystal_I2C lcd(0x3F,20,4);
  
  //************** RFID ********************// 
    #define RST_PIN 9
    #define SS_PIN 10
    
    byte readCard[4];
    int successRead;
    int n;
    
    MFRC522 mfrc522(SS_PIN, RST_PIN);
    MFRC522::MIFARE_Key key;
  //*********************************************//
  
  void setup()
  {
      pinMode(BT1,INPUT);
      pinMode(BT2,INPUT);
      pinMode(POT,INPUT);
      pinMode(IR,INPUT);
      
      pinMode(IN1, OUTPUT);
      pinMode(ENA, OUTPUT);
      
      pinMode(led_orange,OUTPUT);
      pinMode(led_vert,OUTPUT);
      pinMode(led_rouge,OUTPUT);
      pinMode(buzzer,OUTPUT);
      rtc.begin();
      // The following lines can be uncommented to set the date and time
      //rtc.setDOW(WEDNESDAY);     // Set Day-of-Week to SUNDAY
      //rtc.setTime(12, 0, 0);     // Set the time to 12:00:00 (24hr format)
      //rtc.setDate(1, 1, 2014);   // Set the date to January 1st, 2014

      Serial.begin(9600);
      BT.begin(9600);
      BT.println("Hello from Arduino");
      
      lcd.init(); //lcd 1 startup
      lcd.backlight();
      lcd.setCursor(0,1);
      lcd.print("      LAD   ");
      lcd.setCursor(0,2);
      lcd.print(" 333 M&L T7 " ); 
      
      delay(1000);
      lcd.clear();
      
      SPI.begin();
      mfrc522.PCD_Init();
      
  }
  
  void loop()
  {

    getID();
    Serial.print("RFID : ");
    Serial.println(n);
    
    if (BT.available())
      {
        a=(BT.read());
       if (a=='a')
          {
            BT.println("Cause 1");
            cause = "cause 1";
            digitalWrite(led_orange, HIGH); 
          }
        if (a=='m')
          {
            BT.println("Cause 2");
            cause = "cause 2";
            digitalWrite(led_orange, LOW);
          }  
      }
    if(digitalRead(BT1)==0 || digitalRead(BT2)==0 )
      {
       digitalWrite(led_vert, LOW);  
       digitalWrite(led_rouge, HIGH); 
       etat = 0;
      }
      
    if(digitalRead(BT1)==1 && digitalRead(BT2)==1 )
      {   
        etat = 1;
        digitalWrite(led_vert, HIGH);  
        digitalWrite(led_rouge, LOW);
        
        // Send Day-of-Week
        Serial.print(rtc.getDOWStr());
        Serial.print(" ");
        // Send date
        Serial.print(rtc.getDateStr());
        Serial.print(" -- ");
        // Send time
        Serial.println(rtc.getTimeStr());
        
        if(digitalRead(IR)==1)
            {
              t = rtc.getTime();
              first_time= t.hour*60*60+ t.min *60 +t.sec;
              delay(1000);
              
              if(digitalRead(IR)==0)
                 {
                  compteur =compteur+1;
                 }
            }
        

        t = rtc.getTime();
        last_time= t.hour*60*60+ t.min *60 +t.sec;
        Serial.println("first_time : ");
        Serial.println(first_time/1000);
        Serial.println("last_time : ");
        Serial.println(last_time/1000);
        if((last_time-first_time)> t1 && (last_time-first_time)< t2)
         {
          digitalWrite(buzzer, HIGH);
          delay(200); 
          digitalWrite(buzzer, LOW);
          delay(100); 
         }
   
        vitesse1=map(analogRead(POT), 0, 1023, 0, 255); 
        vitesse=map(vitesse1, 0, 255, 0, 100);
        
       if((last_time-first_time)> t2)
         {
          march_avant(vitesse1);
          arret();
          first_time=0;
         }
        }
      lcd.clear();
      lcd.backlight(); 
      lcd.setCursor(1,0);
      lcd.print(t.date);
      lcd.print(".");
      lcd.print(t.mon);
      lcd.print(".");
      lcd.print(t.year);
      lcd.print(" -- ");  
      lcd.print(t.hour);  
      lcd.print(":");  
      lcd.print(t.min);   
   
      lcd.setCursor(0,1);
      lcd.print(" Systeme : ");
      if(etat==1)lcd.print("en marche");
      else lcd.print("en arret");
      lcd.setCursor(0,2);
      lcd.print(" Vitesse : ");
      lcd.print(vitesse);
      lcd.print(" % ");
      lcd.setCursor(0,3);
      lcd.print(" Quantite : ");
      lcd.print(compteur);       
      delay(1000);
      

  }

void march_avant(int vitesse1)
{
// Marche Avant
  analogWrite(ENA, vitesse1);
  digitalWrite(IN1, 1);
  Serial.println("moteur tourne");
  delay(100);
}

void arret()
{
  // Arrêt des moteurs
  analogWrite(ENA, 0);
  digitalWrite(IN1, 0);
  Serial.println("moteur en arret");
  delay(100);
}

int getID() {
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
      { 
        return 0;
      }
  if ( ! mfrc522.PICC_ReadCardSerial()) 
      {
        return 0;
      }
  Serial.print("Card ID: ");

  for (int i = 0; i < mfrc522.uid.size; i++) 
      { 
        readCard[i] = mfrc522.uid.uidByte[i];
        Serial.print(readCard[i], DEC);
      }
  n=readCard[1];
  mfrc522.PICC_HaltA();
  Serial.println();
  return 1;
}

//       ///////////////////////////////////////////
//      ////// Send data over Bluetooth //////
//      /////////////////////////////////////////
//      
//        BT.print("*T"+String(t)+"*");
//        BT.print("*H"+String(h)+"*");
