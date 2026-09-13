# GrowPilot — Intelligent Smart Agriculture & Farm Management System
### Comprehensive Technical Architecture, System Design & Operational Guide

---

## 1. Why I Built This Project (Motivation & Problem Statement)

### The Real-World Problem
Modern farm management and agricultural operations are frequently hindered by fragmented workflows, disjointed record-keeping, and intuition-based decision-making:
- **Disjointed Context & Paper Trails:** Farm managers often maintain agricultural records across scattered paper logbooks, disjointed Excel spreadsheets, and isolated messaging apps. Tracking worker shifts, salaries, supplier invoices, and inventory quantities across separate silos leads to inventory shrinkage, missed supplier payments, and lost data.
- **Intuition-Driven Rather Than Data-Driven Cultivation:** Deciding which crop to plant based solely on historical habit or guesswork often results in sub-optimal crop yields, soil nutrient depletion, and severe financial losses when soil chemistry (Nitrogen, Phosphorus, Potassium, pH) does not match the crop's physiological requirements.
- **Unpredictable Micro-Climates:** Weather volatility directly impacts planting, irrigation, and harvesting schedules. Without real-time, localized meteorological data embedded directly within the farm's operational workspace, growers cannot prepare for unexpected rainfall or temperature fluctuations.
- **Lack of Enterprise-Grade Data Integrity:** Minimum viable applications often use local file-based storage or hardcoded queries that lack transactional safety, concurrent user support, and enterprise schema enforcement.

### The Vision Behind GrowPilot
I built **GrowPilot** to deliver an **end-to-end, enterprise-ready Smart Agricultural ERP and Decision-Support System** that centralizes operations and empowers growers with data science:
- **Centralized Workforce & Operations Management:** A unified employee management hub tracking employment types, work shifts, agricultural specialties, contact info, and payroll.
- **Complete Supply Chain & Inventory Control:** Real-time tracking of item categories, products, stock status (In Stock / Out of Stock / Low Stock), and supplier invoicing.
- **Machine Learning Crop Recommendation Engine:** A trained Random Forest model that analyzes 7 distinct agro-climatic parameters ($N, P, K$, temperature, humidity, pH, rainfall) to scientifically recommend the highest-yielding crop.
- **Real-Time Meteorological Intelligence:** Live satellite and meteorological forecasts integrated directly into the workspace via OpenWeatherMap API.
- **Enterprise PostgreSQL 18 Architecture:** A robust relational backend built with `psycopg`, connection pooling, automated database/schema initialization, and transaction-safe operations.

---

## 2. What We've Built and Why (Current Project Overview)

GrowPilot is a desktop-native agricultural enterprise application designed with high visual clarity and rock-solid relational persistence:
1. **Relational Database Core (PostgreSQL 18):** Powered by `psycopg` (v3) with a dedicated compatibility and connection-pooling wrapper ([`db.py`](db.py)) that provides cross-platform transactional reliability and schema isolation.
2. **Predictive Agronomy (Random Forest Classifier):** A trained Machine Learning pipeline ([`prediction.py`](prediction.py)) built on `scikit-learn` and `joblib` capable of recommending optimal crops from soil and climatic vectors with a self-healing fallback that automatically retrains if model version mismatches occur.
3. **Live Weather Micro-Interface ([`weather.py`](weather.py)):** An asynchronous meteorological console querying real-time atmospheric telemetry (temperature, wind, humidity, pressure).
4. **Supply Chain & Inventory Management ([`products.py`](products.py), [`supplier.py`](supplier.py), [`category.py`](category.py)):** Full lifecycle tracking from supplier invoices to catalog categorization and stock adjustments.
5. **Human Resources & Workforce Directory ([`employees.py`](employees.py)):** Comprehensive staff records with filtering, search by multiple attributes, and date pickers powered by `tkcalendar`.
6. **Authentication & Session Security ([`signin.py`](signin.py), [`signup.py`](signup.py)):** User registration, password reset workflows, and credential verification against PostgreSQL.

```
+-----------------------------------------------------------------------------------+
|                                 GROWPILOT GUI LAYER                               |
|                  Tkinter & ttk High-Performance Desktop Interface                 |
+----------------------------------------+------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            AUTHENTICATION & SECURITY                              |
|   - signin.py / signup.py                                                         |
|   - Validates user credentials against PostgreSQL user_signin_details             |
|   - Password reset workflow with username verification                            |
+----------------------------------------+------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             CENTRAL DASHBOARD ROUTER                              |
|   - Real-time statistics counters (Employees, Suppliers, Categories, Products)    |
|   - Dynamic clock & date telemetry                                                |
+----+-------------------+-------------------+------------------+-------------------+
     |                   |                   |                  |                   |
     v                   v                   v                  v                   v
+------------+     +-------------+     +------------+     +------------+     +-------------+
| EMPLOYEES  |     |  SUPPLIERS  |     | CATEGORIES |     |  PRODUCTS  |     |  WEATHER &  |
| MANAGEMENT |     | INVOICING   |     | MANAGEMENT |     | INVENTORY  |     | ML CROP REC |
|            |     |             |     |            |     |            |     |             |
| employees  |     | supplier.py |     |category.py |     |products.py |     | weather.py  |
|    .py     |     |             |     |            |     |            |     |prediction.py|
+-----+------+     +------+------+     +-----+------+     +-----+------+     +------+------+
      |                   |                  |                  |                   |
      +-------------------+------------------+------------------+                   |
                          |                                                         |
                          v                                                         v
+----------------------------------------------------+            +---------------------------------+
|              DATABASE WRAPPER (db.py)              |            |       SCIKIT-LEARN ML ENGINE    |
|  - psycopg connection management                   |            |  - model.pkl (Random Forest)    |
|  - PgCursorWrapper & PgConnectionWrapper           |            |  - Crop_recommendation.csv      |
|  - Parameter sequence normalization                |            |  - Self-healing auto-retraining |
+-------------------------+--------------------------+            +---------------------------------+
                          |
                          v
+-----------------------------------------------------------------------------------+
|                         ENTERPRISE POSTGRESQL 18 SERVER                           |
|   - Database: inventory (localhost:5432)                                          |
|   - Tables: user_signin_details, employee_data, supplier_data,                    |
|             product_data, category_data                                           |
+-----------------------------------------------------------------------------------+
```

---

## 3. Contents & File-by-File Technical Breakdown

| File / Directory | Purpose & Technical Role |
| :--- | :--- |
| **`signin.py`** | **Application Authentication Entrypoint.** Provides the graphical login console with password visibility toggles, input placeholder handling, account creation navigation, and a secure password recovery modal. Validates credentials directly against PostgreSQL. |
| **`signup.py`** | **User Registration Window.** Captures new user credentials (email, username, password) with password confirmation verification, checks for existing usernames, and registers authorized users into the PostgreSQL database. |
| **`dashboard.py`** | **Central Command Hub & Navigation Orchestrator.** Manages the persistent application frame, runs real-time aggregation queries against PostgreSQL to display live KPI counts (total employees, suppliers, categories, products), displays an updating system clock, and swaps form views dynamically. |
| **`employees.py`** | **Human Resources & Workforce Management.** Full-featured CRUD console for farm staff. Integrates `tkcalendar.DateEntry` for birth and joining dates, multi-field search (`Name`, `EmpID`, `FarmRole`, `Work_shift`, `MainCrop`), tabular data display with `ttk.Treeview`, and input sanitization. |
| **`products.py`** | **Inventory & Stock Management.** Manages agricultural commodities, tools, and seeds. Features dynamic combobox population for categories and suppliers directly from PostgreSQL, stock status tracking (`In Stock`, `Out of Stock`), pricing, and quantity adjustments. |
| **`supplier.py`** | **Supply Chain & Invoicing Directory.** Manages agricultural vendors and wholesalers. Stores invoice numbers, business names, contact details, physical addresses, and order descriptions with transactional edit and delete features. |
| **`category.py`** | **Product Categorization Module.** Establishes taxonomic classifications (e.g., *Grains, Fertilizers, Machinery, Seeds*) to maintain organized product catalogs and prevent unclassified inventory. |
| **`prediction.py`** | **Machine Learning Crop Recommendation Engine.** Loads a pre-trained `RandomForestClassifier` to recommend optimal crops based on 7 inputs: Nitrogen ($N$), Phosphorus ($P$), Potassium ($K$), Temperature, Humidity, Soil pH, and Rainfall. Includes a self-healing fallback that retrains on `Crop_recommendation.csv` if environment or serialization discrepancies occur. |
| **`weather.py`** | **Real-Time Meteorological Forecast Console.** Queries the OpenWeatherMap REST API to retrieve real-time atmospheric conditions (temperature in °C, weather description, wind speed, relative humidity, and pressure). Built with a clean two-panel visual layout. |
| **`setup_db.py`** | **Automated PostgreSQL Schema Initializer.** Connects to PostgreSQL, idempotently creates the `inventory` database if not present, generates all 5 relational tables with proper data types and primary keys, and seeds the default administrative account (`admin` / `admin`). |
| **`db.py`** | **Centralized Database Layer & Compatibility Wrapper.** Implements `connect_database()` using `psycopg` (v3). Wraps connections and cursors in `PgConnectionWrapper` and `PgCursorWrapper` to normalize query parameters, handle sequence conversion, and maintain clean database connectivity across all GUI forms. |
| **`model.pkl`** | **Serialized Machine Learning Model.** Pipelined and persisted Random Forest Classifier trained on agronomic soil and weather features for instant crop recommendations. |
| **`Crop_recommendation.csv`** | **Agricultural Training Dataset.** Verified dataset containing 2,200+ multi-parameter agricultural data points mapping chemical and climatic conditions to 22 distinct crop varieties. |
| **`run.bat`** | **One-Click Windows Launcher.** Batch script that launches the GrowPilot desktop client (`python signin.py`) directly from Windows Explorer. |
| **`requirements.txt`** | **Pinned Python Dependencies.** Specifies required packages: `psycopg`, `pillow`, `tkcalendar`, `scikit-learn`, `joblib`, `pandas`, `numpy`, and `requests`. |
| **`images/`** | **UI Graphical Assets.** Contains application icons, navigation buttons, illustrations, and logos used across the desktop interface. |

---

## 4. Enterprise Database Architecture & PostgreSQL Schema Reference

### Why PostgreSQL 18?
GrowPilot utilizes **PostgreSQL 18** as its relational storage engine for several key advantages:
- **ACID Compliance & Reliability:** Strong transactional guarantees ensure that operations like deleting a supplier or updating stock quantities never leave the database in an inconsistent state.
- **Enterprise Concurrency:** Multi-Version Concurrency Control (MVCC) allows simultaneous reading and updating across different administrative terminals.
- **Strict Data Types:** Native support for `NUMERIC(10,2)` for financial salaries and product prices prevents floating-point rounding errors.

### The Database Abstraction Layer (`db.py`)
To prevent tight coupling between GUI forms and the underlying database driver, [`db.py`](db.py) introduces custom wrappers:
- **`PgCursorWrapper`**: Intercepts queries, gracefully handles PostgreSQL connection semantics, and automatically normalizes single scalar arguments (e.g. `cursor.execute(query, emp_id)`) into tuples `(emp_id,)` to comply with `psycopg` sequence requirements.
- **`PgConnectionWrapper`**: Wraps the PostgreSQL connection to provide standard `.cursor()`, `.commit()`, and `.rollback()` semantics.

### Relational Schema Reference

#### 1. `user_signin_details` (Authentication Accounts)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **`id`** | `SERIAL` | `PRIMARY KEY` | Unique autoincrementing account ID |
| **`email`** | `VARCHAR(100)` | | Registered user email address |
| **`username`** | `VARCHAR(70)` | `NOT NULL` | Unique sign-in username |
| **`password`** | `VARCHAR(40)` | `NOT NULL` | User password credential |

#### 2. `employee_data` (Workforce & Human Resources)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **`empid`** | `INT` | `PRIMARY KEY` | Unique Employee ID |
| **`name`** | `VARCHAR(75)` | | Full employee name |
| **`farmrole`** | `VARCHAR(100)` | | Farm assignment (e.g., *Field Manager, Agronomist*) |
| **`gender`** | `VARCHAR(15)` | | Gender identity |
| **`dob`** | `VARCHAR(10)` | | Date of Birth (`DD/MM/YYYY`) |
| **`contact`** | `VARCHAR(20)` | | Phone number |
| **`employement_type`** | `VARCHAR(50)` | | *Fulltime, Parttime, Contract, Seasonal, Internship* |
| **`education`** | `VARCHAR(40)` | | Educational qualification |
| **`work_shift`** | `VARCHAR(50)` | | Shift schedule (*Morning, Afternoon, Evening, Night*) |
| **`address`** | `VARCHAR(100)` | | Residential address |
| **`doj`** | `VARCHAR(30)` | | Date of Joining (`DD/MM/YYYY`) |
| **`salary`** | `NUMERIC(10,2)` | | Monthly compensation |
| **`usertype`** | `VARCHAR(30)` | | Access permission level (*Admin, Employee*) |
| **`maincrop`** | `VARCHAR(100)` | | Primary crop focus |

#### 3. `supplier_data` (Vendor Registry & Invoicing)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **`invoice`** | `INT` | `PRIMARY KEY` | Unique invoice or vendor account ID |
| **`name`** | `VARCHAR(50)` | | Supplier company or individual name |
| **`contact`** | `VARCHAR(15)` | | Telephone or contact line |
| **`address`** | `VARCHAR(100)` | | Business location or warehouse address |
| **`description`** | `TEXT` | | Supplier terms, commodities provided, notes |

#### 4. `product_data` (Inventory & Stock Catalog)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **`id`** | `SERIAL` | `PRIMARY KEY` | Autoincrementing product SKU ID |
| **`category`** | `VARCHAR(100)` | | Linked category classification |
| **`supplier`** | `VARCHAR(100)` | | Linked supplier vendor |
| **`name`** | `VARCHAR(100)` | | Commercial product / seed / tool name |
| **`price`** | `NUMERIC(12,2)` | | Unit price in local currency |
| **`quantity`** | `INT` | | Current warehouse stock count |
| **`status`** | `VARCHAR(50)` | | Stock availability (*In Stock, Out of Stock, Low Stock*) |

#### 5. `category_data` (Taxonomy & Organization)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **`id`** | `INT` | `PRIMARY KEY` | Category identifier |
| **`name`** | `VARCHAR(50)` | | Category name (*Grains, Fertilizers, Machinery, Seeds*) |
| **`description`** | `TEXT` | | Description of categorized items |

---

## 5. Machine Learning & Predictive Analytics Engine

### Crop Recommendation Architecture
GrowPilot incorporates a production-ready Machine Learning model designed to eliminate guesswork from crop selection. The system takes into account soil chemistry and climatic readings:

$$\mathbf{x} = \begin{bmatrix} N & P & K & \text{Temperature} & \text{Humidity} & \text{pH} & \text{Rainfall} \end{bmatrix}^T$$

- **Input Features ($7$ Parameters):**
  1. **Nitrogen ($N$):** Soil Nitrogen content ratio (mg/kg).
  2. **Phosphorus ($P$):** Soil Phosphorus content ratio (mg/kg).
  3. **Potassium ($K$):** Soil Potassium content ratio (mg/kg).
  4. **Temperature:** Ambient temperature in degrees Celsius (°C).
  5. **Humidity:** Relative atmospheric humidity percentage (%).
  6. **pH:** Soil acidity/alkalinity level (scale $0.0 - 14.0$).
  7. **Rainfall:** Precipitation rate (mm).

- **Classifier:** `RandomForestClassifier(n_estimators=200, random_state=42)` trained on [`Crop_recommendation.csv`](Crop_recommendation.csv).
- **Target Classes ($22$ Varieties):** Recommends crops including *Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, and Coffee*.

### Self-Healing Model Fallback
In multi-environment deployments, deserializing Python `.pkl` models with different `scikit-learn` versions can cause `InconsistentVersionWarning` or unpickling failures. GrowPilot implements a self-healing fallback in [`prediction.py`](prediction.py):
```python
def _load_or_train_model():
    try:
        return joblib.load("model.pkl")
    except Exception:
        # Automatically retrain on the active environment
        df = pd.read_csv("Crop_recommendation.csv")
        X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
        y = df["label"]
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        joblib.dump(model, "model.pkl")
        return model
```
This ensures zero runtime crashes even when upgrading Python or machine learning libraries.

---

## 6. Real-Time Meteorological Intelligence

The [`weather.py`](weather.py) module provides real-time climate monitoring directly inside the desktop client:
- **API Provider:** OpenWeatherMap API.
- **Two-Panel Responsive Layout:**
  - **Left Panel:** Graphical weather illustration and branding.
  - **Right Panel:** Interactive city query entry and live atmospheric readouts.
- **Telemetry Displayed:**
  - **Temperature:** Real-time reading with dynamic unit formatting (°C).
  - **Condition:** Weather condition descriptor (*Clear, Rain, Clouds, Mist*).
  - **Wind Speed:** Atmospheric wind velocity (km/h).
  - **Humidity:** Relative moisture saturation percentage (%).
  - **Pressure:** Atmospheric pressure (hPa).
  - **Local Clock:** Synchronized local time for the requested city.

---

## 7. Step-by-Step Local Setup & Execution Guide

Follow these steps to run GrowPilot on your local environment:

### Step 1: System Prerequisites
- **Operating System:** Windows 10/11, macOS, or Linux.
- **Python:** Python 3.10 to 3.13 installed.
- **Database:** PostgreSQL Server (v14 or higher, PostgreSQL 18 recommended) installed and running locally on port `5432`.

### Step 2: Clone the Repository
```bash
git clone https://github.com/Neelendra-Mishra/Grow_Pilot.git
cd Grow_Pilot
```

### Step 3: Set Up a Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
Install all required libraries using the pinned requirements file:
```bash
pip install -r requirements.txt
```

### Step 5: Configure PostgreSQL Credentials
Open [`db.py`](db.py) and update your PostgreSQL credentials if different from the default:
```python
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'YOUR_POSTGRES_PASSWORD'
DB_NAME = 'inventory'
```

### Step 6: Initialize the Database & Tables
Run the automated initialization script:
```bash
python setup_db.py
```
*Expected output:*
```text
Created PostgreSQL database 'inventory'.
Default admin user created ('admin' / 'admin').
Database setup complete. All PostgreSQL tables verified successfully.
```

### Step 7: Launch the GrowPilot Application
Run the main sign-in script:
```bash
python signin.py
```
*(Or on Windows, double-click [`run.bat`](run.bat))*

### Step 8: Default Log-in Credentials
Upon initial setup, log in with the default administrative credentials:
- **Username:** `admin`
- **Password:** `admin`

---

## 8. Database Administration with pgAdmin 4

GrowPilot's data is stored in standard relational tables that can be viewed, queried, and backed up using **pgAdmin 4**:

1. **Launch pgAdmin 4:**
   - Search for **pgAdmin 4** in the Windows Start Menu, or run:
     ```text
     C:\Program Files\PostgreSQL\18\pgAdmin 4\runtime\pgAdmin4.exe
     ```
2. **Connect to Your Server:**
   - In the left sidebar tree, click **Servers** → **PostgreSQL 18** and enter your master password.
3. **Inspect the Tables:**
   - Navigate to:
     ```text
     Servers -> PostgreSQL 18 -> Databases -> inventory -> Schemas -> public -> Tables
     ```
   - You will see:
     - `category_data`
     - `employee_data`
     - `product_data`
     - `supplier_data`
     - `user_signin_details`
4. **Browse & Edit Rows:**
   - Right-click any table (e.g. `employee_data`) and select **View/Edit Data** → **All Rows** to inspect live records in a spreadsheet format.

---

## 9. Future Roadmap & Extensibility

- [ ] **Automated PDF Invoicing:** Export professional invoice and salary receipts using ReportLab.
- [ ] **IoT Soil Sensor Telemetry:** Direct MQTT integration with ESP32 / Arduino soil moisture probes.
- [ ] **Barcode & QR Scanning:** Fast stock scanning using OpenCV and webcams for warehouse inventory check-in/check-out.
- [ ] **Role-Based Access Control (RBAC):** Restrict standard employee logins to viewing their personal schedules and tasks while locking financial settings to administrators.
- [ ] **Multi-Farm Tenancy:** Support managing multiple farm locations from a single centralized dashboard.

---

## 10. Author & License

- **Developer:** [Neelendra Mishra](https://github.com/Neelendra-Mishra)
- **Repository:** [Grow_Pilot on GitHub](https://github.com/Neelendra-Mishra/Grow_Pilot)
- **License:** Open Source for educational and agricultural innovation purposes.
