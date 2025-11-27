#include "Parada.hpp"
#include <cmath>

// Construtor padrão
Parada::Parada() {
    this->coord_x = 0.0;
    this->coord_y = 0.0;
    this->tipo = EMBARQUE;
    this->id_demanda = -1;
}

// Construtor parametrizado
Parada::Parada(double x, double y, TipoParada tipo, int id_demanda) {
    this->coord_x = x;
    this->coord_y = y;
    this->tipo = tipo;
    this->id_demanda = id_demanda;
}

// Destrutor
Parada::~Parada() {
    // Nada para liberar
}

// Getters
double Parada::getCoordX() const {
    return this->coord_x;
}

double Parada::getCoordY() const {
    return this->coord_y;
}

TipoParada Parada::getTipo() const {
    return this->tipo;
}

int Parada::getIdDemanda() const {
    return this->id_demanda;
}

// Setters
void Parada::setCoordX(double x) {
    this->coord_x = x;
}

void Parada::setCoordY(double y) {
    this->coord_y = y;
}

void Parada::setTipo(TipoParada tipo) {
    this->tipo = tipo;
}

void Parada::setIdDemanda(int id) {
    this->id_demanda = id;
}

// Métodos auxiliares
double Parada::calcularDistancia(const Parada& outra) const {
    double dx = this->coord_x - outra.coord_x;
    double dy = this->coord_y - outra.coord_y;
    return sqrt(dx * dx + dy * dy);
}