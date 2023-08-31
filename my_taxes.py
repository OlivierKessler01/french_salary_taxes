from fire import Fire
from tax import taxes

def my_taxes(income_1: int, income_2: int, nb_children:int):

    nb_parts = 0
    half_parts = abs(0 - nb_children) * 0.5
    full_parts = nb_children - 2 if nb_children > 2 else 0
    parts = half_parts + full_parts

    situations = {
                f"Not married {nb_children} child, first person declare the children":[[income_1, 1+ parts], [income_2, 1]],
                f"Not married {nb_children} child, second person declare the children":[[income_1, 1], [income_2, 1 + parts]],
                f"Married {nb_children} child":[[income_1 + income_2, 2 + parts]],
            }

    revenues = income_1 + income_2
    
    for key, value in situations.items():
        result = 0
        for element in value:
            result += taxes(taxeable_annual_income=element[0], nb_parts=element[1])

        print(f"{key} : \n\tRevenues: {revenues}, \n\tTaxe :"
              f"{result}, \n\tAfter taxes: {revenues - result},"
              f" \n\tafter taxes per month netto: {(revenues - result)/12}")








if __name__ == "__main__":
    Fire(my_taxes)
