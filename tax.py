from fire import Fire

def tax_relief(ir, nb_parts):
    ceiling_tax_relief=[ 1840, 3045 ] # ceilings 2022
    somme_forfaitaire=[ 833, 1378 ]
    if nb_parts==1:
        if ir<=ceiling_tax_relief[0]:
            return max(0, (1.0+45.25/100)*ir - somme_forfaitaire[0])
        else:
            return ir
    else:
        if ir<=ceiling_tax_relief[1]:
            return max(0, (1.0+45.25/100)*ir - somme_forfaitaire[1])
        else:
            return ir

def slices_taxes(taxeable_annual_income, nb_parts):
    tranches = [  # tranches 2023
        (0, 10777, 0),
        (10778, 27478, 11),
        (27479, 78570, 30),
        (78571, 168994, 41),
        (168995, float("inf"), 45) ]
    r = 0.9 * taxeable_annual_income / nb_parts    
    res = 0
    for item in tranches:
        if r > item[0]:
            res +=  min(r - item[0], item[1] - item[0]) * item[2] / 100
    res *= nb_parts
    return tax_relief(res, nb_parts)

def taxes(taxeable_annual_income, nb_parts):
    ir1 = slices_taxes(taxeable_annual_income, nb_parts)
    if nb_parts <= 2.0: return ir1
    
    ir2 = slices_taxes(taxeable_annual_income, 2)
    ceiling_qf = [ 1678, 839 ] # ceiling 2023
    # 1678 pour chaque demi-part
    # 839 pour chaque demi-part
    reduction = (nb_parts-2)/0.25 * ceiling_qf[1]
    
    if ir2 - ir1 > reduction:
        return ir2 - reduction
    else:
        return ir1

def print_range(rmin, rmax, rstep, nparts):
    for r in range(rmin, rmax, rstep):
        print(r, taxes(r, nparts))



if __name__ == "__main__":
    Fire(taxes)
