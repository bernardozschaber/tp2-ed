#include "Trecho.hpp"
#include <cmath>

// Construtor padrão
Trecho::Trecho() {
    this->parada_inicio = nullptr;
    this->parada_fim = nullptr;
    this->tempo = 0.0;
    this->distancia = 0.0;
    this->natureza = DESLOCAMENTO;
}

// Construtor parametrizado
Trecho::Trecho(Parada* inicio, Parada* fim, double tempo, double distancia, NaturezaTrecho natureza) {
    this->parada_inicio = inicio;
    this->parada_fim = fim;
    this->tempo = tempo;
    this->distancia = distancia;
    this->natureza = natureza;
}

// Destrutor
Trecho::~Trecho() {
    // Paradas serão gerenciadas externamente, não deletamos aqui
}

// Getters
Parada* Trecho::getParadaInicio() const {
    return this->parada_inicio;
}

Parada* Trecho::getParadaFim() const {
    return this->parada_fim;
}

double Trecho::getTempo() const {
    return this->tempo;
}

double Trecho::getDistancia() const {
    return this->distancia;
}

NaturezaTrecho Trecho::getNatureza() const {
    return this->natureza;
}

// Setters
void Trecho::setParadaInicio(Parada* inicio) {
    this->parada_inicio = inicio;
}

void Trecho::setParadaFim(Parada* fim) {
    this->parada_fim = fim;
}

void Trecho::setTempo(double tempo) {
    this->tempo = tempo;
}

void Trecho::setDistancia(double distancia) {
    this->distancia = distancia;
}

void Trecho::setNatureza(NaturezaTrecho natureza) {
    this->natureza = natureza;
}

// Métodos auxiliares
void Trecho::calcularTempoDistancia(double velocidade) {
    if (this->parada_inicio != nullptr && this->parada_fim != nullptr) {
        this->distancia = this->parada_inicio->calcularDistancia(*this->parada_fim);
        this->tempo = this->distancia / velocidade;
    }
}