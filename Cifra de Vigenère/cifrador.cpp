#include <iostream>
#include <fstream>
using namespace std;

string criptografar(string mensagem, string senha)
{
    string criptograma;

    int tamanho_senha = senha.size();

    for (int i = 0, j = 0; i < mensagem.size(); i++)
    {
        if (mensagem[i] < 'A' or mensagem[i] > 'Z')
        {
            criptograma.push_back(mensagem[i]);
            continue;
        }

        char letra_criptografada = 'A' + ((mensagem[i] - 'A') + (senha[j % tamanho_senha] - 'A'))%26;

        criptograma.push_back(letra_criptografada);

        j++;
    }

    return criptograma;
}

int main ()
{
    string mensagem;
    cout << "Escreva a mensagem: ";
    getline(cin, mensagem);

    string senha;
    cout << "Escreva a senha: ";
    cin >> senha;

    ofstream arquivo("criptograma");
    if (!arquivo)
    {
        cout << "Erro ao abrir o arquivo.\n";
        return -1;
    }

    string criptograma = criptografar(mensagem, senha);

    cout << "O criptograma é: " << criptograma << '\n';

    arquivo << criptograma;

    return 0;
}
