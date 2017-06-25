#include<stdio.h>

int main(){
  int n = 2;
  int* p = &n;
  printf("%p\n", &p);
  printf("%p\n", &n);
}
