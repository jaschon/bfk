#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEMLEN  30000
#define STACKLEN 20

typedef struct {
  int last;
  int stack[STACKLEN];
} Stack;

typedef struct {
  char * pgm;
  int pgmlen;
  int pos;
  int ptr;
  int mem[MEMLEN];
  Stack stack;
} BFK;

char convert(int num){
  if (num > -1){
    return (char)(num % 65536);
  } else {
    return (char)(num + 65536);
  }
}

void stack_init(Stack * stack) {
  stack->last = -1;
  for(int i = 0; i < STACKLEN; i++){
    stack->stack[i] = -1;
  }
}
void stack_pop(Stack *stack){
  if(stack->last > 0) {
    stack->last--;
  } else {
    stack->last = -1;
  }
}

void stack_push(Stack * stack, int val) {
  if(stack->last+1 < STACKLEN) {
    stack->last++;
    stack->stack[stack->last] = val;
  }
}

void bfk_mem_init(BFK *bfk) {
  for(int i = 0; i < MEMLEN; i++){
    bfk->mem[i] = 0;
  }
}

void bfk_set_pgm(BFK *bfk, char pgm[], int pgmlen) {
  bfk->pgm = malloc(sizeof(char) * pgmlen);
  strcpy(bfk->pgm, pgm);
  bfk->pgmlen = pgmlen;
}

void bfk_init(BFK *bfk, char pgm[], int pgmlen) {
  bfk->pos = 0;
  bfk->ptr = 0;
  stack_init(&bfk->stack);
  bfk_mem_init(bfk);
  bfk_set_pgm(bfk, pgm, pgmlen);
}

void plus(BFK *bfk){
  if (bfk->mem[bfk->ptr] == 127){
    bfk->mem[bfk->ptr] = -128;
  } else {
    bfk->mem[bfk->ptr]++;
  }
}

void minus(BFK *bfk){
  if (bfk->mem[bfk->ptr] == -128){
    bfk->mem[bfk->ptr] = 127;
  } else {
    bfk->mem[bfk->ptr]--;
  }
}

void mem_r(BFK *bfk) {
  bfk->ptr = (bfk->ptr+1) % MEMLEN;
}

void mem_l(BFK *bfk) {
  bfk->ptr = (bfk->ptr-1) % MEMLEN;
}

void loop_l(BFK *bfk) {
  if (bfk->mem[bfk->ptr] != 0) {
    stack_push(&bfk->stack, bfk->pos);
  } else {
    Stack stack;
    stack_init(&stack);
    while(bfk->pos < bfk->pgmlen){
      if (bfk->pgm[bfk->pos] == '['){
        stack_push(&stack, bfk->pos);
      } else if (bfk->pgm[bfk->pos] == ']') {
        stack_pop(&stack);
        if (stack.last == -1) {
          break;
        }
      }
      bfk->pos++;
    }
  }
}

void loop_r(BFK *bfk) {
  if (bfk->mem[bfk->ptr] != 0){
    bfk->pos = bfk->stack.stack[bfk->stack.last];
  } else {
    stack_pop(&bfk->stack);
  }
}

void output(BFK *bfk) {
  printf("%c",convert(bfk->mem[bfk->ptr]));
}

void input(BFK *bfk){
  int input;
  scanf("%i", &input);
  bfk->mem[bfk->ptr] = input % 127;
}

void debug(BFK *bfk) {
  printf("\nPROGRAM: %i MEM LOC: %i MEM VAL: %i MEM CHAR: '%c'\n", bfk->pos, bfk->ptr, bfk->mem[bfk->ptr], convert(bfk->mem[bfk->ptr]));
}

void loop(BFK * bfk){
  while (bfk->pos < bfk->pgmlen) {
    if(bfk->pgm[bfk->pos] == '+'){
      plus(bfk);
    } else if (bfk->pgm[bfk->pos] == '-') {
      minus(bfk);
    } else if (bfk->pgm[bfk->pos] == '>') {
      mem_r(bfk);
    } else if (bfk->pgm[bfk->pos] == '<') {
      mem_l(bfk);
    } else if (bfk->pgm[bfk->pos] == '[') {
      loop_l(bfk);
    } else if (bfk->pgm[bfk->pos] == ']') {
      loop_r(bfk);
    } else if (bfk->pgm[bfk->pos] == '.') {
      output(bfk);
    } else if (bfk->pgm[bfk->pos] == ',') {
      input(bfk);
    } else if (bfk->pgm[bfk->pos] == '#') {
      debug(bfk);
    }
    bfk->pos++;
  }
}

int main(int argc, char *argv[])
{
  if (argc == 2) {
    char *pgm = argv[1];
    BFK bfk;
    bfk_init(&bfk, pgm, strlen(pgm));
    loop(&bfk);
  }

  return 0;
}
