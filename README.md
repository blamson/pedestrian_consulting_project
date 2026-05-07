# Pedestrian Consulting Project

## Project Summary

This project seeks to quantify the reduction in pedestrian risk that is expected to result from the installation of traffic calming measures being installed on two intersections on the main road of Granby Colorado. 

This repository contains a plethora of notes on how to answer this question while following Federal Highway Administration (FHWA) guidelines. 

Initial reporting that kicked off this project were provided by the engineering firm SGM. 

## Contacts and Ownership

**Brady Lamson:** `brady.lamson@ucdenver.edu`

**Davyd Sadovskyy:** `davyd.2.sadovskyy@cuanschutz.edu`

## Repository Layout and Navigation

- **`src/`** - Code used for key output in the project. Taken from `eda/` once work in that directory is complete.  
- **`data/`** - For all data files. 
- **`eda/`** - For exploratory work and miscellaneous notebooks. Initial variable selection and modeling may also go here. Really think of this as an exploratory directory. We do analysis and find solutions here.
- **`docs/`** - Documents used to support the project. Files, notes, images, etc. 

## Tech Stack Used

Most of this directory is simply markdown notes and images, though some code was used for generating results and plots.

- R version used: 4.5.1
- R Packages used:
    - `dplyr`
    - `tidyr`
    - `readr`
    - `ggplot2`
    - `ggrepel` 

# Repository Setup With Poetry

## Setup

This project uses `poetry` and requires Python 3.12.

### 1. Install Python 3.12

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

### 2. Install Poetry

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

### 3. Install dependencies

```bash
poetry config virtualenvs.in-project true
poetry install
```

---

### 4. Run the app (Streamlit)

```bash
poetry run streamlit run <your_app_file>.py
```

---

## Notes

- Python must be **3.12.x** (3.13 will likely break dependencies)
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