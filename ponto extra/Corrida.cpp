#include "Corrida.hpp"
#include <cmath>

// Construtor padrão
Corrida::Corrida() {
    this->capacidade_ids = 2;
    this->ids_demandas = new int[this->capacidade_ids];
    this->num_demandas = 0;
    
    this->capacidade_trechos = 4;
    this->trechos = new Trecho*[this->capacidade_trechos];
    this->num_trechos = 0;
    
    this->capacidade_paradas = 4;
    this->paradas = new Parada*[this->capacidade_paradas];
    this->num_paradas = 0;
    
    this->duracao_total = 0.0;
    this->distancia_total = 0.0;
    this->eficiencia = 1.0;
    this->tempo_inicio = 0.0;  // NOVO
}

// Construtor parametrizado
Corrida::Corrida(int capacidade_inicial) {
    this->capacidade_ids = capacidade_inicial;
    this->ids_demandas = new int[this->capacidade_ids];
    this->num_demandas = 0;
    
    this->capacidade_trechos = capacidade_inicial * 2;
    this->trechos = new Trecho*[this->capacidade_trechos];
    this->num_trechos = 0;
    
    this->capacidade_paradas = capacidade_inicial * 2;
    this->paradas = new Parada*[this->capacidade_paradas];
    this->num_paradas = 0;
    
    this->duracao_total = 0.0;
    this->distancia_total = 0.0;
    this->eficiencia = 1.0;
    this->tempo_inicio = 0.0;  // NOVO
}

// Destrutor
Corrida::~Corrida() {
    delete[] this->ids_demandas;
    
    // Deletar os trechos
    for (int i = 0; i < this->num_trechos; i++) {
        delete this->trechos[i];
    }
    delete[] this->trechos;
    
    // Deletar as paradas
    for (int i = 0; i < this->num_paradas; i++) {
        delete this->paradas[i];
    }
    delete[] this->paradas;
}

// Getters
int* Corrida::getIdsDemandas() const {
    return this->ids_demandas;
}

int Corrida::getNumDemandas() const {
    return this->num_demandas;
}

Trecho** Corrida::getTrechos() const {
    return this->trechos;
}

int Corrida::getNumTrechos() const {
    return this->num_trechos;
}

Parada** Corrida::getParadas() const {
    return this->paradas;
}

int Corrida::getNumParadas() const {
    return this->num_paradas;
}

double Corrida::getDuracaoTotal() const {
    return this->duracao_total;
}

double Corrida::getDistanciaTotal() const {
    return this->distancia_total;
}

double Corrida::getEficiencia() const {
    return this->eficiencia;
}

// NOVO - Getter para tempo de início
double Corrida::getTempoInicio() const {
    return this->tempo_inicio;
}

// Setters
void Corrida::setDuracaoTotal(double duracao) {
    this->duracao_total = duracao;
}

void Corrida::setDistanciaTotal(double distancia) {
    this->distancia_total = distancia;
}

void Corrida::setEficiencia(double eficiencia) {
    this->eficiencia = eficiencia;
}

// NOVO - Setter para tempo de início
void Corrida::setTempoInicio(double tempo) {
    this->tempo_inicio = tempo;
}

// Métodos de manipulação
void Corrida::adicionarDemanda(int id_demanda) {
    if (this->num_demandas >= this->capacidade_ids) {
        redimensionarIds();
    }
    this->ids_demandas[this->num_demandas] = id_demanda;
    this->num_demandas++;
}

void Corrida::adicionarTrecho(Trecho* trecho) {
    if (this->num_trechos >= this->capacidade_trechos) {
        redimensionarTrechos();
    }
    this->trechos[this->num_trechos] = trecho;
    this->num_trechos++;
}

void Corrida::adicionarParada(Parada* parada) {
    if (this->num_paradas >= this->capacidade_paradas) {
        redimensionarParadas();
    }
    this->paradas[this->num_paradas] = parada;
    this->num_paradas++;
}

// Métodos auxiliares
void Corrida::calcularEficiencia(double* distancias_individuais) {
    if (this->distancia_total == 0.0) {
        this->eficiencia = 1.0;
        return;
    }
    
    double soma_distancias_individuais = 0.0;
    for (int i = 0; i < this->num_demandas; i++) {
        soma_distancias_individuais += distancias_individuais[i];
    }
    
    this->eficiencia = soma_distancias_individuais / this->distancia_total;
}

void Corrida::calcularDuracaoDistancia() {
    this->duracao_total = 0.0;
    this->distancia_total = 0.0;
    
    for (int i = 0; i < this->num_trechos; i++) {
        this->duracao_total += this->trechos[i]->getTempo();
        this->distancia_total += this->trechos[i]->getDistancia();
    }
}

bool Corrida::contemDemanda(int id_demanda) const {
    for (int i = 0; i < this->num_demandas; i++) {
        if (this->ids_demandas[i] == id_demanda) {
            return true;
        }
    }
    return false;
}

// ==================== NOVOS MÉTODOS PARA CORRIDA DINÂMICA ====================

// Limpa todos os trechos (mas não deleta as paradas)
void Corrida::limparTrechos() {
    for (int i = 0; i < this->num_trechos; i++) {
        delete this->trechos[i];
    }
    this->num_trechos = 0;
    this->duracao_total = 0.0;
    this->distancia_total = 0.0;
}

// Limpa todas as paradas
void Corrida::limparParadas() {
    for (int i = 0; i < this->num_paradas; i++) {
        delete this->paradas[i];
    }
    this->num_paradas = 0;
}

// Reconstrói a rota (trechos) com base nas paradas existentes
void Corrida::reconstruirRota(double velocidade) {
    // Limpar trechos antigos
    limparTrechos();
    
    // Criar novos trechos entre as paradas
    for (int i = 0; i < this->num_paradas - 1; i++) {
        // Determinar natureza do trecho
        NaturezaTrecho natureza;
        if (this->paradas[i]->getTipo() == EMBARQUE && this->paradas[i+1]->getTipo() == EMBARQUE) {
            natureza = COLETA;
        } else if (this->paradas[i]->getTipo() == DESEMBARQUE && this->paradas[i+1]->getTipo() == DESEMBARQUE) {
            natureza = ENTREGA;
        } else {
            natureza = DESLOCAMENTO;
        }
        
        Trecho* trecho = new Trecho(this->paradas[i], this->paradas[i+1], 0.0, 0.0, natureza);
        trecho->calcularTempoDistancia(velocidade);
        adicionarTrecho(trecho);
    }
    
    // Recalcular duração e distância total
    calcularDuracaoDistancia();
}

// Cria uma cópia profunda da corrida para testes
Corrida* Corrida::clonar() const {
    Corrida* clone = new Corrida(this->num_demandas);
    
    // Copiar IDs das demandas
    for (int i = 0; i < this->num_demandas; i++) {
        clone->adicionarDemanda(this->ids_demandas[i]);
    }
    
    // Copiar paradas (criar novas instâncias)
    for (int i = 0; i < this->num_paradas; i++) {
        Parada* parada_original = this->paradas[i];
        Parada* parada_clone = new Parada(
            parada_original->getCoordX(),
            parada_original->getCoordY(),
            parada_original->getTipo(),
            parada_original->getIdDemanda()
        );
        clone->adicionarParada(parada_clone);
    }
    
    // Copiar trechos (criar novas instâncias)
    for (int i = 0; i < this->num_trechos; i++) {
        Trecho* trecho_original = this->trechos[i];
        
        // Obter paradas correspondentes no clone
        Parada* parada_origem = clone->paradas[i];
        Parada* parada_destino = clone->paradas[i + 1];
        
        Trecho* trecho_clone = new Trecho(
            parada_origem,
            parada_destino,
            trecho_original->getTempo(),
            trecho_original->getDistancia(),
            trecho_original->getNatureza()
        );
        clone->adicionarTrecho(trecho_clone);
    }
    
    // Copiar atributos
    clone->setDuracaoTotal(this->duracao_total);
    clone->setDistanciaTotal(this->distancia_total);
    clone->setEficiencia(this->eficiencia);
    clone->setTempoInicio(this->tempo_inicio);
    
    return clone;
}

// Métodos privados de redimensionamento
void Corrida::redimensionarIds() {
    int nova_capacidade = this->capacidade_ids * 2;
    int* novo_array = new int[nova_capacidade];
    
    for (int i = 0; i < this->num_demandas; i++) {
        novo_array[i] = this->ids_demandas[i];
    }
    
    delete[] this->ids_demandas;
    this->ids_demandas = novo_array;
    this->capacidade_ids = nova_capacidade;
}

void Corrida::redimensionarTrechos() {
    int nova_capacidade = this->capacidade_trechos * 2;
    Trecho** novo_array = new Trecho*[nova_capacidade];
    
    for (int i = 0; i < this->num_trechos; i++) {
        novo_array[i] = this->trechos[i];
    }
    
    delete[] this->trechos;
    this->trechos = novo_array;
    this->capacidade_trechos = nova_capacidade;
}

void Corrida::redimensionarParadas() {
    int nova_capacidade = this->capacidade_paradas * 2;
    Parada** novo_array = new Parada*[nova_capacidade];
    
    for (int i = 0; i < this->num_paradas; i++) {
        novo_array[i] = this->paradas[i];
    }
    
    delete[] this->paradas;
    this->paradas = novo_array;
    this->capacidade_paradas = nova_capacidade;
}