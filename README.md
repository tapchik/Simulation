# Simulation

> This application allows to simulate people's behaviour based on their motives. 

## Instalation

1. Navigate to project folder "Simulation": 
    > `cd Simulation`
2. Using console, create virtual environment: 
    > `python -m venv .venv`
3. Activate virtual environment: 
    - On Windows: `.venv\Scripts\activate.bat`
    - In PowerShell: `.venv\Scripts\activate.ps1`
    - On Linux: `source .venv/bin/activate`
4. Install requirements into .venv: 
    > `pip install -r requirements.txt`

## Running

1. Go to Simulation folder
2. Activate virtual environment
3. Run Simulation interface: 
    > `python game.py`

## Roadmap

- [x] character.motives is a dictionary(key, motive) which allows to introduce unique key and friendly title
- [x] Performing an action takes time
- [ ] Ticks jump gradualy on high speed
- [ ] Interface shows how long till action ends
- [ ] Actions require resources (e.g. number of toilets, beds or computers available)