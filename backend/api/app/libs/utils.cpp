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
pair<vector<double>, double> compara_testemunha(const vector<int>& testemunha, const vector<int>& previsao) {
    vector<double> erros_quadraticos;

    for (size_t i = 0; i < testemunha.size(); ++i) {
        double erro = pow(testemunha[i] - previsao[i], 2);
        erros_quadraticos.push_back(erro);
    }

    double erro_quadratico_medio = accumulate(erros_quadraticos.begin(), erros_quadraticos.end(), 0.0) / erros_quadraticos.size();

    return make_pair(erros_quadraticos, erro_quadratico_medio);
}

// Função para binarizar uma lista
vector<int> binariza(const vector<int>& lista, int n_ante, int n_poste) {
    vector<int> ante(lista);
    vector<int> poste(lista);

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
                subir = static_cast<double>(acres) / (acres + decre);
            } else {
                subir = 0.001;
            }
        }
    }

    return vector<double>{subir};
}


// Função para calcular a taxa de acréscimo
pair<double, double> tax_acrescimo(const vector<int>& lista) {
    vector<int> coluna(lista.begin(), lista.end() - 1);
    vector<int> poste(lista.begin() + 1, lista.end());

    vector<int> acrescimo;
    vector<int> decrescimo;

    for (size_t i = 0; i < coluna.size(); ++i) {
        int diff = poste[i] - coluna[i];
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


extern "C" {
    // Função para dividir uma lista em duas sub-listas
    void split_list(const int* lista, int tamanho_lista, int segundo_membro, int* base, int* testemunha) {
        if (segundo_membro < 0 || segundo_membro > tamanho_lista) {
            throw std::invalid_argument("O parâmetro 'segundo_membro' deve ser um inteiro não negativo menor ou igual ao tamanho da lista.");
        }

        std::memcpy(base, lista, (tamanho_lista - segundo_membro) * sizeof(int));
        std::memcpy(testemunha, lista + (tamanho_lista - segundo_membro), segundo_membro * sizeof(int));
    }

    // Função para comparar os valores reais com as previsões
    double compara_testemunha(const int* testemunha, const int* previsao, int tamanho) {
        double erros_quadraticos[tamanho];
        double erro_quadratico_medio = 0.0;

        for (int i = 0; i < tamanho; ++i) {
            erros_quadraticos[i] = std::pow(testemunha[i] - previsao[i], 2);
        }

        for (int i = 0; i < tamanho; ++i) {
            erro_quadratico_medio += erros_quadraticos[i];
        }

        return erro_quadratico_medio / tamanho;
    }

    // Função para binarizar uma lista
    void binariza(const int* lista, int tamanho_lista, int n_ante, int n_poste, int* binarios) {
        int ante[tamanho_lista];
        int poste[tamanho_lista];

        std::memcpy(ante, lista, tamanho_lista * sizeof(int));
        std::memcpy(poste, lista, tamanho_lista * sizeof(int));

        if (n_ante > 0) {
            for (int i = tamanho_lista - n_ante; i < tamanho_lista; ++i) {
                ante[i] = ante[tamanho_lista - n_ante];
            }
        }

        if (n_poste > 0) {
            for (int i = 0; i < n_poste; ++i) {
                poste[i] = poste[n_poste];
            }
        }

        for (int i = 0; i < tamanho_lista; ++i) {
            binarios[i] = (poste[i] - ante[i] > 0) ? 1 : 0;
        }
    }

    // Função para inferência Bayesiana binária geral
    double inferencia_bayes_bin_general(const int* binarios, int tamanho_binarios, int n) {
        if (n < 2) {
            throw std::invalid_argument("O valor de 'n' deve ser maior ou igual a 2.");
        }

        int pref[tamanho_binarios - (n - 1)];
        int final[n];
        std::memcpy(pref, binarios, (tamanho_binarios - (n - 1)) * sizeof(int));
        std::memcpy(final, binarios + (tamanho_binarios - n), n * sizeof(int));

        double subir = 0.5;

        // Calcula a probabilidade de subir (a implementação real depende do seu modelo específico)

        return subir;
    }

    // Função para calcular a taxa de acréscimo
    void tax_acrescimo(const int* lista, int tamanho_lista, double* media_acrescimo, double* media_decrescimo) {
        int coluna[tamanho_lista - 1];
        int poste[tamanho_lista - 1];

        std::memcpy(coluna, lista, (tamanho_lista - 1) * sizeof(int));
        std::memcpy(poste, lista + 1, (tamanho_lista - 1) * sizeof(int));

        int acrescimo[tamanho_lista - 1];
        int decrescimo[tamanho_lista - 1];
        int cont_acrescimo = 0;
        int cont_decrescimo = 0;

        for (int i = 0; i < tamanho_lista - 1; ++i) {
            int diff = poste[i] - coluna[i];
            if (diff > 0) {
                acrescimo[cont_acrescimo++] = diff;
            } else {
                decrescimo[cont_decrescimo++] = diff;
            }
        }

        *media_acrescimo = 0.0;
        *media_decrescimo = 0.0;

        if (cont_acrescimo > 0) {
            for (int i = 0; i < cont_acrescimo; ++i) {
                *media_acrescimo += acrescimo[i];
            }
            *media_acrescimo /= cont_acrescimo;
        }

        if (cont_decrescimo > 0) {
            for (int i = 0; i < cont_decrescimo; ++i) {
                *media_decrescimo += decrescimo[i];
            }
            *media_decrescimo /= cont_decrescimo;
        }
    }
}

       
