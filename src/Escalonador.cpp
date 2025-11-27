#include "Escalonador.hpp"

// ==================== CLASSE EVENTO ====================

// Construtor padrão
Evento::Evento() {
    this->tempo = 0.0;
    this->tipo = COLETA_PASSAGEIRO;
    this->corrida_associada = nullptr;
    this->indice_parada = 0;
}

// Construtor parametrizado
Evento::Evento(double tempo, TipoEvento tipo, Corrida* corrida, int indice_parada) {
    this->tempo = tempo;
    this->tipo = tipo;
    this->corrida_associada = corrida;
    this->indice_parada = indice_parada;
}

// Destrutor
Evento::~Evento() {
    // Corrida será gerenciada externamente
}

// Getters
double Evento::getTempo() const {
    return this->tempo;
}

TipoEvento Evento::getTipo() const {
    return this->tipo;
}

Corrida* Evento::getCorridaAssociada() const {
    return this->corrida_associada;
}

int Evento::getIndiceParada() const {
    return this->indice_parada;
}

// Setters
void Evento::setTempo(double tempo) {
    this->tempo = tempo;
}

void Evento::setTipo(TipoEvento tipo) {
    this->tipo = tipo;
}

void Evento::setCorridaAssociada(Corrida* corrida) {
    this->corrida_associada = corrida;
}

void Evento::setIndiceParada(int indice) {
    this->indice_parada = indice;
}

// Operador de comparação para o heap
bool Evento::operator>(const Evento& outro) const {
    return this->tempo > outro.tempo;
}

// ==================== CLASSE ESCALONADOR ====================

// Construtor padrão
Escalonador::Escalonador() {
    this->capacidade = 100;
    this->heap = new Evento*[this->capacidade];
    this->tamanho = 0;
    this->total_eventos_processados = 0;
    this->total_eventos_inseridos = 0;
}

// Construtor parametrizado
Escalonador::Escalonador(int capacidade_inicial) {
    this->capacidade = capacidade_inicial;
    this->heap = new Evento*[this->capacidade];
    this->tamanho = 0;
    this->total_eventos_processados = 0;
    this->total_eventos_inseridos = 0;
}

// Destrutor
Escalonador::~Escalonador() {
    // Deletar eventos restantes
    for (int i = 0; i < this->tamanho; i++) {
        delete this->heap[i];
    }
    delete[] this->heap;
}

// Operações principais
void Escalonador::inicializa() {
    this->tamanho = 0;
    this->total_eventos_processados = 0;
    this->total_eventos_inseridos = 0;
}

void Escalonador::insereEvento(Evento* evento) {
    if (this->tamanho >= this->capacidade) {
        redimensionar();
    }
    
    this->heap[this->tamanho] = evento;
    heapifyUp(this->tamanho);
    this->tamanho++;
    this->total_eventos_inseridos++;
}

Evento* Escalonador::retiraProximoEvento() {
    if (this->tamanho == 0) {
        return nullptr;
    }
    
    Evento* evento_minimo = this->heap[0];
    this->tamanho--;
    
    if (this->tamanho > 0) {
        this->heap[0] = this->heap[this->tamanho];
        heapifyDown(0);
    }
    
    this->total_eventos_processados++;
    return evento_minimo;
}

void Escalonador::finaliza() {
    // Gerar estatísticas de escalonamento
    // Por enquanto, apenas limpar eventos restantes
    for (int i = 0; i < this->tamanho; i++) {
        delete this->heap[i];
    }
    this->tamanho = 0;
}

// Métodos auxiliares
bool Escalonador::estaVazio() const {
    return this->tamanho == 0;
}

int Escalonador::getTamanho() const {
    return this->tamanho;
}

double Escalonador::getTempoProximoEvento() const {
    if (this->tamanho == 0) {
        return -1.0;
    }
    return this->heap[0]->getTempo();
}

// Estatísticas
int Escalonador::getTotalEventosProcessados() const {
    return this->total_eventos_processados;
}

int Escalonador::getTotalEventosInseridos() const {
    return this->total_eventos_inseridos;
}

// Métodos privados do heap
void Escalonador::heapifyUp(int indice) {
    while (indice > 0) {
        int pai = getPai(indice);
        if (*this->heap[indice] > *this->heap[pai]) {
            break;
        }
        trocar(indice, pai);
        indice = pai;
    }
}

void Escalonador::heapifyDown(int indice) {
    while (true) {
        int menor = indice;
        int esquerdo = getFilhoEsquerdo(indice);
        int direito = getFilhoDireito(indice);
        
        if (esquerdo < this->tamanho && *this->heap[esquerdo] > *this->heap[menor]) {
            menor = esquerdo;
        }
        
        if (direito < this->tamanho && *this->heap[direito] > *this->heap[menor]) {
            menor = direito;
        }
        
        if (menor == indice) {
            break;
        }
        
        trocar(indice, menor);
        indice = menor;
    }
}

void Escalonador::redimensionar() {
    int nova_capacidade = this->capacidade * 2;
    Evento** novo_heap = new Evento*[nova_capacidade];
    
    for (int i = 0; i < this->tamanho; i++) {
        novo_heap[i] = this->heap[i];
    }
    
    delete[] this->heap;
    this->heap = novo_heap;
    this->capacidade = nova_capacidade;
}

int Escalonador::getPai(int indice) const {
    return (indice - 1) / 2;
}

int Escalonador::getFilhoEsquerdo(int indice) const {
    return 2 * indice + 1;
}

int Escalonador::getFilhoDireito(int indice) const {
    return 2 * indice + 2;
}

void Escalonador::trocar(int indice1, int indice2) {
    Evento* temp = this->heap[indice1];
    this->heap[indice1] = this->heap[indice2];
    this->heap[indice2] = temp;
}