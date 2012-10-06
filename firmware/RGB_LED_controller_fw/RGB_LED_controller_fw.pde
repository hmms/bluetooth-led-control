/*
 *RGB LED controller with Bluetooth Connectivity
 *Muralidhar M. Shenoy
 *12-11-2011
 *http://murlidharshenoy.wordpress.com/
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * Murlidhar Shenoy wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return 
 * ----------------------------------------------------------------------------
 *
 */
 
#define RED_PIN         9
#define GREEN_PIN       10
#define BLUE_PIN        11
#define POT_PIN         1

int breathe_state;
long previousMillis = 0;
int fadeValue;
int i;
int red_val,green_val,blue_val,val;
int delayVal;
char mode;

void setup() {           
  pinMode(RED_PIN, OUTPUT);  
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(3, OUTPUT);//test Pin
  breathe_state = 0;
  fadeValue = 0 ;
  i = 0;
  delayVal = 10;
  mode = 0;

  Serial.begin(9600);/*Init The Serial Port to start Communicating at 9600 Baud 8N1*/
}

void loop() {
  serial_parser();//the communications part is handled by this function.
  /*Non-blocking delay example http://www.arduino.cc/playground/Code/Sensirion#Example*/
  /*Non Blocking Delay Code Block*/
  /*This Code Gets executed every delayVal milliseconds*/
  /*The LEDs Color is update inside this Block*/

  unsigned long currentMillis = millis();//millis is an Arduino function that gives the number of milliseconds elapsed since microcontroller was powered on 
  if(currentMillis - previousMillis > delayVal) {
    // save the last time you entered the Loop 
    previousMillis = currentMillis;   

    //Put all the functions that need to be update   
    mode_update();
    setLEDColour(red_val,green_val,blue_val);

  }
}  

/*sets the led colour*/
int setLEDColour(int red,int green,int blue){
  analogWrite(RED_PIN,red); 
  analogWrite(GREEN_PIN,green); 
  analogWrite(BLUE_PIN,blue); 
}

#define COLOUR_CHANGER 0
#define COLOUR_BREATHE 1
#define COLOUR_SELECT  2


/*the parser that decides what mode it is from the data received over the UART*/
void serial_parser(){
  char mode_val;
  if(Serial.available() >= 2){
    switch( byte( Serial.read() )) {
    case 'm':
      mode_val = Serial.read();

      switch(mode_val){
      case '0':
        // Serial.print("mode1");
        mode = COLOUR_CHANGER;
        red_val = 0;
        green_val = 0;
        blue_val = 0;
        break;

      case '1':
        //Serial.print("mode2");
        mode = COLOUR_BREATHE;
        red_val = 0;
        green_val = 0;
        blue_val = 0;
        break;

      case '2':
        //Serial.print("mode3");
        mode = COLOUR_SELECT;
        red_val = 0;
        green_val = 0;
        blue_val = 0;
        break;
      }
      break;

    case 'r':
      if(mode == COLOUR_SELECT){
        red_val = Serial.read();/*read the color info only if in color select mode*/
      }
      break;

    case 'g':
      if(mode == COLOUR_SELECT){
        green_val = Serial.read();/*read the color info only if in color select mode*/
      }
      break;

    case 'b':
      if(mode == COLOUR_SELECT){
        blue_val = Serial.read();/*read the color info only if in color select mode*/
      }
      break;

    case 'c':
      Serial.flush();/*for testing*/
      Serial.print("\ntest");
      break;

    case 'd':
      delayVal = Serial.read();/*sets the DelayVal which sets the delay between the execution of the mode_update and setLEDColour functions*/
      Serial.flush();
    }
  }

}

/*the parser sends the updated mode to the mode_update function which calls the actual */
/*function which calculate the intensity for each color*/
void mode_update(){
  switch (mode){
  case COLOUR_CHANGER:
    color_changer();
    break;

  case COLOUR_BREATHE:
    breathe();
    break;

  case COLOUR_SELECT:
    break;
  }
}

/*private function to convert HSV to RGB values*/
void h2rgb(float H, int& R, int& G, int& B) {

  int var_i;
  float S=1, V=1, var_1, var_2, var_3, var_h, var_r, var_g, var_b;

  if ( S == 0 )                      
  {
    R = V * 255;
    G = V * 255;
    B = V * 255;
  }
  else
  {
    var_h = H * 6;
    if ( var_h == 6 ) var_h = 0;      
    var_i = int( var_h ) ;            
    var_1 = V * ( 1 - S );
    var_2 = V * ( 1 - S * ( var_h - var_i ) );
    var_3 = V * ( 1 - S * ( 1 - ( var_h - var_i ) ) );

    if      ( var_i == 0 ) {
      var_r = V     ;
      var_g = var_3 ;
      var_b = var_1 ;
    }
    else if ( var_i == 1 ) {
      var_r = var_2 ;
      var_g = V     ;
      var_b = var_1 ;
    }
    else if ( var_i == 2 ) {
      var_r = var_1 ;
      var_g = V     ;
      var_b = var_3 ;
    }
    else if ( var_i == 3 ) {
      var_r = var_1 ;
      var_g = var_2 ;
      var_b = V     ;
    }
    else if ( var_i == 4 ) {
      var_r = var_3 ;
      var_g = var_1 ;
      var_b = V     ;
    }
    else                   {
      var_r = V     ;
      var_g = var_1 ;
      var_b = var_2 ;
    }

    R = (1-var_r) * 255;                  
    G = (1-var_g) * 255;
    B = (1-var_b) * 255;
  }
}

/*The color transition Modes are implemented here*/

/*The colour changes from blue to red traversing the entire color spectrum*/
void color_changer(){
  int h_int;
  float h;
  if (fadeValue <= 1024) {
    fadeValue += 5;
    if(fadeValue >1024){
      fadeValue = 0 ;
    }
    h = ((float)fadeValue)/1024;
    h2rgb(h,red_val,green_val,blue_val);  
  }
}

/*This mode the each colour individually starts from zero intensity and then reaches maximum intensity*/
/*in the final part of this mode the all the colour simultaneously increase their brightness from zero to maximum and*/
/*go back to zero.*/

#define STATE_1 0
#define STATE_2 1
#define STATE_3 2
#define STATE_4 3
#define STATE_5 4
#define STATE_6 5
#define STATE_7 6
#define STATE_8 7


#if 1
void breathe (){
  switch(breathe_state){

  case STATE_1:
    if(i <255){
      red_val = i;  
      green_val = 0;
      blue_val = 0;
      i++;
    }
    else{
      breathe_state = STATE_2;
    }
    break;

  case STATE_2: 
    if (i>0){
      red_val = i;  
      green_val = 0;
      blue_val = 0;
      i -- ;
    }
    else{
      breathe_state = STATE_3;
      i = 0;
    }
    break;

  case STATE_3:
    if(i <255){
      red_val = 0;  
      green_val = i;
      blue_val = 0;
      i++;
    }
    else{
      breathe_state = STATE_4;
    }
    break;

  case STATE_4: 
    if (i>0){
      red_val = 0;
      green_val = i;
      blue_val = 0;
      i -- ;
    }
    else{
      breathe_state = STATE_5;
      i = 0;
    }
    break;

  case STATE_5:
    if(i <255){
      red_val = 0;  
      green_val = 0;
      blue_val = i;
      i++;
    }
    else{
      breathe_state = STATE_6;
    }
    break;

  case STATE_6: 
    if (i>0){
      red_val = 0;  
      green_val = 0;
      blue_val = i;
      i -- ;
    }
    else{
      breathe_state = STATE_7;
      i = 0;
    }
    break;

  case STATE_7:
    if(i <255){
      red_val = i;  
      green_val = i;
      blue_val = i;
      i++;
    }
    else{
      breathe_state = STATE_8;
    }
    break;

  case STATE_8: 
    if (i>0){
      red_val = i;  
      green_val = i;
      blue_val = i;
      i -- ;
    }
    else{
      breathe_state = STATE_1;
      i = 0;
    }
    break;


  }
}
#endif



