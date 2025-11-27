#ifndef TRECHO_HPP
#define TRECHO_HPP

#include "Parada.hpp"

enum NaturezaTrecho {
    COLETA,      // Duas paradas de embarque
    ENTREGA,     // Duas paradas de desembarque
    DESLOCAMENTO // Um embarque e um desembarque
};

class Trecho {
private:
    Parada* parada_inicio;
    Parada* parada_fim;
    double tempo;
    double distancia;
    NaturezaTrecho natureza;
    
public:
    // Construtor
    Trecho();
    Trecho(Parada* inicio, Parada* fim, double tempo, double distancia, NaturezaTrecho natureza);
    
    // Destrutor
    ~Trecho();
    
    // Getters
    Parada* getParadaInicio() const;
    Parada* getParadaFim() const;
    double getTempo() const;
    double getDistancia() const;
    NaturezaTrecho getNatureza() const;
    
    // Setters
    void setParadaInicio(Parada* inicio);
    void setParadaFim(Parada* fim);
    void setTempo(double tempo);
    void setDistancia(double distancia);
    void setNatureza(NaturezaTrecho natureza);
    
    // Métodos auxiliares
    void calcularTempoDistancia(double velocidade);
};

#endif