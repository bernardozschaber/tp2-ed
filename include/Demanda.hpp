#ifndef DEMANDA_HPP
#define DEMANDA_HPP

// Forward declaration para evitar dependência circular
class Corrida;

enum EstadoDemanda {
    DEMANDADA,
    INDIVIDUAL,
    COMBINADA,
    CONCLUIDA
};

class Demanda {
private:
    int id;
    double tempo_solicitacao;
    double origem_x;
    double origem_y;
    double destino_x;
    double destino_y;
    
    EstadoDemanda estado;
    Corrida* corrida_associada;
    
    // Estatísticas de execução
    double tempo_conclusao;
    double distancia_percorrida;
    
public:
    // Construtor
    Demanda();
    Demanda(int id, double tempo, double ox, double oy, double dx, double dy);
    
    // Destrutor
    ~Demanda();
    
    // Getters
    int getId() const;
    double getTempoSolicitacao() const;
    double getOrigemX() const;
    double getOrigemY() const;
    double getDestinoX() const;
    double getDestinoY() const;
    EstadoDemanda getEstado() const;
    Corrida* getCorridaAssociada() const;
    double getTempoConclusao() const;
    double getDistanciaPercorrida() const;
    
    // Setters
    void setEstado(EstadoDemanda novo_estado);
    void setCorridaAssociada(Corrida* corrida);
    void setTempoConclusao(double tempo);
    void setDistanciaPercorrida(double distancia);
    
    // Métodos auxiliares
    double calcularDistanciaOrigem(const Demanda& outra) const;
    double calcularDistanciaDestino(const Demanda& outra) const;
    double calcularDistanciaCorrida() const;
};

#endif