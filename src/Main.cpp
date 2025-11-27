#include <iostream>
#include <iomanip>
#include <cmath>
#include <exception>
#include <string>
#include "Demanda.hpp"
#include "Parada.hpp"
#include "Trecho.hpp"
#include "Corrida.hpp"
#include "Escalonador.hpp"

using namespace std;

// ==================== EXCEÇÕES CUSTOMIZADAS ====================

class SimulacaoException : public exception {
protected:
    string mensagem;
public:
    SimulacaoException(const string& msg) : mensagem(msg) {}
    virtual const char* what() const throw() {
        return mensagem.c_str();
    }
};

class ParametroInvalidoException : public SimulacaoException {
public:
    ParametroInvalidoException(const string& msg) : SimulacaoException(msg) {}
};

class DemandaInvalidaException : public SimulacaoException {
public:
    DemandaInvalidaException(const string& msg) : SimulacaoException(msg) {}
};

class MemoriaInsuficienteException : public SimulacaoException {
public:
    MemoriaInsuficienteException(const string& msg) : SimulacaoException(msg) {}
};

class EstadoInvalidoException : public SimulacaoException {
public:
    EstadoInvalidoException(const string& msg) : SimulacaoException(msg) {}
};

// ==================== ESTRUTURA PARA RESULTADOS ====================

struct ResultadoCorrida {
    double tempo_conclusao;
    Corrida* corrida;
};

// ==================== FUNÇÕES DE ORDENAÇÃO (QUICKSORT) ====================

void trocarResultados(ResultadoCorrida& a, ResultadoCorrida& b) {
    ResultadoCorrida temp = a;
    a = b;
    b = temp;
}

int particionar(ResultadoCorrida* resultados, int inicio, int fim) {
    double pivo = resultados[fim].tempo_conclusao;
    int i = inicio - 1;
    
    for (int j = inicio; j < fim; j++) {
        if (resultados[j].tempo_conclusao <= pivo) {
            i++;
            trocarResultados(resultados[i], resultados[j]);
        }
    }
    
    trocarResultados(resultados[i + 1], resultados[fim]);
    return i + 1;
}

void quicksort(ResultadoCorrida* resultados, int inicio, int fim) {
    if (inicio < fim) {
        int pivo = particionar(resultados, inicio, fim);
        quicksort(resultados, inicio, pivo - 1);
        quicksort(resultados, pivo + 1, fim);
    }
}

void ordenarResultados(ResultadoCorrida* resultados, int tamanho) {
    if (tamanho > 1) {
        quicksort(resultados, 0, tamanho - 1);
    }
}

// ==================== FUNÇÕES AUXILIARES ====================

double calcularDistancia(double x1, double y1, double x2, double y2) {
    double dx = x2 - x1;
    double dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}

void validarParametros(int eta, double gama, double delta, double alfa, double beta, double lambda) {
    if (eta <= 0) {
        throw ParametroInvalidoException("Capacidade do veiculo (eta) deve ser positiva");
    }
    if (gama <= 0.0) {
        throw ParametroInvalidoException("Velocidade do veiculo (gama) deve ser positiva");
    }
    if (delta < 0.0) {
        throw ParametroInvalidoException("Intervalo temporal (delta) nao pode ser negativo");
    }
    if (alfa < 0.0) {
        throw ParametroInvalidoException("Distancia maxima entre origens (alfa) nao pode ser negativa");
    }
    if (beta < 0.0) {
        throw ParametroInvalidoException("Distancia maxima entre destinos (beta) nao pode ser negativa");
    }
    if (lambda < 0.0 || lambda > 1.0) {
        throw ParametroInvalidoException("Eficiencia minima (lambda) deve estar entre 0 e 1");
    }
}

bool verificarCriteriosCompartilhamento(Demanda** demandas_corrida, int num_demandas, 
                                        Demanda* nova_demanda, double alfa, double beta) {
    // Verificar distâncias entre todas as origens
    for (int i = 0; i < num_demandas; i++) {
        double dist_origem = demandas_corrida[i]->calcularDistanciaOrigem(*nova_demanda);
        if (dist_origem > alfa) {
            return false;
        }
    }
    
    // Verificar distâncias entre todos os destinos
    for (int i = 0; i < num_demandas; i++) {
        double dist_destino = demandas_corrida[i]->calcularDistanciaDestino(*nova_demanda);
        if (dist_destino > beta) {
            return false;
        }
    }
    
    return true;
}

Corrida* construirCorrida(Demanda** demandas_corrida, int num_demandas, double gama, double tempo_inicio) {
    if (num_demandas <= 0) {
        throw EstadoInvalidoException("Tentativa de construir corrida sem demandas");
    }
    
    Corrida* corrida = new Corrida(num_demandas);
    
    // Adicionar IDs das demandas
    for (int i = 0; i < num_demandas; i++) {
        corrida->adicionarDemanda(demandas_corrida[i]->getId());
    }
    
    // Criar paradas de embarque (origens) na ordem das demandas
    for (int i = 0; i < num_demandas; i++) {
        Parada* parada_embarque = new Parada(
            demandas_corrida[i]->getOrigemX(),
            demandas_corrida[i]->getOrigemY(),
            EMBARQUE,
            demandas_corrida[i]->getId()
        );
        corrida->adicionarParada(parada_embarque);
    }
    
    // Criar paradas de desembarque (destinos) na ordem das demandas
    for (int i = 0; i < num_demandas; i++) {
        Parada* parada_desembarque = new Parada(
            demandas_corrida[i]->getDestinoX(),
            demandas_corrida[i]->getDestinoY(),
            DESEMBARQUE,
            demandas_corrida[i]->getId()
        );
        corrida->adicionarParada(parada_desembarque);
    }
    
    // Criar trechos
    Parada** paradas = corrida->getParadas();
    int total_paradas = corrida->getNumParadas();
    
    for (int i = 0; i < total_paradas - 1; i++) {
        // Determinar natureza do trecho
        NaturezaTrecho natureza;
        if (paradas[i]->getTipo() == EMBARQUE && paradas[i+1]->getTipo() == EMBARQUE) {
            natureza = COLETA;
        } else if (paradas[i]->getTipo() == DESEMBARQUE && paradas[i+1]->getTipo() == DESEMBARQUE) {
            natureza = ENTREGA;
        } else {
            natureza = DESLOCAMENTO;
        }
        
        Trecho* trecho = new Trecho(paradas[i], paradas[i+1], 0.0, 0.0, natureza);
        trecho->calcularTempoDistancia(gama);
        corrida->adicionarTrecho(trecho);
    }
    
    // Calcular duração e distância total
    corrida->calcularDuracaoDistancia();
    
    return corrida;
}

double calcularEficienciaCorrida(Demanda** demandas_corrida, int num_demandas, double distancia_total) {
    if (distancia_total == 0.0) {
        return 1.0;
    }
    
    double soma_distancias_individuais = 0.0;
    for (int i = 0; i < num_demandas; i++) {
        soma_distancias_individuais += demandas_corrida[i]->calcularDistanciaCorrida();
    }
    
    return soma_distancias_individuais / distancia_total;
}

void imprimirCorrida(Corrida* corrida, double tempo_conclusao) {
    // Formato: <tempo_conclusão> <distância_total> <eficiência> <num_paradas> <x1> <y1> <x2> <y2> ...
    cout << fixed << setprecision(2);
    cout << tempo_conclusao << " ";
    cout << corrida->getDistanciaTotal() << " ";
    cout << corrida->getEficiencia() << " ";  // ← ADICIONADO
    cout << corrida->getNumParadas();
    
    Parada** paradas = corrida->getParadas();
    for (int i = 0; i < corrida->getNumParadas(); i++) {
        cout << " " << paradas[i]->getCoordX() << " " << paradas[i]->getCoordY();
    }
    cout << endl;
}

// ==================== MAIN ====================

int main() {
    try {
        // Leitura dos parâmetros
        int eta;
        double gama, delta, alfa, beta, lambda;
        int num_demandas;
        
        cin >> eta >> gama >> delta >> alfa >> beta >> lambda >> num_demandas;
        
        // Validar parâmetros
        validarParametros(eta, gama, delta, alfa, beta, lambda);
        
        if (num_demandas <= 0) {
            throw ParametroInvalidoException("Numero de demandas deve ser positivo");
        }
        
        // Alocar array de demandas
        Demanda** demandas = new Demanda*[num_demandas];
        if (demandas == nullptr) {
            throw MemoriaInsuficienteException("Falha ao alocar memoria para demandas");
        }
        
        // Ler demandas
        for (int i = 0; i < num_demandas; i++) {
            int id;
            double tempo, ox, oy, dx, dy;
            cin >> id >> tempo >> ox >> oy >> dx >> dy;
            
            demandas[i] = new Demanda(id, tempo, ox, oy, dx, dy);
            if (demandas[i] == nullptr) {
                throw MemoriaInsuficienteException("Falha ao alocar memoria para demanda");
            }
        }
        
        // Array de corridas criadas
        Corrida** corridas = new Corrida*[num_demandas];
        int num_corridas = 0;
        
        // Escalonador de eventos
        Escalonador escalonador(num_demandas * 10);
        escalonador.inicializa();
        
        // ==================== CONSTRUÇÃO DAS CORRIDAS ====================
        
        for (int i = 0; i < num_demandas; i++) {
            // Pular demandas já processadas
            if (demandas[i]->getEstado() != DEMANDADA) {
                continue;
            }
            
            // Conjunto de demandas para a corrida atual
            Demanda** demandas_corrida = new Demanda*[eta];
            demandas_corrida[0] = demandas[i];
            int num_demandas_corrida = 1;
            
            double tempo_base = demandas[i]->getTempoSolicitacao();
            
            // Tentar combinar com outras demandas
            for (int j = i + 1; j < num_demandas && num_demandas_corrida < eta; j++) {
                if (demandas[j]->getEstado() != DEMANDADA) {
                    continue;
                }
                
                // Critério 1: Intervalo de tempo
                double diff_tempo = demandas[j]->getTempoSolicitacao() - tempo_base;
                if (diff_tempo >= delta) {
                    break; // Não há mais candidatos dentro do intervalo
                }
                
                // Critério 2 e 3: Distância entre origens e destinos
                if (!verificarCriteriosCompartilhamento(demandas_corrida, num_demandas_corrida, demandas[j], alfa, beta)) {
                    continue;
                }
                
                // Construir corrida temporária para verificar eficiência
                demandas_corrida[num_demandas_corrida] = demandas[j];
                num_demandas_corrida++;
                
                Corrida* corrida_temp = construirCorrida(demandas_corrida, num_demandas_corrida, gama, tempo_base);
                double eficiencia = calcularEficienciaCorrida(demandas_corrida, num_demandas_corrida, corrida_temp->getDistanciaTotal());
                
                // Critério 4: Eficiência
                if (eficiencia < lambda) {
                    // Remover última demanda adicionada
                    num_demandas_corrida--;
                    delete corrida_temp;
                    break;
                }
                
                delete corrida_temp;
            }
            
            // Construir corrida final
            Corrida* corrida_final = construirCorrida(demandas_corrida, num_demandas_corrida, gama, tempo_base);
            double eficiencia_final = calcularEficienciaCorrida(demandas_corrida, num_demandas_corrida, corrida_final->getDistanciaTotal());
            corrida_final->setEficiencia(eficiencia_final);
            
            // Atualizar estado das demandas
            for (int k = 0; k < num_demandas_corrida; k++) {
                if (num_demandas_corrida == 1) {
                    demandas_corrida[k]->setEstado(INDIVIDUAL);
                } else {
                    demandas_corrida[k]->setEstado(COMBINADA);
                }
                demandas_corrida[k]->setCorridaAssociada(corrida_final);
            }
            
            corridas[num_corridas] = corrida_final;
            num_corridas++;
            
            // Escalonar primeiro evento (primeira coleta)
            Evento* primeiro_evento = new Evento(tempo_base, COLETA_PASSAGEIRO, corrida_final, 0);
            escalonador.insereEvento(primeiro_evento);
            
            delete[] demandas_corrida;
        }
        
        // ==================== SIMULAÇÃO DE EVENTOS ====================
        
        // Array para armazenar resultados
        ResultadoCorrida* resultados = new ResultadoCorrida[num_corridas];
        int num_resultados = 0;
        
        while (!escalonador.estaVazio()) {
            Evento* evento_atual = escalonador.retiraProximoEvento();
            
            if (evento_atual == nullptr) {
                break;
            }
            
            Corrida* corrida_evento = evento_atual->getCorridaAssociada();
            int indice_parada_atual = evento_atual->getIndiceParada();
            int total_paradas = corrida_evento->getNumParadas();
            
            // Se for a última parada, armazenar resultado
            if (indice_parada_atual >= total_paradas - 1) {
                double tempo_conclusao = evento_atual->getTempo();
                resultados[num_resultados].tempo_conclusao = tempo_conclusao;
                resultados[num_resultados].corrida = corrida_evento;
                num_resultados++;
            } else {
                // Escalonar próxima parada
                Trecho** trechos = corrida_evento->getTrechos();
                double tempo_proximo = evento_atual->getTempo() + trechos[indice_parada_atual]->getTempo();
                
                Evento* proximo_evento = new Evento(tempo_proximo, COLETA_PASSAGEIRO, corrida_evento, indice_parada_atual + 1);
                escalonador.insereEvento(proximo_evento);
            }
            
            delete evento_atual;
        }
        
        // Ordenar resultados por tempo de conclusão (QuickSort implementado manualmente)
        ordenarResultados(resultados, num_resultados);
        
        // Imprimir resultados ordenados
        for (int i = 0; i < num_resultados; i++) {
            imprimirCorrida(resultados[i].corrida, resultados[i].tempo_conclusao);
        }
        
        delete[] resultados;
        
        // ==================== LIMPEZA DE MEMÓRIA ====================
        
        escalonador.finaliza();
        
        for (int i = 0; i < num_corridas; i++) {
            delete corridas[i];
        }
        delete[] corridas;
        
        for (int i = 0; i < num_demandas; i++) {
            delete demandas[i];
        }
        delete[] demandas;
        
        return 0;
        
    } catch (const SimulacaoException& e) {
        cerr << "Erro de simulacao: " << e.what() << endl;
        return 1;
    } catch (const exception& e) {
        cerr << "Erro inesperado: " << e.what() << endl;
        return 1;
    } catch (...) {
        cerr << "Erro desconhecido" << endl;
        return 1;
    }
}