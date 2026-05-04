from fire import Fire
from tax import taxes
import math
 
def cap_loan(annual_rate_pct: float, monthly_payment: float, n_months: int) -> float:
    """
    Maximum loan capital for a fixed monthly payment.

    Standard amortization formula: C = M * (1 - (1+i)^-N) / i
    where i is the monthly rate.
    """
    if annual_rate_pct == 0:
        return monthly_payment * n_months

    i = annual_rate_pct / 1200
    return monthly_payment * (1 - (1 + i) ** -n_months) / i

# Approximate conversion ratios for a cadre (executive) status:
#   gross -> net          ~= 0.78  (employee social contributions ~22%)
#   net   -> net taxable  ~= 1.025 (non-deductible CSG/CRDS)
GROSS_TO_NET = 0.78
NET_TO_TAXABLE = 1.025
GROSS_TO_TAXABLE = GROSS_TO_NET * NET_TO_TAXABLE


def my_taxes(income_1: int, income_2: int, nb_children:int):
    """
    Args:
        income_1: Yearly annual gross revenues for the first person
        income_2: Yearly annual gross revenues for the second person
        nb_children : Number of children
    """

    if nb_children > 2:
        full_parts = nb_children -2
        half_parts = 1  #2*0.5
    else:
        full_parts = 0
        half_parts = 0.5*nb_children

    parts = half_parts + full_parts

    net_1 = income_1 * GROSS_TO_NET
    net_2 = income_2 * GROSS_TO_NET
    taxable_1 = income_1 * GROSS_TO_TAXABLE
    taxable_2 = income_2 * GROSS_TO_TAXABLE

    situations = {
        f"Not married {nb_children} child, first person declares the children":[[taxable_1, 1+ parts], [taxable_2, 1]],
        f"Not married {nb_children} child, second person declares the children":[[taxable_1, 1], [taxable_2, 1 + parts]],
        f"Married {nb_children} child":[[taxable_1 + taxable_2, 2 + parts]],
    }

    total_gross_revenues = income_1 + income_2
    total_net_revenues = net_1 + net_2

    for key, value in situations.items():
        taxes_to_pay = 0
        for element in value:
            taxes_to_pay += taxes(taxable_annual_income=element[0], nb_parts=element[1])

        taxes_to_pay = math.ceil(taxes_to_pay)
        max_debt_year = math.ceil(total_net_revenues * 0.35)
        max_debt_month = math.ceil(max_debt_year/12)
        netto_after_tax = math.ceil(total_net_revenues - taxes_to_pay)
        netto_after_tax_month = math.ceil(netto_after_tax /12)

        print(f"{key} : \n\tGross revenues: {math.ceil(total_gross_revenues)}/yr {math.floor(total_gross_revenues/12)}/month,"
              f"\n\tNetto revenues before income tax: {math.ceil(total_net_revenues)}/yr {math.floor(total_net_revenues/12)}/month,"
              f"\n\tMaximum housing loan montly payment: {max_debt_month} / month"
              f"\n\tMaximum housing loan at 4% interest rate over 25 years : {math.ceil(cap_loan(4,max_debt_month,300))} euros."
              f"\n\tTaxes : {taxes_to_pay} / year"
              f"\n\tNetto revenues after income tax : {netto_after_tax_month} / month"
              f"\n\tNetto revenues after income tax, minus housing :"
              f" {netto_after_tax_month - max_debt_month} / month"
        )



if __name__ == "__main__":
    Fire(my_taxes)
