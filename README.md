# Chemical Equipment Parameter Visualizer

A hybrid web + desktop application for visualizing and analyzing chemical equipment data. Built for FOSSEE Intern Screening Task.

## Features

- **CSV Upload**: Upload equipment data files for analysis
- **Data Summary**: View total count, averages for flowrate, pressure, temperature
- **Visualization**: Interactive charts showing equipment type distribution
- **History Management**: Keeps track of last 5 uploaded datasets
- **PDF Reports**: Generate downloadable PDF reports
- **Authentication**: Basic user authentication system

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend (Web) | React.js + Chart.js | Interactive dashboard in browser |
| Frontend (Desktop) | PyQt5 + Matplotlib | Native desktop application |
| Backend | Django + Django REST Framework | REST API serving both frontends |
| Data Handling | Pandas | CSV parsing and analytics |
| Database | SQLite | Storing datasets and user data |

## Project Structure

```
fossee/
├── backend/                 # Django Backend
│   ├── core/               # Django project settings
│   ├── accounts/           # User authentication
│   ├── analytics/          # Data models and API views
│   └── requirements.txt
├── frontend-web/           # React Web Application
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Login and Dashboard pages
│   │   ├── context/       # Auth context
│   │   └── services/      # API client
│   └── package.json
├── frontend-desktop/       # PyQt5 Desktop Application
│   ├── main.py            # Entry point
│   ├── login_window.py    # Login UI
│   ├── dashboard_window.py # Main dashboard
│   ├── api_client.py      # Backend API client
│   └── requirements.txt
└── sample_equipment_data.csv  # Sample test data
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Web Frontend Setup

```bash
cd frontend-web

# Install dependencies
npm install

# Start development server
npm run dev
```

The web app will be available at `http://localhost:5173`

### Desktop Application Setup

```bash
cd frontend-desktop

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Getting Started

1. Start the Django backend server first
2. Launch either the web app or desktop application
3. Register a new account or login
4. Upload the `sample_equipment_data.csv` file
5. View statistics and charts
6. Download PDF report

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login user |
| POST | `/api/auth/logout/` | Logout user |
| GET | `/api/datasets/` | List datasets (last 5) |
| POST | `/api/datasets/` | Upload new CSV |
| GET | `/api/datasets/{id}/stats/` | Get dataset statistics |
| GET | `/api/datasets/{id}/equipment/` | Get equipment data |
| GET | `/api/datasets/{id}/report/` | Download PDF report |

## Sample Data Format

The CSV file should have the following columns:
- **Equipment Name**: Name/identifier of the equipment
- **Type**: Type of equipment (Reactor, Pump, Valve, etc.)
- **Flowrate**: Flow rate value (numeric)
- **Pressure**: Pressure value (numeric)
- **Temperature**: Temperature value (numeric)

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,5.2,85.0
Pump-P1,Pump,50.0,10.5,30.0
```

## Screenshots

### Web Application
- Modern dark theme with glassmorphism effects
- Interactive Chart.js visualizations
- Responsive sidebar with dataset list

### Desktop Application
- Native PyQt5 interface with dark theme
- Matplotlib charts for data visualization
- Drag-and-drop file upload support

## Demo Video

A 2-3 minute demo video showcasing:
1. User registration and login
2. CSV file upload
3. Dashboard visualization (both web and desktop)
4. PDF report generation

## Author

Built for FOSSEE Web + Desktop Application Screening Task

## License

MIT License
