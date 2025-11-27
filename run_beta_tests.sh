#!/bin/bash
# ---------------------------------------------------------
# Script para executar testes do Experimento 1.3 - Beta
# Coleta métricas de corridas compartilhadas
# ---------------------------------------------------------

BIN="./bin/tp2.out"
INPUT_DIR="./exp1_beta/inputs"
OUTPUT_DIR="./exp1_beta/outputs"
METRICS_FILE="./exp1_beta/metrics_beta.csv"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "========================================="
echo "  EXPERIMENT 1.3 - BETA VARIATION"
echo "========================================="
echo ""

# Verifica se o executável existe
if [ ! -f "$BIN" ]; then
    echo -e "${RED}❌ Executável não encontrado! Rode 'make' antes.${NC}"
    exit 1
fi

# Cria diretórios se não existirem
mkdir -p "$OUTPUT_DIR"
mkdir -p "$(dirname "$METRICS_FILE")"

# Verifica se há arquivos de input
input_count=$(ls -1 "$INPUT_DIR"/input_beta_*.txt 2>/dev/null | wc -l)
if [ "$input_count" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Nenhum arquivo de input encontrado em $INPUT_DIR${NC}"
    echo "Crie arquivos executando: python3 generate_beta_tests.py"
    exit 1
fi

echo -e "${CYAN}📊 Experimento 1.3: Variação de Beta${NC}"
echo -e "${BLUE}📁 Diretório de inputs: $INPUT_DIR${NC}"
echo -e "${BLUE}📁 Diretório de outputs: $OUTPUT_DIR${NC}"
echo -e "${BLUE}📊 Arquivo de métricas: $METRICS_FILE${NC}"
echo -e "${BLUE}📂 Total de inputs: $input_count${NC}"
echo ""
echo -e "${YELLOW}📊 Iniciando testes...${NC}"
echo ""

# Cria header do CSV de métricas
echo "test_num,beta,total_demands,individual_rides,shared_rides,pct_shared,avg_passengers_shared,avg_efficiency" > "$METRICS_FILE"

# Contador de sucessos e falhas
success_count=0
fail_count=0

# Processa todos os arquivos de input EM ORDEM
for input_file in $(ls -1 "$INPUT_DIR"/input_beta_*.txt | sort -V); do
    if [ ! -f "$input_file" ]; then
        continue
    fi
    
    # Extrai o número do teste
    filename=$(basename "$input_file")
    test_num=$(echo "$filename" | sed 's/input_beta_\([0-9]*\).txt/\1/')
    
    output_file="$OUTPUT_DIR/output_beta_${test_num}.txt"
    
    # Show progress only every 10 tests
    if [ $((success_count % 10)) -eq 0 ]; then
        echo -e "${YELLOW}🧪 [$((success_count + fail_count + 1))/$input_count] Testando $filename ...${NC}"
    fi
    
    # Roda o programa
    $BIN < "$input_file" > "$output_file" 2>&1
    
    # Verifica se executou com sucesso
    if [ $? -eq 0 ]; then
        # Extrai métricas do input
        total_demands=$(head -n 7 "$input_file" | tail -n 1)
        beta=$(head -n 5 "$input_file" | tail -n 1)
        
        # Conta corridas individuais (2 paradas) e compartilhadas (>2 paradas)
        individual_rides=$(awk '{if($3==2) print}' "$output_file" | wc -l)
        shared_rides=$(awk '{if($3>2) print}' "$output_file" | wc -l)
        total_rides=$((individual_rides + shared_rides))
        
        # Calcula % de corridas compartilhadas usando AWK (mais portável que bc)
        if [ "$total_rides" -gt 0 ]; then
            pct_shared=$(awk "BEGIN {printf \"%.2f\", 100 * $shared_rides / $total_rides}")
        else
            pct_shared="0.00"
        fi
        
        # Calcula média de passageiros por corrida compartilhada
        if [ "$shared_rides" -gt 0 ]; then
            avg_passengers=$(awk '{if($3>2) {sum+=$3/2; count++}} END {if(count>0) printf "%.2f", sum/count; else print "0.00"}' "$output_file")
        else
            avg_passengers="0.00"
        fi
        
        # Calcula eficiência média
        avg_efficiency=$(awk '{sum+=$3; count++} END {if(count>0) printf "%.4f", sum/count; else print "0.0000"}' "$output_file")
        
        # Salva métricas no CSV
        echo "$test_num,$beta,$total_demands,$individual_rides,$shared_rides,$pct_shared,$avg_passengers,$avg_efficiency" >> "$METRICS_FILE"
        
        success_count=$((success_count + 1))
    else
        echo -e "${RED}  ❌ Erro ao executar o teste $test_num${NC}"
        fail_count=$((fail_count + 1))
    fi
done

echo ""
echo "========================================="
echo -e "${GREEN}✨ Testes finalizados!${NC}"
echo "========================================="
echo ""
echo -e "${CYAN}📊 Resultados do Experimento 1.3:${NC}"
echo "  ✅ Sucessos: $success_count"
echo "  ❌ Falhas: $fail_count"
echo ""

if [ -f "$METRICS_FILE" ]; then
    echo -e "${GREEN}📁 Arquivo de métricas criado:${NC}"
    echo "  $METRICS_FILE"
    echo ""
    echo -e "${CYAN}📋 Primeiras linhas das métricas:${NC}"
    head -n 11 "$METRICS_FILE"
    echo ""
fi