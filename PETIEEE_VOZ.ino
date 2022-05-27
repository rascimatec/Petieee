#include <SoftwareSerial.h>
#include "VoiceRecognitionV3.h"

/**
  Connection
  Arduino    VoiceRecognitionModule
   2   ------->     TX
   3   ------->     RX
*/
VR myVR(10, 11);   // 2:RX 3:TX, you can choose your favourite pins.

uint8_t records[7]; // save record
uint8_t buf[64];

int led = 11; /*pino 11 do arduino */
/*depois eu troco o nome das variaveis para portugues mas por agora melhor não quebrar o codigo */
#define HorarioRemedio    (0) /*numero do comando a configurar 0 do teste de voz (led vai acender) */
#define HorarioBanho   (1) /*numero do comando a configurar 1 do teste de voz (led vai desligar) */

/**
  @brief   Print signature, if the character is invisible,
           print hexible value instead.
  @param   buf     --> command length
           len     --> number of parameters
*/
void printSignature(uint8_t *buf, int len)
{
  int i;
  for (i = 0; i < len; i++) {
    if (buf[i] > 0x19 && buf[i] < 0x7F) {
      Serial.write(buf[i]);
    }
    else {
      Serial.print("[");
      Serial.print(buf[i], HEX);
      Serial.print("]");
    }
  }
}

/**
  @brief   Print signature, if the character is invisible,
           print hexible value instead.
  @param   buf  -->  VR module return value when voice is recognized.
             buf[0]  -->  Group mode(FF: None Group, 0x8n: User, 0x0n:System
             buf[1]  -->  number of record which is recognized.
             buf[2]  -->  Recognizer index(position) value of the recognized record.
             buf[3]  -->  Signature length
             buf[4]~buf[n] --> Signature
*/
void printVR(uint8_t *buf)
{
  Serial.println("VR Index\tGroup\tRecordNum\tSignature");

  Serial.print(buf[2], DEC);
  Serial.print("\t\t");

  if (buf[0] == 0xFF) {
    Serial.print("NONE");
  }
  else if (buf[0] & 0x80) {
    Serial.print("UG ");
    Serial.print(buf[0] & (~0x80), DEC);
  }
  else {
    Serial.print("SG ");
    Serial.print(buf[0], DEC);
  }
  Serial.print("\t");

  Serial.print(buf[1], DEC);
  Serial.print("\t\t");
  if (buf[3] > 0) {
    printSignature(buf + 4, buf[3]);
  }
  else {
    Serial.print("NONE");
  }
  Serial.println("\r\n");
}

void setup()
{
  /** initialize */
  myVR.begin(9600); /*taxa de bits por segundo do arduino (preciso ver a velocidade do eps32) */

  Serial.begin(115200); /*taxa de bits por segundo do pcz */
  Serial.println("modulo de reconhecimento de voz V3");

  pinMode(led, OUTPUT);

  if (myVR.clear() == 0) {
    Serial.println("reconheceu o modulo de reconhecimento de voz V3.");
  } else {
    Serial.println("não foi encontrado o modulo de reconhecimento de voz.");
    Serial.println("Por favor cheque a conexão e reinicie o arduino.");
    while (1);
  }

  if (myVR.load((uint8_t)HorarioRemedio) >= 0) {
    Serial.println("Horario de Remedio foi carregado");
  }

  if (myVR.load((uint8_t)HorarioBanho) >= 0) {
    Serial.println("Horario de Banho foi Carregado");
  }
}

void loop()
{
  int ret;
  ret = myVR.recognize(buf, 50); /*bota a variavel para reconhecer em x tempo vozez no loop*/
  if (ret > 0) {
    switch (buf[1]) {
      case HorarioRemedio:
        /* acende o led */
        //digitalWrite(led, HIGH);
        Serial.println("o seu velho esta morrendo");
        break;
      case HorarioBanho:
        /* desliga o led */
        //digitalWrite(led, LOW);
        break;
      default:
        Serial.println("Record function undefined");
        break;
    }
    /* a voz foi reconhecida */
    printVR(buf);
  }
}
