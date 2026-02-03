# Frontend Architecture & UI Documentation
**Project**: Chemical Equipment Visualizer (Web Frontend)

## Overview
This document outlines the current structure, components, and logic of the React frontend. The goal is to redesign the UI for a premium, modern aesthetic without altering the core functionality or API integrations.

---

## 1. Technical Context
- **Framework**: React 18 + Vite
- **Styling**: Vanilla CSS (currently using BEM-like naming)
- **State Management**: React Context API (`AuthContext`)
- **Routing**: `react-router-dom` (Protected & Public routes)
- **HTTP Client**: Axios (configured in `api.js` with interceptors)

---

## 2. Core Logic & API (DO NOT CHANGE)
The following files handle the application logic and must be preserved or conceptually maintained:

### `src/services/api.js`
- **Base URL**: `/api` (proxied to Django backend)
- **Auth**: Stores/Retrieves JWT token from `localStorage`
- **Endpoints**:
  - `authAPI`: login, register, logout, profile
  - `datasetAPI`: list, upload, get stats, get equipment, download PDF

### `src/context/AuthContext.jsx`
- Manages global `user` state and `loading` status.
- Key functions: `login(username, password)`, `register(...)`, `logout()`.

---

## 3. Page Structure

### A. Login Page (`src/pages/Login.jsx`)
**Current Functionality**:
- Toggles between **Sign In** and **Sign Up** modes.
- Fields: Username, Password, Email (only in Sign Up).
- **Logic**: calls `login` or `register` from `useAuth`.

**Components to Style**:
- `.login-container`: Full-screen wrapper.
- `.login-card`: Main form container.
- Input fields with floating labels or distinct styles.
- Submit button with loading state (`isSubmitting`).
- Toggle button ("Don't have an account? Sign Up").

### B. Dashboard Page (`src/pages/Dashboard.jsx`)
**Current Layout**:
- **Sidebar**: Logo, Upload Dropzone, Recent Datasets List, User Profile (Logout).
- **Main Content**: Header, Stats Cards, Charts (Row), Data Table.

**State Variables**:
- `selectedDataset`: Objects { id, name, ... }
- `stats`: Object { total_count, avg_flowrate, ... }
- `equipment`: Array of equipment objects.

---

## 4. Component Breakdown (For UL Redesign)

### `UploadDropzone.jsx`
- **Props**: `onUpload` (function), `uploading` (boolean).
- **UI**: Needs a distinct "drag active" state and "loading" spinner.
- **Goal**: Make this look like a premium file upload area (glassmorphism/dashed border).

### `DatasetList.jsx`
- **Props**: `datasets` (array), `selected` (object), `onSelect` (function).
- **UI**: List of items in the sidebar. Needs clear "active" state styling.
- **Items**: Display Name, Date, and Item Count.

### `StatsCards.jsx`
- **Props**: `stats` (object).
- **UI**: Grid of 4 cards (Total, Flowrate, Pressure, Temp).
- **Goal**: Add icons, vibrant gradients, or sleek dark mode cards.

### `EquipmentChart.jsx`
- **Props**: `stats` (object).
- **Libraries**: `react-chartjs-2`.
- **UI**: Two charts currently (Bar & Doughnut).
- **Goal**: Style the container cards, chart colors, and legends to match the new theme.

### `EquipmentTable.jsx`
- **Props**: `equipment` (array).
- **UI**: Standard HTML `<table>`.
- **Goal**: Style rows, headers, and pagination (if added). Add hover effects and status badges for "Type".

---

## 5. Design Guidelines for AI
- **Theme**: Premium Dark Mode / Glassmorphism / Cyberpunk / Clean Corporate (Pick one).
- **Color Palette**: Use CSS variables for primary, secondary, and background colors.
- **Animations**: Add subtle entrance animations (framer-motion or CSS keyframes).
- **Responsiveness**: Ensure the sidebar collapses or adapts on mobile.
- **Icons**: Suggest using `lucide-react` or `react-icons` for a modern look.

## 6. Prompt for AI Generation
*To generate the new UI, provide the AI with the code for a specific component (e.g., `Login.jsx` and `Login.css`) and ask:*

> "Redesign this React component to look [Desired Style, e.g., Futuristic/Glassmorphism]. Keep the existing state logic, props, and event handlers exactly as they are. Only modify the JSX structure (classes/layout) and the CSS. Use standard CSS variables for colors."
