# Canadian Architectural & Engineering Services Price Analysis

![Dashboard Screenshot](analysis/assets/interactive_dashboard.png)

## 📌 Project Overview
Analysis of Statistics Canada's **AESPI** dataset tracking professional service prices across Canadian regions (2018-2024). Combines:
- Exploratory data analysis (Jupyter Notebook)
- Interactive dashboard (Plotly Dash)
- Regional price trend visualizations

## 📜 License
This project is licensed under the **MIT License** - see [LICENSE.txt](LICENSE.txt) for details.

## 🏗️ Repository Structure
```
canada-service-prices/
├── analysis/                # Jupyter notebook + static visuals
├── dashboard/               # Interactive web app
├── data/                    # Raw and processed datasets
├── LICENSE.txt              # MIT License terms
└── README.md
```

## 🔍 Key Insights
1. **Regional Variations**
   - Quebec & BC: Highest increases (+35-38 pts) from mega-projects
   - Atlantic Region: Architectural services spike (+36.7)
   - Ontario/Prairies: Most stable growth patterns

2. **Service Differences**  
   ![Heatmap](analysis/figures/price_change_heatmap.png)

## 🚀 Getting Started
### 1. Reproduce Analysis
```bash
conda env create -f environment.yml
jupyter notebook analysis/analysis.ipynb
```

### 2. Run Dashboard
```bash
cd dashboard
pip install -r requirements.txt
python app.py
```
Access at: `http://localhost:8050`

## 🛠️ Technical Stack
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Missingno
- **Dashboard**: Plotly Dash, GeoPandas

## 📊 Data Source
[Statistics Canada - Architectural, Engineering and Related Services Price Index](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810016401)  
*(CANSIM Table 18-10-0164-01, 2018-2024)*

---

**Note**: Project focuses on observable trends rather than predictive modeling due to economic volatility.
