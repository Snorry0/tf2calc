import requests
def api_prezzo():
    url = 'https://backpack.tf/api/IGetPrices/v1?key=TUO_API_KEY'  # Inserisci la tua API key qui
    response = requests.get(url)
    data = response.json()
    key_price = data['response']['currencies']['keys']['price']['value']

    return key_price

def scomponi_refined(totale_refined):
    # Estrai refined (parte intera)
    refined = int(totale_refined)
    restante = totale_refined - refined
    reclaimed = int(restante // 0.33)
    scrap = int(round((restante % 0.33) / 0.11))
    return refined, reclaimed, scrap


def calcola_refined(totref, totrec, totscrap):
    # Estrai refined (parte intera)
    refined = totref
    #partiamo dal calcolo del valore minore, lo scrap
    #così facendo se lo scrap da resto, lo posso portare "sopra" (al reclaimed, essendo che 0.33 scrap -> 1 rec || 0.99 scrap -> 1 ref)
    # Calcola scrap
    while totscrap >= 3:
        if totscrap >= 9:
            refined+=1
            totscrap-=9
        elif totscrap >= 3:
            totrec += 1
            totscrap -= 3
    scrap = totscrap * 0.11
    # Calcola reclaimed 
    while totrec >= 3:
        refined+=1
        totrec -=3
    reclaimed = totrec * 0.33

    return refined, reclaimed, scrap

def esegui_operando_generics(expr):
    expr = expr.replace(' ', '')
    for op in ['+','-','*','/']:
        if op in expr:
            oper1, oper2 = expr.split(op) #con questa funzione andiamo a separare gli operandi, e il termine di separazione è l'operazione
            oper1 = float(oper1) #l'espressione la considera come totalmente string, devo riconvertirla in float
            oper2 = float(oper2)
            operando = op
            break
    else:
        raise Exception("Operatore non trovato nella stringa");
        
    ref1, rec1, scrap1 = scomponi_refined(oper1)
    ref2, rec2, scrap2 = scomponi_refined(oper2)
    print(f"Refined: {ref1, ref2}")
    print(f"Reclaimed: {rec1, rec2}")
    print(f"Scrap: {scrap1, scrap2}")

    totale1 = ref1 + rec1 * 0.33 + scrap1 * 0.11
    totale2 = ref2 + rec2 * 0.33 + scrap2 * 0.11

    #checko le operazioni
    if op == '+':
        ris = totale1 + totale2
    elif op == '-':
        if(totale1 < totale2):
            ris = totale2 - totale1
        else: ris = totale1 - totale2 
    elif op == '*':
        ris = totale1 * totale2
    elif op == '/':
        if totale2 > 0:
            ris = totale1 + totale2
        else:
            raise Exception("Divisione con 0 e minore non permessa!")
    
    risRef, risRec, risScrap = scomponi_refined(ris)
    risRef, risRec, risScrap = calcola_refined(risRef, risRec, risScrap)

    return risRef, risRec, risScrap
# Input dell'utente
expr = input("Inserisci l'espressione in refined (es 3.33 + 2.66): ")
ref, rec, scrap = esegui_operando_generics(expr)
tot = ref+rec+scrap
print("Risultato:", tot)

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


