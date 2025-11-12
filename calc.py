def scomponi_refined(totale_refined):
    # Estraggo refined, reclaimed e scrap separatamente
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

