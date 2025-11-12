import os
import requests
from calc import scomponi_refined, calcola_refined
def api_prezzo():
    api_key = os.getenv('BF_TOK_API_KEY')
    if not api_key:
        raise RuntimeError("Inserisci l'api key nell'env!")
    url = 'https://backpack.tf/api/IGetPrices/v4?key' 
    response = requests.get(url)
    data = response.json()
    key_price = data['response']['currencies']['keys']['price']['value']

    return key_price



def esegui_operando_generics(expr):
    expr = expr.replace(' ', '')
    # trovo l'operatore: prendo il primo tra + - * /
    for op in ['+','-','*','/']:
        if op in expr:
            oper1_str, oper2_str = expr.split(op, 1)  # split una sola volta
            # controllo che i due pezzi non siano vuoti
            if not oper1_str or not oper2_str:
                raise Exception("Uno dei due operandi è vuoto!")
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

#totale = float(input("Inserisci il secondo valore in refined: "))

#totref = ref1+ref2
#totrec = rec1+rec2
#totscrap = scrap1+scrap2
#totref, totrec, totscrap = calcola_refined(totref, totrec, totscrap)




# Input dell'utente

#print(f"Refined: {totref}")
#print(f"Reclaimed: {totrec}")
#print(f"Scrap: {totscrap}")
#print(f"Totale verifica: {totref + totrec + totscrap }")


