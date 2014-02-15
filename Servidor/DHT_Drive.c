/ *
 * Dht22.c:
 * Programa simples teste para testar as funções wiringPi
 * Com base na dht11.c existente
 * Alterado por technion@lolware.net
 * /

# Include <wiringPi.h>

# Include
# Include <stdlib.h>
# Include <stdint.h>
# Include <sys/types.h>
# Include <unistd.h>

# Include "locking.h"

# Define MAXTIMINGS 85
static int DHTPIN = 7;
int dht22_dat estática [5] = {0,0,0,0,0};

sizecvt uint8_t estática (const int lido)
{
  / * DigitalRead () e amigos da wiringpi são definidos como retornar um valor
  <256. No entanto, eles são retornados como int (tipos). Esta é uma função de segurança * /

  if (leia> 255 | | ler <0)
  {
    printf ("dados inválidos de wiringPi biblioteca \ n");
    exit (EXIT_FAILURE);
  }
  voltar (uint8_t) ler;
}

static int read_dht22_dat ()
{
  uint8_t laststate = ALTA;
  uint8_t contador = 0;
  uint8_t j = 0, i;

  dht22_dat [0] = dht22_dat [1] = dht22_dat [2] = dht22_dat [3] = dht22_dat [4] = 0;

  / / Puxar o pino para baixo por 18 milissegundos
  pinMode (DHTPIN, OUTPUT);
  digitalWrite (DHTPIN, HIGH);
  atraso (10);
  digitalWrite (DHTPIN, LOW);
  atraso (18);
  / / Em seguida, puxe-a para 40 microssegundos
  digitalWrite (DHTPIN, HIGH);
  delayMicroseconds (40); 
  / / Se prepare para ler o pino
  pinMode (DHTPIN, INPUT);

  / / Detectar a mudança e ler dados
  for (i = 0; i <MAXTIMINGS; i + +) {
    contador = 0;
    while (sizecvt (digitalRead (DHTPIN)) == laststate) {
      contador + +;
      delayMicroseconds (1);
      if (contador == 255) {
        break;
      }
    }
    laststate = sizecvt (digitalRead (DHTPIN));

    if (contador == 255) break;

    / / Ignore 3 primeiras transições
    if ((i> = 4) && (i% 2 == 0)) {
      / / Enfiar cada bit nos bytes de armazenamento
      dht22_dat [j / 8] << = 1;
      if (contador> 16)
        dht22_dat [j / 8] | = 1;
      j + +;
    }
  }

  / / Verifica se lê 40 bits (8 bits x 5) + verificar a soma de verificação no último byte
  / / Imprimi-lo se os dados é bom
  if ((j> = 40) && 
      (Dht22_dat [4] == ((dht22_dat [0] + dht22_dat [1] + dht22_dat [2] + dht22_dat [3]) & 0xFF))) {
        flutuador t, h;
        h = (float) dht22_dat [0] * 256 + (float) dht22_dat [1];
        h / = 10;
        t = (float) (dht22_dat [2] & 0x7F) * 256 + (float) dht22_dat [3];
        t / = 10.0;
        if ((dht22_dat [2] & 0x80) = 0!) t * = -1;


    printf ("Umidade =% .2 f%% Temperatura =% .2 f * C \ n", h, t);
    retornar 1;
  }
  outro
  {
    printf ("Os dados não é bom, pular \ n");
    return 0;
  }
}

int main (int argc, char * argv [])
{
  int lockfd;

  if (argc! = 2)
    printf ("Uso:% s <PIN> \ nDescrição: pino é o número de pinos wiringPi \ nusing 7 (GPIO 4) \ n", argv [0]);
  outro
    DHTPIN = atoi (argv [1]);
   

  printf ("leitor Raspberry Pi wiringPi DHT22 \ nwww.lolware.net \ n");

  lockfd = open_lockfile (lockfile);

  if (wiringPiSetup () == -1)
    exit (EXIT_FAILURE);
    
  if (setuid (getuid ()) <0)
  {
    perror ("privilégios Dropping falhou \ n");
    exit (EXIT_FAILURE);
  }

  while (read_dht22_dat () == 0) 
  {
     delay (1000); 1seg / / espera para refrescar
  }

  delay (1500);
  close_lockfile (lockfd);

  return 0;
}