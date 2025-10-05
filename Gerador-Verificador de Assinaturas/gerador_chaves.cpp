#include <iostream>
#include <gmp.h>

bool miller_rabin(mpz_t n, int k, gmp_randstate_t state){
    if (mpz_cmp_ui(n, 2) < 0) return false;
    if (mpz_cmp_ui(n, 2) == 0) return true;
    if (mpz_even_p(n)) return false;        // n par, ou seja, não primo

    mpz_t d, sub, a, x;
    mpz_inits(d, sub, a, x, NULL);

    // sub = n - 1
    mpz_sub_ui(sub, n, 1);

    // d = n - 1 e fatorar potências de 2: n−1 = 2^s * d
    mpz_set(d, sub);
    long long s = 0;
    while (mpz_even_p(d)) {
        mpz_fdiv_q_2exp(d, d, 1);
        s++;
    }

    for (int i = 0; i < k; i++) {
        // Escolhe 2 <= a <= n-2
        mpz_urandomm(a, state, sub);      // 0 <= a < n-1
        mpz_add_ui(a, a, 2);              // 2 <= a <= n-2

        // x = a^d mod n
        mpz_powm(x, a, d, n); 

        //Se x == 1 ou x == n-1, continua
        if (mpz_cmp_ui(x, 1) == 0 || mpz_cmp(x, sub) == 0) continue;

        /*
        repitir até s-1 vezes:
        x = x^2 mod n
        Se x == n-1, encerra o loop 
        Se x == 1, então n é composto
        */
        bool flag = false;
        for (unsigned long r = 1; r < s; r++) {
            
            // x = x^2 mod n
            mpz_powm_ui(x, x, 2, n); 

            if (mpz_cmp(x, sub) == 0) {
                flag = true;
                break;
            }
            if (mpz_cmp_ui(x, 1) == 0) {
                mpz_clears(sub, d, a, x, NULL);
                return false;       // composto
            }
        }

        if (flag) continue;
        mpz_clears(sub, d, a, x, NULL);
        return false;       // composto
    }

    mpz_clears(sub, d, a, x, NULL);
    return true;        // provavelmente primo
}

void gerar_chaves() {
    mpz_t p, q;
    gmp_randstate_t state;

    mpz_inits(p, q, NULL);

    gmp_randinit_mt(state);
    gmp_randseed_ui(state, time(NULL));

    do{
        mpz_rrandomb(p, state, 1024);
    }while(!miller_rabin(p, 20, state));
    
    do{
        mpz_rrandomb(q, state, 1024);
    }while(!miller_rabin(q, 20, state));

    gmp_printf("p = %Zd\n", p);
    gmp_printf("q = %Zd\n", q);

    mpz_clears(p, q, NULL);
    gmp_randclear(state);
}

int main() {
    gerar_chaves();
    return 0;
}
