#ifndef SEKC_CORE_H
#define SEKC_CORE_H

#ifdef __cplusplus
extern "C" {
#endif

double sekc_add(double a, double b);
double sekc_sub(double a, double b);

void sekc_print_str(const char *s);
void sekc_print_num(double d);
void sekc_read_str(char *buffer, int size);

void sekc_log(const char *msg);

#ifdef __cplusplus
}
#endif

#endif
