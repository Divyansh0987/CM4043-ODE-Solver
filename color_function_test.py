def mixture_color(C_HBrO2, C_Br_, C_Fe3_, C_HBrO2_0, C_Br_0, C_Fe3_0 ):
    # Color changes mostly due to the redox reaction between Mn+ and M(n-1)+ (in this case Fe3+ and Fe2+), 
    # and the formation of Br2
    # Suppose C_BrO3 is constant so C_BrO3_0 = C_BrO3_
    C_Br2 = (0)/2
    C_Fe2_ = C_Fe3_0 - C_Fe3_
    color_Br2 = (176, 72, 12)
    color_Fe3_ = (255, 215, 77)
    color_Fe2_ = (173, 209, 230)
    color_with_conc = [ (color_Br2, C_Br2), 
                        (color_Fe3_, C_Fe3_), 
                        (color_Fe2_, C_Fe2_)]
    return mix_colors_cmyk(color_with_conc)    

# Extract concentration values at each timepoint, then return the respective mixed color
def color_over_time_fxn(solution,  C_HBrO2_0, C_Br_0, C_Fe3_0):
    mixed_colors_over_time = []
    for xi, yi, zi in zip(*solution.y):  # x, y, z at each timepoint
        mixed_rgb = mixture_color(float(xi), float(yi), float(zi), C_HBrO2_0, C_Br_0, C_Fe3_0)
        mixed_colors_over_time.append(mixed_rgb)
    return mixed_colors_over_time

# Use substractive color mixing to simulate real life color mixing (CYMK)
def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1  # pure black
    r_prime, g_prime, b_prime = r / 255, g / 255, b / 255
    k = 1 - max(r_prime, g_prime, b_prime)
    c = (1 - r_prime - k) / (1 - k) if k < 1 else 0
    m = (1 - g_prime - k) / (1 - k) if k < 1 else 0
    y = (1 - b_prime - k) / (1 - k) if k < 1 else 0
    return c, m, y, k

def cmyk_to_rgb(c, m, y, k):
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return r, g, b

def mix_colors_cmyk(colors_with_concentration):
    total_conc = sum(conc for _, conc in colors_with_concentration)
    if total_conc == 0:
        return (0, 0, 0)

    c_total = m_total = y_total = k_total = 0

    for (r, g, b), conc in colors_with_concentration:
        c, m, y, k = rgb_to_cmyk(r, g, b)
        c_total += c * conc
        m_total += m * conc
        y_total += y * conc
        k_total += k * conc

    c_avg = c_total / total_conc
    m_avg = m_total / total_conc
    y_avg = y_total / total_conc
    k_avg = k_total / total_conc

    return cmyk_to_rgb(c_avg, m_avg, y_avg, k_avg)

print(mixture_color(0.1, 0.1, 0.1, 0.1, 0.1, 0.1))