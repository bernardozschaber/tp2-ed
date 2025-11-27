#include "Demanda.hpp"
#include <cmath>

// Construtor padrão
Demanda::Demanda() {
    this->id = -1;
    this->tempo_solicitacao = 0.0;
    this->origem_x = 0.0;
    this->origem_y = 0.0;
    this->destino_x = 0.0;
    this->destino_y = 0.0;
    this->estado = DEMANDADA;
    this->corrida_associada = nullptr;
    this->tempo_conclusao = 0.0;
    this->distancia_percorrida = 0.0;
}

// Construtor parametrizado
Demanda::Demanda(int id, double tempo, double ox, double oy, double dx, double dy) {
    this->id = id;
    this->tempo_solicitacao = tempo;
    this->origem_x = ox;
    this->origem_y = oy;
    this->destino_x = dx;
    this->destino_y = dy;
    this->estado = DEMANDADA;
    this->corrida_associada = nullptr;
    this->tempo_conclusao = 0.0;
    this->distancia_percorrida = 0.0;
}

// Destrutor
Demanda::~Demanda() {
    // Corrida será gerenciada externamente, não deletamos aqui
}

// Getters
int Demanda::getId() const {
    return this->id;
}

double Demanda::getTempoSolicitacao() const {
    return this->tempo_solicitacao;
}

double Demanda::getOrigemX() const {
    return this->origem_x;
}

double Demanda::getOrigemY() const {
    return this->origem_y;
}

double Demanda::getDestinoX() const {
    return this->destino_x;
}

double Demanda::getDestinoY() const {
    return this->destino_y;
}

EstadoDemanda Demanda::getEstado() const {
    return this->estado;
}

Corrida* Demanda::getCorridaAssociada() const {
    return this->corrida_associada;
}

double Demanda::getTempoConclusao() const {
    return this->tempo_conclusao;
}

double Demanda::getDistanciaPercorrida() const {
    return this->distancia_percorrida;
}

// Setters
void Demanda::setEstado(EstadoDemanda novo_estado) {
    this->estado = novo_estado;
}

void Demanda::setCorridaAssociada(Corrida* corrida) {
    this->corrida_associada = corrida;
}

void Demanda::setTempoConclusao(double tempo) {
    this->tempo_conclusao = tempo;
}

void Demanda::setDistanciaPercorrida(double distancia) {
    this->distancia_percorrida = distancia;
}

// Métodos auxiliares
double Demanda::calcularDistanciaOrigem(const Demanda& outra) const {
    double dx = this->origem_x - outra.origem_x;
    double dy = this->origem_y - outra.origem_y;
    return sqrt(dx * dx + dy * dy);
}

double Demanda::calcularDistanciaDestino(const Demanda& outra) const {
    double dx = this->destino_x - outra.destino_x;
    double dy = this->destino_y - outra.destino_y;
    return sqrt(dx * dx + dy * dy);
}

double Demanda::calcularDistanciaCorrida() const {
    double dx = this->destino_x - this->origem_x;
    double dy = this->destino_y - this->origem_y;
    return sqrt(dx * dx + dy * dy);
}