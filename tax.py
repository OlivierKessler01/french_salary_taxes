from fire import Fire

# Constants below are for income year 2024 (filed in 2025).
# Update yearly from the loi de finances.

def tax_relief(ir, nb_parts):
    somme_forfaitaire = [889, 1470]                # décote 2025
    ceiling_tax_relief = [1965, 3249]              # = somme_forfaitaire / 0.4525
    if nb_parts == 1:
        if ir <= ceiling_tax_relief[0]:
            return max(0, (1.0 + 45.25/100) * ir - somme_forfaitaire[0])
        return ir
    if ir <= ceiling_tax_relief[1]:
        return max(0, (1.0 + 45.25/100) * ir - somme_forfaitaire[1])
    return ir

def slices_taxes(taxable_annual_income, nb_parts):
    tranches = [  # tranches barème 2025 (revenus 2024)
        (0,      11497,        0),
        (11498,  29315,        11),
        (29316,  83823,        30),
        (83824,  180294,       41),
        (180295, float("inf"), 45),
    ]
    r = 0.9 * taxable_annual_income / nb_parts
    res = 0
    for item in tranches:
        if r > item[0]:
            res +=  min(r - item[0], item[1] - item[0]) * item[2] / 100
    res *= nb_parts
    return tax_relief(res, nb_parts)

def taxes(taxable_annual_income, nb_parts):
    ir1 = slices_taxes(taxable_annual_income, nb_parts)
    if nb_parts <= 2.0: return ir1

    ir2 = slices_taxes(taxable_annual_income, 2)
    half_part_ceiling = 1791                       # plafonnement QF 2025 par demi-part
    reduction = (nb_parts - 2) / 0.5 * half_part_ceiling
    
    if ir2 - ir1 > reduction:
        return ir2 - reduction
    else:
        return ir1

def print_range(rmin, rmax, rstep, nparts):
    for r in range(rmin, rmax, rstep):
        print(r, taxes(r, nparts))



if __name__ == "__main__":
    Fire(taxes)
