# Product Requirements Document (PRD)
## Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

### 1. Project Overview
A hybrid application designed to visualize and analyze chemical equipment data. The system consists of a central Django backend with two frontends: a React-based web interface and a PyQt5-based desktop application. Both interfaces allow users to upload CSV data, view statistics, visualize parameters, and generate reports.

### 2. Architecture
- **Architecture Style**: Client-Server
- **Backend**: Python (Django + DRF) - Serves REST APIs.
- **Frontend Web**: React.js - Consumes APIs, renders UI in browser.
- **Frontend Desktop**: Python (PyQt5) - Consumes APIs, renders native UI.
- **Database**: SQLite - Stores user data and historical datasets.
- **Processing**: Pandas - Data ingestion and analytics.

### 3. Functional Requirements

#### 3.1 Authentication
- Basic User Authentication (Login/Logout).
- *Web*: JWT or Session-based auth.
- *Desktop*: Token-based auth stored in session.

#### 3.2 Data Management (CSV Upload)
- Users can upload `sample_equipment_data.csv` compatible files.
- **Backend Validation**: Check columns [Equipment Name, Type, Flowrate, Pressure, Temperature].
- **Storage**: Store the raw CSV file or parsed data in SQLite.
- **History**: Maintain only the last 5 uploaded datasets per user or globally (as per simple requirements). *Constraint: "Store last 5 uploaded datasets"* - Likely implies a rolling window of 5 recent uploads.

#### 3.3 Analytics & Visualization
- **Summary Statistics**:
  - Total count of equipment.
  - Average Flowrate, Pressure, Temperature.
  - Distribution of Equipment Types (Count per Type).
- **Visualization**:
  - *Web (Chart.js)*: Bar chart (Type distribution), Line/Scatter charts (if applicable for correlations).
  - *Desktop (Matplotlib)*: Similar plots embedded in the GUI.

#### 3.4 Reporting
- Generate a PDF report summarizing the statistics and potentially including snapshot images of charts.

### 4. Layer-by-Layer Specifications

#### 4.1 Backend Layer (Django + DRF)
- **Project Name**: `equipment_backend`
- **Apps**: `analytics`, `accounts`
- **Models**:
  - `Dataset`: `id`, user (FK), file_path, uploaded_at. (Limit logic needed here)
  - `Equipment`: `id`, dataset (FK), name, type, flowrate, pressure, temperature.
- **APIs**:
  - `POST /api/auth/login/`: User login.
  - `POST /api/upload/`: Multipart upload of CSV. Parsing happens synchronously or async. Returns ID.
  - `GET /api/datasets/`: List last 5 datasets.
  - `GET /api/datasets/{id}/stats/`: JSON response with averages, counts.
  - `GET /api/datasets/{id}/data/`: JSON list of actual records for tables.
  - `GET /api/datasets/{id}/report/`: Download generated PDF.

#### 4.2 Frontend Web Layer (React.js)
- **Tech**: Vite + React, Chart.js (`react-chartjs-2`), Axios, TailwindCSS (for "Rich Aesthetics").
- **Pages**:
  - `LoginPage`: Simple form.
  - `Dashboard`:
    - Upload Component (Drag & Drop or File Select).
    - Recent Uploads List (Sidebar or Top bar).
    - Stats Cards (Total, Averages).
    - Charts Section (Bar Chart for Types).
    - Data Table (Paginated list of equipment).
    - "Download PDF" button.

#### 4.3 Frontend Desktop Layer (PyQt5)
- **Tech**: PyQt5, `matplotlib` (backend_qt5agg), `requests`.
- **Windows**:
  - `LoginWindow`: Username/Password input.
  - `MainWindow`:
    - Menu/Toolbar: Upload CSV, Refresh.
    - Sidebar: Last 5 datasets list.
    - Central Widget: Tabbed view or Split view.
      - *Summary Tab*: Text labels for stats, embedded Matplotlib Canvas for charts.
      - *Data Tab*: `QTableWidget` to show raw data.
      - *Actions*: Button to trigger PDF download (opens in default viewer or saves to disk).

### 5. Non-Functional Requirements
- **Performance**: Parsing logic should handle sample size efficienty (Pandas is sufficient).
- **UI/UX**:
  - Web: Modern, responsive, "Premium" feel (gradients, shadows, hover effects).
  - Desktop: Clean, native look, responsive to window resizing.
- **Security**: Validate CSV inputs to prevent arbitrary code execution or bad data.

### 6. Implementation Strategy
1.  **Backend Core**: Setup Django, Models, and basic Views.
2.  **Web Basic**: Setup React, Connect Login, Connect Upload.
3.  **Analysis Logic**: Implement Pandas processing and Stats API.
4.  **Web Viz**: Implement Charts and Tables.
5.  **Desktop Core**: Setup PyQt5, Login, and API Client class.
6.  **Desktop Viz**: Implement Matplotlib integration and data tables.
7.  **Polish**: PDF generation, UI styling, and cleanup.
