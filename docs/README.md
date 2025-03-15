# Parking Logs in Guanajuato

## Installing

Requires git, chrome, python and pip installed.

1. clone this repo

```bash
git clone https://github.com/L4rralde/Parking_Lots.git
cd Parking_Lots
```

2. Create venv

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install python packages

```bash
pip install -r requirements.txt
```

## How to use

- Run scrapper

```bash
python src/main.py
```

- Update data

```bash
python src/update_data.py
```

FUTURE: Automate calling the script above.
