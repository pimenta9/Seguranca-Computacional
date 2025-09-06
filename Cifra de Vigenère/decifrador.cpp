#include <iostream>
using namespace std;

string descriptografar(string criptograma, string senha)
{
    string mensagem;

    int tamanho_senha = senha.size();

    for (int i = 0, j = 0; i < criptograma.size(); i++)
    {
        if (criptograma[i] < 'A' or criptograma[i] > 'Z')
        {
            mensagem.push_back(criptograma[i]);
            continue;
        }

        char letra = 'A' + ((criptograma[i] - 'A') + 26 - (senha[j % tamanho_senha] - 'A'))%26;

        mensagem.push_back(letra);

        j++;
    }

    return mensagem;
}

int main ()
{
    string criptograma;
    cout << "Escreva o criptograma: ";
    getline(cin, criptograma);

    string senha;
    cout << "Escreva a senha: ";
    cin >> senha;

    string mensagem = descriptografar(criptograma, senha);

    cout << "A mensagem é: " << mensagem << '\n';

    return 0;
}
