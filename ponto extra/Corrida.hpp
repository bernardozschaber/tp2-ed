#ifndef CORRIDA_HPP
#define CORRIDA_HPP

#include "Trecho.hpp"
#include "Parada.hpp"

class Corrida {
private:
    int* ids_demandas;          // Array de IDs das demandas satisfeitas
    int num_demandas;           // Número de demandas nesta corrida
    int capacidade_ids;         // Capacidade alocada para o array
    
    Trecho** trechos;           // Array de ponteiros para trechos
    int num_trechos;            // Número de trechos
    int capacidade_trechos;     // Capacidade alocada para o array
    
    Parada** paradas;           // Array de todas as paradas da corrida
    int num_paradas;            // Número total de paradas
    int capacidade_paradas;     // Capacidade alocada para o array
    
    double duracao_total;       // Duração total da corrida
    double distancia_total;     // Distância total percorrida
    double eficiencia;          // Eficiência da corrida
    double tempo_inicio;        // Tempo de início da corrida (NOVO)
    
public:
    // Construtor
    Corrida();
    Corrida(int capacidade_inicial);
    
    // Destrutor
    ~Corrida();
    
    // Getters
    int* getIdsDemandas() const;
    int getNumDemandas() const;
    Trecho** getTrechos() const;
    int getNumTrechos() const;
    Parada** getParadas() const;
    int getNumParadas() const;
    double getDuracaoTotal() const;
    double getDistanciaTotal() const;
    double getEficiencia() const;
    double getTempoInicio() const;  // NOVO - para corrida dinâmica
    
    // Setters
    void setDuracaoTotal(double duracao);
    void setDistanciaTotal(double distancia);
    void setEficiencia(double eficiencia);
    void setTempoInicio(double tempo);  // NOVO - para corrida dinâmica
    
    // Métodos de manipulação
    void adicionarDemanda(int id_demanda);
    void adicionarTrecho(Trecho* trecho);
    void adicionarParada(Parada* parada);
    
    // Métodos auxiliares
    void calcularEficiencia(double* distancias_individuais);
    void calcularDuracaoDistancia();
    bool contemDemanda(int id_demanda) const;
    
    // NOVOS - Métodos para corrida dinâmica
    void limparTrechos();                    // Remove todos os trechos
    void limparParadas();                    // Remove todas as paradas
    void reconstruirRota(double velocidade); // Reconstrói trechos/paradas após adicionar demanda
    Corrida* clonar() const;                 // Cria cópia da corrida para teste
    
private:
    // Métodos auxiliares para redimensionamento
    void redimensionarIds();
    void redimensionarTrechos();
    void redimensionarParadas();
};

#endif