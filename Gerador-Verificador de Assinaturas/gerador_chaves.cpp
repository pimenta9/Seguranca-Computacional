#include <iostream>
#include <cstdint>
#include <vector>
#include <random>
#include <bitset>
#include <gmp.h>

void gerar_chaves() {
    mpz_t p, q;
    gmp_randstate_t state;

    mpz_inits(p, q, NULL);

    gmp_randinit_mt(state);
    gmp_randseed_ui(state, time(NULL));

    mpz_rrandomb(p, state, 1024);
    mpz_rrandomb(q, state, 1024);

    gmp_printf("p = %Zd\n", p);
    gmp_printf("q = %Zd\n", q);
}

int main() {
    gerar_chaves();
    return 0;
}
