import os
import requests
from calc import scomponi_refined, calcola_refined
def api_prezzo():
    api_key = (os.getenv('BPTF_API_KEY')
               or os.getenv('BP_TF_API_KEY')
               or os.getenv('BF_TOK_API_KEY'))
    if not api_key:
        raise RuntimeError("Inserisci l'api key nell'env!")
    url = 'https://backpack.tf/api/IGetCurrencies/v1' 
    # chiamo l'API (timeout per non rimanere appeso all'infinito, 10 secondi vanno bene per la lentezza dell'API stesso)
    #r = requests.get(url, params=params, timeout=10)
    # se 429 (rate limit, molto probabile perchè l'api è molto lento da quando tf2 ha introdotto tante varianti di unusual e skin), 
    # backpack.tf manda Retry-After: per ora mi limito a farlo fallire pulito
   # r.raise_for_status()
    #data = r.json()
    # voglio: response -> currencies -> keys -> price -> value (refined per 1 key)
    #try:
    #    key_price_ref = float(data["response"]["currencies"]["keys"]["price"]["value"])
    #except (KeyError, TypeError, ValueError):
    #    raise RuntimeError("Struttura risposta API cambiata o key invalida. Controlla la tua API key o la doc BP.tf")

    #if key_price_ref <= 0:
    #    raise RuntimeError("Prezzo key non valido dalla API (<=0).")
    r = requests.get(url, params={'key': api_key}, timeout=10)
    r.raise_for_status()
    data = r.json()

    # path standard (se 'response' non c'è, provo al top-level)
    try:
        return float(data['response']['currencies']['keys']['price']['value'])
    except KeyError:
        return float(data['currencies']['keys']['price']['value'])



def printf_parse_operand_tf2(operand_str, key_price_ref):
    # "alla meccanico": se finisce con 'k' stampo la conversione, ma NON la uso nei calcoli
    s = operand_str.strip().lower()
    if s.endswith('k'):
        num = s[:-1] or "1"   # "k" da solo = 1k
        try:
            qty = float(num)
        except ValueError:
            print(f"[parse] {operand_str} -> formato 'k' non valido (tipo '2k', '1.5k')")
            return
        val = qty * key_price_ref
        print(f"[parse] {operand_str} -> {val:.2f} ref   (1k = {key_price_ref:.2f} ref)")
    else:
        print(f"[parse] {operand_str} -> no 'k' (rimane {operand_str} ref)")


def esegui_operando_generics(expr):
    expr = expr.replace(' ', '')

    # prendo il prezzo chiave UNA volta (solo per il printf)
    try:
        key_price = api_prezzo()
        print(f"[api] 1 key = {key_price:.2f} ref")  # stampa sempre, così vedi che funziona
    except Exception as e:
        print(f"[api] impossibile ottenere prezzo key: {e}")
        key_price = None  # continuo senza 'k'
    # trovo l'operatore: prendo il primo tra + - * /
    for op in ['+','-','*','/']:
        if op in expr:
            oper1_str, oper2_str = expr.split(op, 1)  # split una sola volta
            # controllo che i due pezzi non siano vuoti
            if not oper1_str or not oper2_str:
                raise Exception("Uno dei due operandi è vuoto!")
                # --- SOLO PRINTF prima di scomporre ---
            if key_price is not None:
                printf_parse_operand_tf2(oper1_str, key_price)
                printf_parse_operand_tf2(oper2_str, key_price)
            # converto in float (refined)
            oper1 = float(oper1_str)
            oper2 = float(oper2_str)
            break
    else:
        raise Exception("Operatore non trovato nella stringa (usa + - * /)")
        
    #scompongo le due unità in pezzi singoli in ref/rec/scrap, sia per debug che per utilità
    ref1, rec1, scrap1 = scomponi_refined(oper1)
    ref2, rec2, scrap2 = scomponi_refined(oper2)
    print(f"Refined: {ref1, ref2}")
    print(f"Reclaimed: {rec1, rec2}")
    print(f"Scrap: {scrap1, scrap2}")


    # operazioni: + e - tra due importi; * e / trattano il secondo come SCALARE (utile nel trading)
    if op == '+':
        r = oper1 + oper2
    elif op == '-':
        r = abs(oper1 - oper2)
    elif op == '*':
        r = oper1 * oper2
    elif op == '/':
        if oper2 == 0:
            raise Exception("Divisione per 0 non permessa!")
        r = oper1 / oper2

    
    risRef, risRec, risScrap = scomponi_refined(r)
    risRef, risRec, risScrap = calcola_refined(risRef, risRec, risScrap)

    return risRef, risRec, risScrap
# Input dell'utente
expr = input("Inserisci l'espressione in refined (es 3.33 + 2.66): ")
ref, rec, scrap = esegui_operando_generics(expr)
tot = ref+rec+scrap
print(f"Risultato: {tot} ref") #f -> possiamo fare questo print


