/* 
   The Arduino IRremote library for Infrared communications
   https://github.com/shirriff/Arduino-IRremote
   Follow the instructions for installing an Arduino library here
   https://learn.sparkfun.com/tutorials/installing-an-arduino-library
*/
#include <IRremote.h>

/* 
   IR remote control commands. These commands are sent to the Roomba four times in a row with a small delay 
   between them.
*/

// Clean 
const unsigned int clean[15] = {3000,1000,1000,3000,1000,3000,1000,3000,3000,1000,1000,3000,1000,3000,1000};
// Power Button
const unsigned int power[15] = {3000,1000,1000,3000,1000,3000,1000,3000,3000,1000,1000,3000,3000,1000,1000};
// Dock
const unsigned int dock[15] =  {3000,1000,1000,3000,1000,3000,1000,3000,3000,1000,3000,1000,3000,1000,3000};

// This is the instance of the IRremote library that we are going to be using.
IRsend irsend;

// This is the function that sends the given command four times so that the Roomba picks it up and understands it.
void sendRoombaCommand(unsigned int* command){
  for (int i = 0; i < 4; i++){
    irsend.sendRaw(command, 15, 38);
    delay(50);
  }
}


// The commands are the text that we are going to be sending over serial to the Arduino.
#define MAX_COMMAND_LENGTH	30
char commandBuffer[MAX_COMMAND_LENGTH];

/* 
   This function clears out the buffer that holds the command so that it is clean and ready
   for the next command
*/
int clearCommandBuffer(char commandBuffer[30]){
  for (int i = 0; i < MAX_COMMAND_LENGTH; i++){
    int j = i - 1;
    commandBuffer[j] = 0;
  }
}

/*
   The setup function is called when the sketch starts and is used to initialize variables
   or in our case, setup and start using the serial port.
*/
void setup() {
  Serial.begin(9600);
}

/*
   This is the main program loop. For our purposes, it will listen for commands (words) on
   the serial port, and then translate them into IR signals that the Roomba can understand.
   It will keep doing this one function until the power is shut off.
*/
void loop() {
  clearCommandBuffer(commandBuffer);
  // Only do something if something was received from serial. This avoids us being a processor hog.
  if (Serial.available() > 0) {
    /* 
       We are reading bytes until a space (' ') is received. This makes it easier to write something
       that looks more natural to a human such as "Turn on". Later we also demonstrate using something
       easier for a computer to understand in the form of "gohome" which does not have a space.
    */
    Serial.readBytesUntil(' ', commandBuffer, MAX_COMMAND_LENGTH);
    // The following section is set up to makes sense of the commands "turn on" and "turn off"
    if(strcmp(commandBuffer, "turn") == 0){
      clearCommandBuffer(commandBuffer);
      /* 
         Unlike the previous examples, in the next line we are reading until a null ('\0') is 
         encountered. It is historically traditional for languages, such as C, to end their strings
         with a null byte. This null byte therefore marks the end of our string and the second word
         of the command.
      */
      Serial.readBytesUntil('\0', commandBuffer, MAX_COMMAND_LENGTH);
      if(strcmp(commandBuffer, "on") == 0){
        Serial.write("Turning on Roomba\n");
        sendRoombaCommand((unsigned int *)power);
      }
      else if(strcmp(commandBuffer, "off") == 0){
        Serial.write("Turning off Roomba\n");
        sendRoombaCommand((unsigned int *)power);
      }
      // If we first received a "turn" but the second word was neither on nor off, we return an error.
      else {
        Serial.write(commandBuffer);
        Serial.write(" is an unknown command\n");
      }
    }
    // If the first word of the command was not "turn" we check if it was clean instead.
    else if (strcmp(commandBuffer, "clean") == 0){
      clearCommandBuffer(commandBuffer);
      Serial.write("Roomba is starting to clean\n");
        sendRoombaCommand((unsigned int *)clean);
    } 
    /* 
       If the first word of the command was neither "turn" nor "clean", we check if it was our special
       not-quite-english command "gohome".
    */
    else if (strcmp(commandBuffer, "gohome") == 0){
      clearCommandBuffer(commandBuffer);
      Serial.write("Roomba has been told to dock\n");
        sendRoombaCommand((unsigned int *)dock);
    }
    // If the first word of the command is not "turn", "clean" or "gohome" we have received and unknown command.
    else {
      Serial.write(commandBuffer);
      Serial.write(" is an unknown command\n");
    }  
  }
}
