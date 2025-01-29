// =====================================================================================================================
// Name: Tinkerkit_Braccio_Robot_V2
// Description: This program allows control of a Braccio robotic arm through serial communication.
// Target: Arduino Uno
// Compiler: Arduino IDE
// Usage: Control the Braccio robot using Python
// Restriction(s): None.
// History: 7/05/2024 | E. Zoukou / C. Courtemanche / K. Niamba / Creation;
//          1/28/2025 | K. Niamba / Modification ---> Documentation translation (FR to ENG);
// =====================================================================================================================

// =====================================================================================================================
// Including files
// =====================================================================================================================
#include <Braccio.h>
#include <Servo.h>

// ---------------------------------------------------
// Calling the parts of the arm (servo motors)
// ---------------------------------------------------
Servo base;                                                // Base servo
Servo shoulder;                                            // Shoulder servo
Servo elbow;                                               // Elbow servo
Servo wrist_rot;                                           // Wrist rotation servo
Servo wrist_ver;                                           // Wrist flexion servo
Servo gripper;                                             // Gripper servo

// =====================================================================================================================
// Main Program #2
// =====================================================================================================================
void setup() {
  Braccio.begin();                                         // Initialize the Braccio arm
  Serial.begin(9600);                                      // Initialize serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {                            // Check if data is available on the serial port
    String reception = Serial.readStringUntil('\n');       // Read the string until the end of the line
    int values[7];                                         // Array to store the received values (size increased for M6)
    parseValues(reception, values);                        // Call the function to extract the values

    // ---------------------------------------------------
    // Extract values from the array
    // ---------------------------------------------------
    int V = values[0];                                     // Speed
    int M1 = values[1];                                    // Base angle
    int M2 = values[2];                                    // Shoulder angle
    int M3 = values[3];                                    // Elbow angle
    int M4 = values[4];                                    // Wrist rotation angle
    int M5 = values[5];                                    // Wrist flexion angle
    int M6 = values[6];                                    // Gripper angle (M6 added)

    // ---------------------------------------------------
    // Display the received values in the Serial Monitor
    // ---------------------------------------------------
    Serial.print("Received values: ");
    Serial.print("V="); Serial.print(V);
    Serial.print(", M1="); Serial.print(M1);
    Serial.print(", M2="); Serial.print(M2);
    Serial.print(", M3="); Serial.print(M3);
    Serial.print(", M4="); Serial.print(M4);
    Serial.print(", M5="); Serial.print(M5);
    Serial.print(", M6="); Serial.println(M6);

    Braccio.ServoMovement(V, M1, M2, M3, M4, M5, M6);      // Arm movement based on the values received from PyCharm
    delay(1000);

    Braccio.ServoMovement(V, M1, M2, M3, M4, M5, 73);      // Open the gripper
    delay(1000);

    Braccio.ServoMovement(V, 120, 90, 150, 180, 90, 73);   // Arm movement
    delay(1000);

    Braccio.ServoMovement(V, 120, 90, 150, 180, 90, 0);    // Close the gripper
    delay(1000);

    Serial.println("Received and executed: " + reception); // Message indicating the data has been received and processed
  }
}

// ---------------------------------------------------
// Function to extract and separate the values << String >> from PyCharm for the Arduino IDE
// ---------------------------------------------------
void parseValues(String data, int* values) {
  int index = 0;
  while (data.length() > 0) {
    int separatorIndex = data.indexOf(':');                // Look for the index of the separator ':'
    if (separatorIndex != -1) {
      String valueStr = data.substring(0, separatorIndex); // Extract the substring before the separator
      values[index++] = valueStr.toInt();                  // Convert the substring to an integer and add it to the values array
      data = data.substring(separatorIndex + 1);           // Update the string by removing the processed part
    } else {
      values[index++] = data.toInt();                      // Convert the string to an integer and add it to the values array
      break;                                               // Exit the loop
    }
  }
}