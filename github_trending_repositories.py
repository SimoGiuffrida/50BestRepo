import requests
import datetime
import os
import time

# --- CONFIGURAZIONE ---
# Inserisci il tuo Personal Access Token (PAT) di GitHub qui per evitare limiti di richieste (Rate Limit).
# Puoi crearlo su: https://github.com/settings/tokens
GITHUB_TOKEN = '' 
NUM_REPOS = 50
DAYS_AGO = 7
# ----------------------

def get_trending_repos():
    """Recupera le top repo in base alle stelle ottenute di recente."""
    date_start = (datetime.date.today() - datetime.timedelta(days=DAYS_AGO)).strftime('%Y-%m-%d')
    
    # Query: create dopo date_start, ordinate per numero di stelle in ordine decrescente
    search_url = f"https://api.github.com/search/repositories?q=created:>{date_start}&sort=stars&order=desc&per_page={NUM_REPOS}"
    
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
    print(f"Ricerca delle top {NUM_REPOS} repository create dal {date_start}...")
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Errore API (Codice {response.status_code}): {response.text}")
        return []
        
    return response.json().get('items', [])

def download_readmes(repos):
    """Scarica i file README per una lista di repository."""
    # Crea la cartella di destinazione se non esiste
    output_dir = 'readmes'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'

    for i, repo in enumerate(repos, 1):
        full_name = repo['full_name']
        owner = repo['owner']['login']
        name = repo['name']
        
        print(f"[{i}/{len(repos)}] Scaricamento README di: {full_name}")
        
        readme_url = f"https://api.github.com/repos/{owner}/{name}/readme"
        response = requests.get(readme_url, headers=headers)
        
        if response.status_code == 200:
            # Sostituisce la barra (/) con un underscore (_) per il nome del file
            safe_filename = full_name.replace('/', '_') + '.md'
            filepath = os.path.join(output_dir, safe_filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
        elif response.status_code == 404:
            print(f"  -> Nessun README trovato per {full_name}.")
        elif response.status_code in (403, 429):
            print("  -> Limite di richieste API raggiunto (Rate Limit). Aggiungi un GITHUB_TOKEN se non l'hai fatto.")
            break
        else:
            print(f"  -> Errore {response.status_code} scaricando {full_name}.")
            
        # Pausa per rispettare le linee guida sulle richieste API di GitHub e non farsi bloccare
        time.sleep(1) 

if __name__ == "__main__":
    trending_repos = get_trending_repos()
    
    if trending_repos:
        download_readmes(trending_repos)
        print("\nOperazione completata! Tutti i README sono stati salvati nella cartella 'readmes/'.")
    else:
        print("\nNessuna repository trovata o errore nell'esecuzione.")