#include "core.h"
#include <stdio.h>

double add(double a, double b) { return a + b; }

double sub(double a, double b) { return a - b; }

void print_str(const char *s) {
  if (s == NULL)
    printf("null\n");
  else
    printf("%s\n", s);
}

void print_num(double d) {
  if (d == (long)d)
    printf("%ld\n", (long)d);
  else
    printf("%g\n", d);
}

void read_str(char *buffer, int size) {
  if (fgets(buffer, size, stdin) != NULL) {
    size_t len = 0;
    while (buffer[len] != '\0')
      len++;
    if (len > 0 && buffer[len - 1] == '\n')
      buffer[len - 1] = '\0';
  }
}

void core_log(const char *msg) { fprintf(stderr, "[CORE] %s\n", msg); }
