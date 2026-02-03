# Intern Screening Task – Hybrid Web + Desktop Application (Implementation Status)

## Project Overview
Create a Web + Desktop application that allows users to upload a CSV file containing a list of chemical equipment.

**Status**: ✅ **COMPLETED**

## Tech Stack (Fixed)

| Layer | Technology | Purpose | Status |
|-------|------------|---------|--------|
| **Frontend (Web)** | React.js + Chart.js | Show table + charts | ✅ **Implemented** |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Same visualization in desktop | ✅ **Implemented** |
| **Backend** | Python Django + DRF | Common backend API | ✅ **Implemented** |
| **Data Handling** | Pandas | Reading CSV & analytics | ✅ **Implemented** |
| **Database** | SQLite | Store last 5 uploaded datasets | ✅ **Implemented** |
| **Version Control** | Git & GitHub | Collaboration & submission | ✅ **Ready** |
| **Sample Data** | sample_equipment_data.csv | Sample CSV file provided | ✅ **Verified** |

## Key Features Required

1.  **CSV Upload**
    - [x] Web and Desktop must allow users to upload a CSV file to the backend.
    
2.  **Data Summary API**
    - [x] Django API should return total count, averages, and equipment type distribution.
    
3.  **Visualization**
    - [x] Display charts using Chart.js (Web).
    - [x] Display charts using Matplotlib (Desktop).
    
4.  **History Management**
    - [x] Store last 5 uploaded datasets with summary.
    
5.  **Additional Features**
    - [x] Generate PDF report.
    - [x] Add basic authentication.

6.  **Demo Data**
    - [x] Use the provided sample CSV (sample_equipment_data.csv) for demo and testing.

## Task Instructions
- [x] Develop both Web and Desktop frontends connected to the same Django backend.
- [x] Demonstrate proper data handling, API integration, and UI/UX consistency.

## Submission Guidelines
- [x] Source code (backend + both frontends)
- [x] README file with setup instructions
- [ ] Short demo video (2–3 minutes) - *To be done by user*
- [x] Optional: Deployment link for web version - *Local setup complete*
