#ifndef SEKC_CORE_H
#define SEKC_CORE_H

#ifdef __cplusplus
extern "C" {
#endif

double add(double a, double b);
double sub(double a, double b);

void print_str(const char *s);
void print_num(double d);
void read_str(char *buffer, int size);

void core_log(const char *msg);

#ifdef __cplusplus
}
#endif

#endif
