#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <unordered_set>
#include <algorithm>
#include <cmath>
using namespace std;

unordered_map< string, vector<int> > sequencias; 

vector<int> get_divisores(int numero){
    vector<int> divisores;

    for (int i = 1; i <= sqrt(numero); i++) {
        if (numero % i == 0) {
            
            if (numero / i == i) {
                divisores.push_back(i) ;
            }
            else {
                divisores.push_back(i) ;
                divisores.push_back(numero/i) ;
            }
        }
    }

    return divisores;
}

int calcula_tamanho_chave(vector< pair<string, vector<int>> > distancias){
    vector<vector<int>> divisores;

    for(int i = 0; i < distancias.size(); i++){
        for(int j = 0; j < distancias[i].second.size(); j++){
            divisores.push_back(get_divisores(distancias[i].second[j]));
        }
    }

    int frequencia[1000] = {0};

    for(int i = 0; i < divisores.size(); i++){
        for(int j = 0; j < divisores[i].size(); j++){
            int d = divisores[i][j];
            if(d > 3) {
                frequencia[d]++;
            }
        }
    }

    int maior_freq = -1, index = -1;
    for(int i = 2; i < 1000; i++){
        if(frequencia[i] > maior_freq || 
           (frequencia[i] == maior_freq && i > index)) {
            maior_freq = frequencia[i];
            index = i;
        }
    }

    return index;
}


vector< pair<string, vector<int>> > calcular_distancias(string ciphertext, int k){
    vector< pair<string, vector<int>> > distancias;

    for(auto& it : sequencias){
        int tamanho_sequencia = it.first.size();
        int quantidade_sequencia = it.second.size();
        
        if(tamanho_sequencia == k && quantidade_sequencia > 1){
            vector<int> dist;

            for(int i = 0; i < quantidade_sequencia - 1; i++){
                int occ1, occ2;
                occ1 = it.second[i];
                occ2 = it.second[i+1];

                dist.push_back(occ2 - occ1);
            }

            distancias.push_back({it.first, dist});
        }
    }

    return distancias;
}

void ocorrencias(string ciphertext, string substring){
    size_t pos = ciphertext.find(substring, 0);

    while(pos != string::npos){
        sequencias[substring].push_back(pos);

        pos = ciphertext.find(substring, pos + 1);
    }
}

int key_length(string ciphertext, int k){
    unordered_set<string> string_processada;

    for(int i = 0; i < ciphertext.size(); i++){
        string substring = ciphertext.substr(i, k);

        if(string_processada.find(substring) == string_processada.end()){
            ocorrencias(ciphertext, substring);
            string_processada.insert(substring);
        }
    }

    vector< pair<string, vector<int>> > distancias = calcular_distancias(ciphertext, k);

    int tamanho_chave = calcula_tamanho_chave(distancias); 

    return tamanho_chave;
}

int main(){
    ifstream inputFile;
    inputFile.open("criptograma");

    if(inputFile.is_open()){
        string ciphertext = "", line;
        int k;

        while(getline(inputFile, line)){
            ciphertext += line;
        }

        cout << "Tamanho do padrão: ";;
        cin >> k;

        int length = key_length(ciphertext, k);

        ofstream outputFile("tamanho.txt");
        if(outputFile.is_open()){
            outputFile << length;
            outputFile.close();
        } else {
            cout << "Erro ao abrir arquivo de saída!" << endl;
        }

    }else{
        cout << "Erro ao abrir arquivo de entrada!";
    }

    return 0;
}