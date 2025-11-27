#!/usr/bin/env Rscript
# Experiment 1.4: Relationship between eta and shared rides percentage
# Author: TP2 Analysis
# Description: Plots how eta (vehicle capacity) affects ride sharing

# Load required libraries
library(ggplot2)
library(scales)

# Read the CSV file
csv_path <- "./exp1_eta/metrics_eta.csv"

# Check if file exists
if (!file.exists(csv_path)) {
  cat("❌ ERRO: Arquivo não encontrado:", csv_path, "\n")
  cat("Execute primeiro: ./run_eta_tests.sh\n")
  quit(status = 1)
}

# Read the CSV file
data <- read.csv(csv_path, header = TRUE)

# Check if data is empty
if (nrow(data) == 0) {
  cat("❌ ERRO: Arquivo CSV está vazio!\n")
  cat("Execute primeiro: ./run_eta_tests.sh\n")
  quit(status = 1)
}

# Debug: Print data structure
cat("========== DEBUG: ESTRUTURA DOS DADOS ==========\n")
cat("Número de linhas:", nrow(data), "\n")
cat("Colunas:", paste(colnames(data), collapse = ", "), "\n")
cat("\n")
print(head(data))
cat("================================================\n\n")

# Check if required columns exist
required_cols <- c("eta", "pct_shared")
missing_cols <- setdiff(required_cols, colnames(data))
if (length(missing_cols) > 0) {
  cat("❌ ERRO: Colunas faltando:", paste(missing_cols, collapse = ", "), "\n")
  quit(status = 1)
}

# Check if pct_shared has valid values
if (all(is.na(data$pct_shared)) || all(data$pct_shared == 0)) {
  cat("⚠️  AVISO: Nenhuma corrida compartilhada detectada!\n")
  cat("Verifique se os testes foram executados corretamente.\n\n")
}

# Create the plot
plot <- ggplot(data, aes(x = eta, y = pct_shared)) +
  # Add points
  geom_point(color = "#2E86AB", size = 4, alpha = 0.8) +
  
  # Add line connecting points
  geom_line(color = "#2E86AB", linewidth = 1.2, alpha = 0.6) +
  
  # Labels and title
  labs(
    title = "Experimento 4: Impacto de Eta no Compartilhamento de Corridas",
    subtitle = "Relação entre capacidade do veículo e percentual de corridas compartilhadas",
    x = "Eta - Capacidade do Veículo (número de passageiros)",
    y = "Corridas Compartilhadas (%)",
    caption = "Configuração: gamma=50, delta=30, alpha=1000, beta=1500, lambda=0.6, 100 demandas"
  ) +
  
  # Theme customization
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    plot.subtitle = element_text(size = 11, hjust = 0.5, color = "gray30"),
    plot.caption = element_text(size = 9, color = "gray50", hjust = 1),
    axis.title = element_text(face = "bold", size = 12),
    axis.text = element_text(size = 10),
    panel.grid.major = element_line(color = "gray90"),
    panel.grid.minor = element_line(color = "gray95"),
    plot.background = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  ) +
  
  # Format axes - MESMA ESCALA DOS OUTROS (0-100%)
  scale_y_continuous(labels = function(x) paste0(x, "%"),
                     limits = c(0, 100),
                     breaks = seq(0, 100, by = 10)) +
  scale_x_continuous(breaks = data$eta)  # Show all eta values

# Display the plot
print(plot)

# Create output directory if needed
dir.create("./exp1_eta", showWarnings = FALSE, recursive = TRUE)

# Save the plot to file
output_file <- "./exp1_eta/experiment_eta_vs_sharing.png"
ggsave(output_file, 
       plot = plot, 
       width = 10, 
       height = 6, 
       dpi = 300,
       bg = "white")

cat("\n✅ Gráfico gerado com sucesso!\n")
cat("📊 Arquivo salvo:", output_file, "\n")
cat("\n")

# Print summary statistics
cat("========== ESTATÍSTICAS DO EXPERIMENTO 1.4 (ETA) ==========\n")
cat(sprintf("Total de testes: %d\n", nrow(data)))
cat(sprintf("Eta variou de: %d até %d\n", min(data$eta), max(data$eta)))
cat(sprintf("Compartilhamento mínimo: %.2f%%\n", min(data$pct_shared)))
cat(sprintf("Compartilhamento máximo: %.2f%%\n", max(data$pct_shared)))
cat(sprintf("Compartilhamento médio: %.2f%%\n", mean(data$pct_shared)))
if ("avg_passengers_shared" %in% colnames(data)) {
  cat(sprintf("Passageiros médios por corrida compartilhada: %.2f\n", mean(data$avg_passengers_shared, na.rm = TRUE)))
}
if ("avg_efficiency" %in% colnames(data)) {
  cat(sprintf("Eficiência média: %.4f\n", mean(data$avg_efficiency, na.rm = TRUE)))
}
cat("==============================================================\n")

# Print detailed table
cat("\n========== TABELA DE RESULTADOS ==========\n")
print(data)
cat("==========================================\n")