#ifndef ESCALONADOR_HPP
#define ESCALONADOR_HPP

#include "Corrida.hpp"

enum TipoEvento {
    COLETA_PASSAGEIRO,
    ENTREGA_PASSAGEIRO
};

class Evento {
private:
    double tempo;
    TipoEvento tipo;
    Corrida* corrida_associada;
    int indice_parada; // Índice da próxima parada na corrida
    
public:
    // Construtor
    Evento();
    Evento(double tempo, TipoEvento tipo, Corrida* corrida, int indice_parada);
    
    // Destrutor
    ~Evento();
    
    // Getters
    double getTempo() const;
    TipoEvento getTipo() const;
    Corrida* getCorridaAssociada() const;
    int getIndiceParada() const;
    
    // Setters
    void setTempo(double tempo);
    void setTipo(TipoEvento tipo);
    void setCorridaAssociada(Corrida* corrida);
    void setIndiceParada(int indice);
    
    // Operador de comparação para o heap
    bool operator>(const Evento& outro) const;
};

class Escalonador {
private:
    Evento** heap;           // Array de ponteiros para eventos (minheap)
    int tamanho;             // Número atual de eventos
    int capacidade;          // Capacidade do heap
    
    // Estatísticas
    int total_eventos_processados;
    int total_eventos_inseridos;
    
public:
    // Construtor
    Escalonador();
    Escalonador(int capacidade_inicial);
    
    // Destrutor
    ~Escalonador();
    
    // Operações principais
    void inicializa();
    void insereEvento(Evento* evento);
    Evento* retiraProximoEvento();
    void finaliza();
    
    // Métodos auxiliares
    bool estaVazio() const;
    int getTamanho() const;
    double getTempoProximoEvento() const;
    
    // Estatísticas
    int getTotalEventosProcessados() const;
    int getTotalEventosInseridos() const;
    
private:
    // Métodos auxiliares do heap
    void heapifyUp(int indice);
    void heapifyDown(int indice);
    void redimensionar();
    int getPai(int indice) const;
    int getFilhoEsquerdo(int indice) const;
    int getFilhoDireito(int indice) const;
    void trocar(int indice1, int indice2);
};

#endif