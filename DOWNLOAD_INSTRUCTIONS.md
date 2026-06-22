# 📥 Como Acessar e Baixar os Resultados

Os arquivos com os resultados experimentais estão disponíveis em dois formatos:

## ✅ Opção 1: GitHub (Recomendado)

Todos os arquivos estão no repositório GitHub:
**https://github.com/qlaudialara/sorting-algorithms/tree/main/downloads**

### Arquivos Disponíveis:

1. **Excel Completo** (Melhor para análise)
   - `Sorting_Algorithms_Analysis.xlsx` (11.6 KB)
   - 6 abas com dados completos e análises

2. **CSVs Individuais** (Para importação)
   - `01_Sorting_Algorithms_Full_Results.csv` - Todos os 20 resultados
   - `02_Algorithm_Rankings.csv` - Rankings ordenados
   - `03_Performance_by_Data_Type.csv` - Segmentado por tipo de dado
   - `04_Performance_by_Structure.csv` - Segmentado por estrutura
   - `05_Performance_by_Size.csv` - Segmentado por tamanho

3. **Relatório em Texto**
   - `06_Detailed_Report.txt` - Relatório formatado pronto para imprimir

4. **Markdown**
   - `Results_Summary.md` - Resumo em formato Markdown

### Como Baixar do GitHub:

**Opção A: Clicar e Baixar**
1. Acesse: https://github.com/qlaudialara/sorting-algorithms/tree/main/downloads
2. Clique no arquivo desejado
3. Clique no botão "Download" (ícone de seta para baixo)

**Opção B: Linha de Comando (Git)**
```bash
git clone https://github.com/qlaudialara/sorting-algorithms.git
cd sorting-algorithms/downloads
# Agora os arquivos estão em ./downloads/
```

**Opção C: CURL/Wget**
```bash
# Exemplo para Excel
curl -O https://raw.githubusercontent.com/qlaudialara/sorting-algorithms/main/downloads/Sorting_Algorithms_Analysis.xlsx

# Ou com wget
wget https://raw.githubusercontent.com/qlaudialara/sorting-algorithms/main/downloads/Sorting_Algorithms_Analysis.xlsx
```

---

## ⚙️ Opção 2: Servidor Local

Se estiver com o repositório clonado localmente, você pode executar um servidor HTTP para acessar os arquivos:

### 1. Iniciar o Servidor
```bash
cd /Users/qlaudia/sorting-experiment
python3 download_server.py 8000
```

Você verá:
```
================================================================================
📥 DOWNLOAD SERVER STARTED
================================================================================

🌐 Server running at: http://localhost:8000
📂 Downloads directory: /Users/qlaudia/sorting-experiment/downloads

Available files:
  1. 01_Sorting_Algorithms_Full_Results.csv     (  2.2 KB)
     → http://localhost:8000/downloads/01_Sorting_Algorithms_Full_Results.csv
  2. 02_Algorithm_Rankings.csv                  (  0.5 KB)
     → http://localhost:8000/downloads/02_Algorithm_Rankings.csv
  ...
```

### 2. Acessar Arquivos

**No Navegador:**
- Acesse: http://localhost:8000
- Clique no arquivo para baixar

**Com cURL:**
```bash
curl -O http://localhost:8000/downloads/Sorting_Algorithms_Analysis.xlsx
```

### 3. Parar o Servidor
Pressione `Ctrl+C` no terminal

---

## 📊 Arquivos por Uso

| Caso de Uso | Arquivo Recomendado |
|---|---|
| 📈 Análise completa no Excel | `Sorting_Algorithms_Analysis.xlsx` |
| 📋 Ver rankings | `02_Algorithm_Rankings.csv` |
| 💾 Importar em banco de dados | `01_Sorting_Algorithms_Full_Results.csv` |
| 🖨️ Imprimir relatório | `06_Detailed_Report.txt` |
| 📝 Incluir em documentação | `Results_Summary.md` |
| 🔬 Análise estatística (Python/R) | `01_Sorting_Algorithms_Full_Results.csv` |

---

## 📋 Resumo dos Dados

**Resultados Experimentais:**
- 20 configurações testadas
- 9 algoritmos de ordenação
- 3 tipos de dados (integer, float, string)
- 5 estruturas de entrada (random, sorted, reversed, nearly_sorted, flat)

**Melhor Performance:** Tim Sort (0.001341s)
**Pior Performance:** Counting Sort (0.185395s)

---

## 🤔 Perguntas Frequentes

**P: Qual arquivo devo baixar?**
R: Comece com `Sorting_Algorithms_Analysis.xlsx` para ter tudo em um lugar.

**P: Os dados são estatisticamente confiáveis?**
R: Cada configuração foi executada 5-10 vezes. Consulte `std_dev` para variabilidade.

**P: Posso usar estes dados em meu projeto?**
R: Sim! O projeto usa licença MIT. Créditos apreciados mas não obrigatórios.

**P: Como reproduzir estes resultados?**
R: Execute `python3 quick_results.py` para gerar novos resultados.

---

**Última Atualização:** 22 de Junho de 2026
**Repositório:** https://github.com/qlaudialara/sorting-algorithms
