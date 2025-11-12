from calc import scomponi_refined, calcola_refined

def test_scomponi_refined():
    assert scomponi_refined(4.22) == (4, 0, 2)
    assert scomponi_refined(5.55) == (5, 1, 2)
    assert scomponi_refined(0) == (0, 0, 0)

def test_calcola_refined_valori():
    ref, rec, scrap = calcola_refined(4, 3, 10)  # 3 reclaimed + 10 scrap devono normalizzarsi
    # 3 reclaimed = 1 refined + 0 reclaimed
    # 10 scrap = 3 reclaimed + 1 scrap (9 scrap = 3 reclaimed = 1 refined)
    # Totale: refined: 4 + 1 + 1 = 6, reclaimed: 0 + 1 = 1, scrap: 1
    # Essendo che in calcola refined includo il calcolo dei ref già ricomposti in currency di tf2, 
    # scrap testa direttamente 0.11. 
    assert ref == 6.0
    assert rec == 0.0
    assert scrap == 0.11
