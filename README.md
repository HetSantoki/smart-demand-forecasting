# Smart Demand Forecasting

![GitHub License](https://img.shields.io/github/license/yourusername/Smart-Demand-Forecasting)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

## 📄 Overview

The **Smart Demand Forecasting** project provides a Django‑based web application for forecasting product demand using time‑series analysis and machine learning models. It includes:

- A RESTful API for uploading historical sales data.
- Interactive dashboards built with Django templates and Chart.js visualizations.
- A configurable pipeline that supports multiple forecasting algorithms (ARIMA, Prophet, LSTM, etc.).
- Docker‑compose setup for easy local development and deployment.

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js** (for front‑end asset compilation)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Smart-Demand-Forecasting.git
   cd Smart-Demand-Forecasting
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Copy the example file and edit as needed:
   ```bash
   cp .env.example .env
   # Edit .env to set DATABASE_URL, SECRET_KEY, etc.
   ```

## 📂 Project Structure

```
Smart Demand Forecasting/
├─ forecast_project/            # Django project root
│   ├─ forecast_project/        # Settings module
│   ├─ dashboard/               # Dashboard app (views, urls, utils)
│   ├─ manage.py                # Django CLI entry point
│   └─ requirements.txt         # Python dependencies
├─ data/                        # Sample data and CSV uploads
│   ├─ cleaned_transactions.csv
│   ├─ daily_demand.csv
│   └─ data.csv
├─ Models/                        # Sample data and CSV uploads
│   ├─ demand_pipeline.pkl
│   └─ feature_cols.pkl
├─ .gitignore
├─ README.md    
└─ requirements.txt           # Project overview (this file)
```

This layout helps you navigate the codebase and locate key components.

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Open <http://127.0.0.1:8000> in your browser.

### Docker (Optional)

```bash
docker-compose up --build
```

The app will be available at <http://localhost:8000>.

## 📊 Usage

- **Upload Data**: Navigate to `/upload/` to import CSV files containing historical sales.
- **Configure Forecast**: Use the `/forecast/` page to select a model, horizon, and parameters.
- **View Results**: Interactive charts show actual vs. predicted demand, confidence intervals, and error metrics.

## 🧪 Testing

```bash
python manage.py test
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure all tests pass (`python manage.py test`).
5. Submit a Pull Request.
