#ifndef PARADA_HPP
#define PARADA_HPP

enum TipoParada {
    EMBARQUE,
    DESEMBARQUE
};

class Parada {
private:
    double coord_x;
    double coord_y;
    TipoParada tipo;
    int id_demanda; // ID da demanda associada a esta parada
    
public:
    // Construtor
    Parada();
    Parada(double x, double y, TipoParada tipo, int id_demanda);
    
    // Destrutor
    ~Parada();
    
    // Getters
    double getCoordX() const;
    double getCoordY() const;
    TipoParada getTipo() const;
    int getIdDemanda() const;
    
    // Setters
    void setCoordX(double x);
    void setCoordY(double y);
    void setTipo(TipoParada tipo);
    void setIdDemanda(int id);
    
    // Métodos auxiliares
    double calcularDistancia(const Parada& outra) const;
};

#endif