# Pedestrian Consulting Project

## Project Summary

This project seeks to quantify the reduction in pedestrian risk that is expected to result from the installation of traffic calming measures being installed on two intersections on the main road of Granby Colorado. 

This repository contains:
  - An interactive web application containing our reported findings and various interactive tools that empower method exploration. 
  - All of the notes taken during the project development process.

Initial reporting that kicked off this project were provided by the engineering firm SGM. 

## Contacts and Ownership

**Brady Lamson:** `brady.lamson@ucdenver.edu`

**Davyd Sadovskyy:** `davyd.2.sadovskyy@cuanschutz.edu`

## Streamlit Web Application

The Streamlit application serves as both a reporting interface and an interactive analysis tool for the Granby Pedestrian Consulting Project. It combines methodological documentation with real-time risk estimation, allowing users to move seamlessly between explanation and exploration.

This application is deployed live on streamlit. The link can be found below.

- [WEB APPLICATION LINK](https://granby-pedestrian-safety-project.streamlit.app/)

---

### Application Structure

The app is organized into three primary sections:

#### 1. Main Page

* Provides a high-level overview of the project, its objectives, and how to navigate the tool.

#### 2. Methodology and Results

A structured walkthrough of the modeling framework and findings:

* **Background** – Context and motivation for the analysis
* **HSM Framework** – Overview of the Highway Safety Manual approach
* **Safety Performance Functions (SPFs)** – Base crash frequency models
* **Crash Modification Factors (CMFs)** – Adjustments for treatments and conditions
* **Data Acquisition** – Sources and preprocessing steps
* **Results** – Key outputs and interpretations
* **Limitations** – Model assumptions and constraints

This section is intended to make the modeling pipeline transparent and interpretable, particularly for stakeholders who want to understand how estimates are generated.

#### 3. Interactive Tools

A set of pages for scenario analysis and simulation:

* **📊 Accident Rates**
  Computes expected annual crash rates based on current inputs.

* **📊 Long Term Risk**
  Translates annual rates into multi-year risk, helping contextualize low-probability events over longer horizons.

* **🎲 Simulation**
  Runs stochastic simulations to generate distributions of possible crash outcomes over a fixed time period.

* **🎲 Bulk Simulation**
  Extends simulation to multiple scenarios simultaneously, enabling direct comparison across configurations.

---

### Key Features

* **Dynamic Sidebar Controls**
  Users can modify traffic volumes, intersection characteristics, and treatment assumptions. Changes propagate immediately through all computations.

* **Scenario-Based Analysis**
  The app supports evaluating multiple configurations, including cases where a single intersection is modeled under different structural assumptions.

* **Deterministic + Stochastic Outputs**

  * Deterministic: Expected crash rates derived from SPFs and CMFs
  * Stochastic: Simulated distributions capturing variability and uncertainty

* **Integrated Visualization**
  Outputs are presented via interactive plots and tables, emphasizing:

  * Comparisons across scenarios
  * Sensitivity to input parameters
  * Distributional behavior over time

---

### Design Notes

* **Separation of Concerns**
  The application is modular, with clear separation between:

  * Input handling (sidebar components)
  * Risk estimation logic
  * Visualization utilities

* **State Management**
  Uses `st.session_state` to maintain consistency across pages and user interactions.

* **Intended Use**
  This tool is designed for exploratory and decision-support purposes. Outputs reflect model assumptions and should not be interpreted as precise forecasts, but rather as structured estimates under the HSM framework.


## Repository Layout and Navigation

- **`app_pages`** - Contains each of the pages of the streamlit application. 
- **`data/`** - For all data files. 
- **`docs/`** - Documents used to support the project. Files, notes, images, etc. 
- **`eda/`** - For exploratory work and miscellaneous notebooks. Initial variable selection and modeling may also go here. Really think of this as an exploratory directory. We do messy analysis and find solutions here.
- **`src/`** - Code used for core functionality of the project. Broken up into sub-directories by type of tool.
  - **`excel/`** - Contains the excel tool provided by HSM that gave us our initial results. 
  - **`r/`** - Old code used for initial result automation. All code has been ported to Python.
  - **`risk_estimation`** - All source code for the web application, written in Python. Has multiple sub-modules dedicated to different aspects of the applications creation. 

## Tech Stack Used

### Python

- **Python**: `>=3.12,<4.0`
- **Dependency Management**: Poetry  
- **Core Libraries**:
  - `streamlit` — interactive UI
  - `polars` — data manipulation
  - `plotly` — visualization
  - `scipy` — statistical methods
  - `sympy` — symbolic computation
  - `loguru` — logging

### R

All of the web application code runs on pyhon, but some older eda code uses the following:

- **R version**: 4.5.1
- **Dependency Management**: N/A
- **R Packages used**:
    - `dplyr`
    - `tidyr`
    - `readr`
    - `ggplot2`
    - `ggrepel` 

---

## Application Setup With Poetry

### Setup

This project uses `poetry` and requires Python 3.12.

#### 1. Install Python 3.12

Required version (from `.python-version`):
```bash
cat .python-version
# 3.12.2
```

Install with pyenv (recommended):
```bash
brew install pyenv  # macOS

pyenv install 3.12.2
pyenv local 3.12.2
```

Verify:
```bash
python --version
# Should be 3.12.x
```

---

#### 2. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify:
```bash
poetry --version
```

If not found:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

#### 3. Install dependencies

```bash
poetry config virtualenvs.in-project true
poetry install
```

---

#### 4. Run the streamlit application

```bash
poetry run streamlit run Main_Page.py
```

---

### Notes

- Python is recommended to be **3.12.x** (3.13 may breeak dependencies)
- Virtual environment is created in `.venv/`
- `poetry.lock` ensures reproducible installs — commit it and don’t modify manually
- If Poetry picks the wrong Python:
  ```bash
  poetry env use $(pyenv which python)
  ```

- If you see build issues with `scipy`, ensure system build tools are installed (e.g., Xcode CLI tools on macOS):
  ```bash
  xcode-select --install
  ```