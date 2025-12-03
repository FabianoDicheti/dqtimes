#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <stdexcept>
#include <cmath>
#include <cstring> // Para usar o memcpy

using namespace std;


// Função para dividir uma lista em duas sub-listas
pair<vector<float>, vector<float>> split_list(const vector<float>& lista, int segundo_membro) {
    if (segundo_membro < 0 || segundo_membro > static_cast<int>(lista.size())) {
        throw invalid_argument("O parâmetro 'segundo_membro' deve ser um inteiro não negativo menor ou igual ao tamanho da lista.");
    }

    vector<float> base(lista.begin(), lista.end() - segundo_membro);
    vector<float> testemunha(lista.end() - segundo_membro, lista.end());

    return make_pair(base, testemunha);
}



// Função para comparar os valores reais com as previsões
pair<vector<double>, double> compara_testemunha(const vector<float>& testemunha, const vector<float>& previsao) {
    vector<double> erros_quadraticos;

    for (size_t i = 0; i < testemunha.size(); ++i) {
        double erro = pow(testemunha[i] - previsao[i], 2);
        erros_quadraticos.push_back(erro);
    }

    double erro_quadratico_medio = accumulate(erros_quadraticos.begin(), erros_quadraticos.end(), 0.0) / erros_quadraticos.size();

    return make_pair(erros_quadraticos, erro_quadratico_medio);
}

// Função para binarizar uma lista
vector<int> binariza(const vector<float>& lista, int n_ante, int n_poste) {
    vector<float> ante(lista);
    vector<float> poste(lista);

    if (n_ante > 0) {
        ante.insert(ante.end(), n_ante - 1, ante.back());
        ante.erase(ante.end() - n_ante, ante.end());
    }

    if (n_poste > 0) {
        poste.insert(poste.begin(), n_poste - 1, poste.front());
        poste.erase(poste.begin(), poste.begin() + n_poste);
    }

    vector<int> binarios;
    for (size_t i = 0; i < ante.size(); ++i) {
        binarios.push_back(poste[i] - ante[i] > 0 ? 1 : 0);
    }

    return binarios;
}

// Função para inferência Bayesiana binária geral
vector<double> inferencia_bayes_bin_general(const vector<int>& binarios, int n) {
    if (n < 2) {
        throw invalid_argument("O valor de 'n' deve ser maior ou igual a 2.");
    }

    vector<int> pref(binarios.begin(), binarios.end() - (n - 1));
    vector<int> final(binarios.end() - (n - 1), binarios.end());
    vector<vector<int>> subsequencias;

    for (size_t i = 0; i <= binarios.size() - n; ++i) {
        vector<int> sub(binarios.begin() + i, binarios.begin() + i + n);
        subsequencias.push_back(sub);
    }

    double subir = 0.5;
    for (int i = 0; i < pow(2, n - 1); ++i) {
        vector<int> valor_final;
        for (int j = n - 2; j >= 0; --j) {
            valor_final.push_back((i >> j) & 1);
        }

        if (valor_final == final) {
            int acres = count(subsequencias.begin(), subsequencias.end(), valor_final);
            int decre = count(subsequencias.begin(), subsequencias.end(), valor_final);
            if (acres > 0) {
                subir = static_cast<double>(acres) / (acres +
                decre);
            } else {
                subir = 0.001;
            }
        }
    }

    return vector<double>{subir};
}

// Função para calcular a taxa de acréscimo
pair<double, double> tax_acrescimo(const vector<float>& lista) {
    vector<float> coluna(lista.begin(), lista.end() - 1);
    vector<float> poste(lista.begin() + 1, lista.end());

    vector<float> acrescimo;
    vector<float> decrescimo;

    for (size_t i = 0; i < coluna.size(); ++i) {
        float diff = poste[i] - coluna[i];
        if (diff > 0) {
            acrescimo.push_back(diff);
        } else {
            decrescimo.push_back(diff);
        }
    }

    double media_acrescimo = 0;
    double media_decrescimo = 0;

    if (!acrescimo.empty()) {
        media_acrescimo = accumulate(acrescimo.begin(), acrescimo.end(), 0.0) / acrescimo.size();
    }

    if (!decrescimo.empty()) {
        media_decrescimo = accumulate(decrescimo.begin(), decrescimo.end(), 0.0) / decrescimo.size();
    }

    return make_pair(media_acrescimo, media_decrescimo);
}
