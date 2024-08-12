from fire import Fire
from tax import taxes
import math
 
def capcredit(IA,M,N):
    """capcredit(IA,M,N): capital emprunté à IA%/an d'intérêt, remboursé en N mois avec une mensualité de M"""
    # si l'intérêt est nul, le capital est facile à calculer!
    if IA==0:
        C=M*N
        return C
    # calcul du capital emprunté
    I=IA/1200
    M=M
    C=M/(I*(1-(1/(1-(1+I)**N))))
    return C

def my_taxes(income_1: int, income_2: int, nb_children:int):
    """
    Args:
        income_1: Yearly annual net revenues for the first person
        income_2: Yearly annual net revenues for the first person
        nb_children : Number of children
    """
   
    if nb_children > 2:
        full_parts = nb_children -2
        half_parts = 1  #2*0.5
    else:
        full_parts = 0
        half_parts = 0.5*nb_children

    parts = half_parts + full_parts

    situations = {
        f"Not married {nb_children} child, first person declares the children":[[income_1, 1+ parts], [income_2, 1]],
        f"Not married {nb_children} child, second person declares the children":[[income_1, 1], [income_2, 1 + parts]],
        f"Married {nb_children} child":[[income_1 + income_2, 2 + parts]],
    }

    total_net_revenues = income_1 + income_2
    
    for key, value in situations.items():
        taxes_to_pay = 0
        for element in value:
            taxes_to_pay += taxes(taxeable_annual_income=element[0], nb_parts=element[1])

        taxes_to_pay = math.ceil(taxes_to_pay)
        max_debt_year = math.ceil(total_net_revenues * 0.35)
        max_debt_month = math.ceil(max_debt_year/12) 
        netto_after_tax = math.ceil(total_net_revenues - taxes_to_pay)
        netto_after_tax_month = math.ceil(netto_after_tax /12)

        print(f"{key} : \n\tNetto revenues before income tax: {total_net_revenues}/yr {math.floor(total_net_revenues/12)}/month,"
              f"\n\tMaximum housing loan montly payment: {max_debt_month} / month"
              f"\n\tMaximum housing loan at 4% interest rate over 25 years : {math.ceil(capcredit(4,max_debt_month,300))} euros."
              f"\n\tTaxes : {taxes_to_pay} / year"
              f"\n\tNetto revenues after income tax : {netto_after_tax_month} / month"
              f"\n\tNetto revenues after income tax, minus housing :"
              f" {netto_after_tax_month - max_debt_month} / month"
        )



if __name__ == "__main__":
    Fire(my_taxes)
