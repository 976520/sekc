#include "core.h"
#include <stdio.h>

double sekc_add(double a, double b) { return a + b; }

double sekc_sub(double a, double b) { return a - b; }

void sekc_print_str(const char *s) {
  if (s == NULL)
    printf("null\n");
  else
    printf("%s\n", s);
}

void sekc_print_num(double d) {
  if (d == (long)d)
    printf("%ld\n", (long)d);
  else
    printf("%g\n", d);
}

void sekc_read_str(char *buffer, int size) {
  if (fgets(buffer, size, stdin) != NULL) {
    size_t len = 0;
    while (buffer[len] != '\0')
      len++;
    if (len > 0 && buffer[len - 1] == '\n')
      buffer[len - 1] = '\0';
  }
}

void sekc_log(const char *msg) { fprintf(stderr, "[CORE] %s\n", msg); }
