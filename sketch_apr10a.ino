unsigned char PAUSE_CODE[5] = {0X7E, 0XFF, 0X03, 0X0E, 0XEF};
unsigned char SOFT_MUSIC[8] = {0X7E, 0XFF, 0X06, 0X03, 0X00, 0X00, 0X01, 0XEF};
unsigned char PASSION_MUSIC[8] = {0X7E, 0XFF, 0X06, 0X03, 0X00, 0X00, 0X02, 0XEF};
int LEDPin = 3;
char comdata = 0;

void setup() {
  pinMode(LEDPin,OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  //Serial.write(PASSION_MUSIC,8);

    while(1){
    if(Serial.available() > 0)  
    {
        comdata = char(Serial.read());
        //Serial.println(comdata);
        delay(10);
        if(comdata == 65){
        Serial.println('B');  //confirm the device
        }
        if(comdata == 'K'){
        Serial.println('B');  //confirm the device
        break;
        }
    }
    }
}

void loop() {
  digitalWrite(13, HIGH);
  if(Serial.available() > 0 ){
        comdata = char(Serial.read());
        //Serial.println(comdata);
        delay(10);
        if(comdata == 'X'){
        Serial.write(PAUSE_CODE,5);
        analogWrite(LEDPin,0); //turn off light
        }
        if(comdata == 'S'){
        Serial.write(SOFT_MUSIC,8);
        analogWrite(LEDPin,50); //darken the light
        }
        if(comdata == 'P'){
        Serial.write(PASSION_MUSIC,8);
        analogWrite(LEDPin,200); //lighten the light
        }
        
    }  
}
