"""
Kernelogik: beregner det forskudte nulpunkt (Millmans sætning) og den
resulterende spænding på hver fase ud fra effektbelastning i watt.
"""
import numpy as np


def fase_spaendinger(p1_w: float, p2_w: float, p3_w: float, u_n: float = 230.0):
    """
    Beregner nulpunktets forskydning og spændingen på hver fase.

    p1_w, p2_w, p3_w : belastning i watt på L1, L2, L3 (rent ohmsk antaget)
    u_n               : nominel fasespænding (V), default 230V

    Returnerer en dict med:
      - vertices: faste fasepunkter (komplekse tal) for L1, L2, L3
      - v_o: det oprindelige/faste centrum (altid 0+0j)
      - v_n: det forskudte nulpunkt (komplekst tal)
      - u_load: liste med [U_L1, U_L2, U_L3] (faktiske spændinger, V)
      - linjespaending: U_n * sqrt(3), til reference i diagrammet
    """
    # Faste fasepunkter, 120 grader forskudt, L1 lagt lige op (90 grader)
    vinkler_grader = [90, -30, 210]
    vertices = [u_n * np.exp(1j * np.radians(v)) for v in vinkler_grader]

    p_watt = [max(p1_w, 0.0), max(p2_w, 0.0), max(p3_w, 0.0)]
    # Admittans Y = P / U_n^2 (ren ohmsk antagelse). P=0 -> Y=0 (åben/ingen last).
    y_values = [p / (u_n ** 2) for p in p_watt]
    y_sum = sum(y_values)

    if y_sum <= 0:
        # Ingen belastning overhovedet på nogen fase -> nulpunktet er udefineret.
        v_n = 0 + 0j
        udefineret = True
    else:
        numerator = sum(v * y for v, y in zip(vertices, y_values))
        v_n = numerator / y_sum
        udefineret = False

    u_load = [abs(v - v_n) for v in vertices]
    beroeringsspaending = abs(v_n - (0 + 0j))

    return {
        "vertices": vertices,
        "v_o": 0 + 0j,
        "v_n": v_n,
        "u_load": u_load,
        "beroeringsspaending": beroeringsspaending,
        "linjespaending": u_n * np.sqrt(3),
        "u_n": u_n,
        "udefineret": udefineret,
    }


if __name__ == "__main__":
    # Selv-test med taleksemplet fra samtalen: L1 tung (10580W), L2 middel
    # (2645W), L3 næsten intet (53W) ved 230V -> forventet ca. 80V/318V/364V
    res = fase_spaendinger(10580, 2645, 53)
    for navn, u in zip(["L1", "L2", "L3"], res["u_load"]):
        print(f"{navn}: {u:.1f} V")

