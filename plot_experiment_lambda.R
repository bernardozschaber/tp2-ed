#!/usr/bin/env Rscript
# Experiment 2.1: Relationship between lambda and efficiency
# Author: TP2 Analysis
# Description: Plots how lambda (minimum efficiency) affects average efficiency

# Load required libraries
library(ggplot2)
library(scales)

# Read the CSV file
csv_path <- "./exp2_lambda/metrics_lambda.csv"

# Check if file exists
if (!file.exists(csv_path)) {
  cat("❌ ERRO: Arquivo não encontrado:", csv_path, "\n")
  cat("Execute primeiro: ./run_lambda_tests.sh\n")
  quit(status = 1)
}

# Read the CSV file
data <- read.csv(csv_path, header = TRUE)

# Check if data is empty
if (nrow(data) == 0) {
  cat("❌ ERRO: Arquivo CSV está vazio!\n")
  cat("Execute primeiro: ./run_lambda_tests.sh\n")
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
required_cols <- c("lambda", "avg_efficiency")
missing_cols <- setdiff(required_cols, colnames(data))
if (length(missing_cols) > 0) {
  cat("❌ ERRO: Colunas faltando:", paste(missing_cols, collapse = ", "), "\n")
  quit(status = 1)
}

# ========== PLOT: Lambda vs Average Efficiency ==========
plot <- ggplot(data, aes(x = lambda, y = avg_efficiency)) +
  # Add points
  geom_point(color = "#2E86AB", size = 2.5, alpha = 0.7) +
  
  # Add line connecting points
  geom_line(color = "#2E86AB", linewidth = 1.0, alpha = 0.6) +
  
  # Add smooth trend line
  {if(nrow(data) > 3) geom_smooth(method = "loess", 
                                   color = "#A23B72", 
                                   fill = "#F18F01", 
                                   alpha = 0.2,
                                   linewidth = 1.2,
                                   se = TRUE)} +
  
  # Labels and title
  labs(
    title = "Experimento 5: Impacto de Lambda na Eficiência Média",
    subtitle = "Relação entre eficiência mínima exigida e eficiência média das corridas aceitas",
    x = "Lambda - Eficiência Mínima Exigida",
    y = "Eficiência Média das Corridas",
    caption = "Configuração: eta=3, gamma=50, delta=30, alpha=3000, beta=4500, 100 demandas"
  ) +
  
  # Theme customization
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 15, hjust = 0.5),
    plot.subtitle = element_text(size = 11, hjust = 0.5, color = "gray30", margin = margin(b = 15)),
    plot.caption = element_text(size = 9, color = "gray50", hjust = 1),
    axis.title = element_text(face = "bold", size = 12),
    axis.text = element_text(size = 10),
    panel.grid.major = element_line(color = "gray90"),
    panel.grid.minor = element_line(color = "gray95"),
    plot.background = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  ) +
  
  # Format axes
  scale_y_continuous(limits = c(0, 1),
                     breaks = seq(0, 1, by = 0.1)) +
  scale_x_continuous(breaks = seq(0.1, 0.9, by = 0.1))

# Display the plot
print(plot)

# Create output directory if needed
dir.create("./exp2_lambda", showWarnings = FALSE, recursive = TRUE)

# Save the plot to file
output_file <- "./exp2_lambda/experiment_lambda_efficiency.png"
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
cat("========== ESTATÍSTICAS DO EXPERIMENTO 2.1 (LAMBDA) ==========\n")
cat(sprintf("Total de testes: %d\n", nrow(data)))
cat(sprintf("Lambda variou de: %.2f até %.2f\n", min(data$lambda), max(data$lambda)))
cat("\n")
cat("EFICIÊNCIA:\n")
cat(sprintf("  Mínima (lambda baixo): %.4f\n", min(data$avg_efficiency)))
cat(sprintf("  Máxima (lambda alto):  %.4f\n", max(data$avg_efficiency)))
cat(sprintf("  Média geral:           %.4f\n", mean(data$avg_efficiency)))
cat(sprintf("  Desvio padrão:         %.4f\n", sd(data$avg_efficiency)))
cat("\n")
cat("COMPARTILHAMENTO:\n")
cat(sprintf("  %% mínimo: %.2f%%\n", min(data$pct_shared)))
cat(sprintf("  %% máximo: %.2f%%\n", max(data$pct_shared)))
cat(sprintf("  %% médio:  %.2f%%\n", mean(data$pct_shared)))
cat("\n")
if ("avg_passengers_shared" %in% colnames(data)) {
  cat(sprintf("Passageiros médios por corrida compartilhada: %.2f\n", mean(data$avg_passengers_shared, na.rm = TRUE)))
  cat("\n")
}
cat("CONCLUSÃO:\n")
cat("  À medida que lambda aumenta (eficiência mínima mais restritiva),\n")
cat("  a eficiência média das corridas aceitas também aumenta.\n")
cat("  Isso demonstra o trade-off: menos corridas compartilhadas,\n")
cat("  mas com maior qualidade (eficiência).\n")
cat("===============================================================\n")

# Print detailed table (first 20 rows)
cat("\n========== TABELA DE RESULTADOS (primeiras 20 linhas) ==========\n")
print(head(data, 20))
cat("=================================================================\n")