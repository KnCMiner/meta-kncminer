#include <sys/time.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>

#define RUN_FILE "/var/run/led-blink.run"

void toggle_blue_led(void)
{
   system("asic 0 0 led 0 0 15 >/dev/null");
   sleep(1);
   system("asic 0 0 led 0 0 0 >/dev/null");
   sleep(1);
}
void handle_SigKill(int sig)
{
   system("asic 0 0 led 0 0 0 >/dev/null");
   unlink(RUN_FILE);
   exit(0);
}

void time_left(int time)
{
   FILE *f = NULL;

   f=fopen(RUN_FILE, "w");
   if(f == NULL)
     exit(-1);
   fprintf(f, "%d\n", time);
   fclose(f);   
}

int main(int argc, char **argv)
{
   time_t now, then, runtime;
   int i=-1;

   if(!access(RUN_FILE, F_OK))
      exit(-1);

   if(argc > 1) {
      sscanf(argv[1], "%d", &i);
      runtime=i;
   } else {
      runtime=600; // seconds
   }

   if(runtime < 2) runtime=2; // At least 2 seconds
   if(runtime > 1800) runtime=1800; // Maximum 30 min
   
   signal(SIGKILL, handle_SigKill);
   signal(SIGQUIT, handle_SigKill);
   signal(SIGTERM, handle_SigKill);
   signal(SIGINT, handle_SigKill);

   time(&now);
   then = now + runtime;
   time_left(runtime);

   daemon(0,0);

   while(now <= then) {
      toggle_blue_led();
      time(&now);
      time_left(then - now);
   }
   unlink(RUN_FILE);
}
