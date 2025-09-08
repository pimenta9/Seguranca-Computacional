#include <iostream>
#include <vector>
#include <map>
using namespace std;

vector<vector<double>> alfabeto =
{
    // inglês
    {0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.0228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.0236, 0.0015, 0.01974, 0.00074}, 
    // português
    {0.1463, 0.0104, 0.0388, 0.0499, 0.1257, 0.0102, 0.013, 0.0128, 0.0618, 0.004, 0.0002, 0.0278, 0.0474, 0.0505, 0.1073, 0.0252, 0.012, 0.0653, 0.0781, 0.0434, 0.0463, 0.0167, 0.0001, 0.0021, 0.0001, 0.0047}
};

string criptograma;

char descobrir_letra (int i, map<char, double> freq, int idioma)
{
    char letra;
    double max_sum;

    for (char j = 'A'; j <= 'Z'; j++)
    {
        double sum = 0;

        for (char k = 'A'; k <= 'Z'; k++)
        {
            sum += alfabeto[idioma][k - 'A'] * freq['A' + (((k - 'A') + (j - 'A')) % 26)];
        }

        if (j == 'A' or sum > max_sum)
        {
            max_sum = sum;
            letra = j;
        }
    }

    return letra;
}

int main ()
{
    cout << "Digite o criptograma: ";
    getline(cin, criptograma);

    int tamanho_senha;
    cout << "Digite o tamanho da senha: ";
    cin >> tamanho_senha;

    int idioma;
    cout << "Qual é o idioma?\n0 - Inglês\n1 - Português\n";
    cin >> idioma;

    vector<map<char, double>> freq(tamanho_senha);
    vector<int> numero_letras(tamanho_senha, 0);
    for (int i = 0, j = 0; i < criptograma.size(); i++)
    {
        if (criptograma[i] < 'A' or criptograma[i] > 'Z')
            continue;

        freq[j % tamanho_senha][criptograma[i]]++;
        numero_letras[j % tamanho_senha]++;
        j++;
    }

    for (int i = 0; i < tamanho_senha; i++)
    {
        for (auto &[k, v] : freq[i])
        {
            v = v/numero_letras[i];
        }
    }

    string senha;
    for (int i = 0; i < tamanho_senha; i++)
    {
        char letra = descobrir_letra(i, freq[i], idioma);

        senha.push_back(letra);
    }

    cout << senha << '\n';

    return 0;
}
