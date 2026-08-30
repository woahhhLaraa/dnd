#!/usr/bin/env python3
"""Intervalo de Clopper-Pearson exacto al 95 % para una proporción.

Es el que usa `FODA.md` en la sección «Margen de error». Se saca aquí como
script para que cualquier cifra publicada en los documentos sea reproducible
con un comando, en vez de un número escrito a mano que nadie puede rehacer.

    python3 _verificacion/intervalo.py <fallos> <total> [<población>]

Con `población` además proyecta cuántos registros malos cabe esperar en un
conjunto mayor con esa misma tasa, con su intervalo.

Clopper-Pearson es **exacto**: se define directamente sobre la binomial, no
sobre la aproximación normal. Con muestras pequeñas y proporciones cercanas a
0 —el caso de esta base— la aproximación normal daría límites inferiores
negativos, que no significan nada.

Definición implementada, por bisección sobre la CDF binomial:
  - inferior = la p que hace P(X >= k | n, p) = alpha/2   (0 si k = 0)
  - superior = la p que hace P(X <= k | n, p) = alpha/2   (1 si k = n)
"""
import math
import sys


def _binom_cdf(k, n, p):
    """P(X <= k) para X ~ Binomial(n, p). Suma exacta con math.comb."""
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 1.0 if k >= n else 0.0
    total = 0.0
    for i in range(0, k + 1):
        total += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return min(1.0, total)


def _biseccion(f, objetivo, creciente):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        v = f(mid)
        if (v < objetivo) == creciente:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def clopper_pearson(k, n, conf=0.95):
    """(inferior, superior) para k fallos de n, exacto al `conf`."""
    if n == 0:
        return (0.0, 1.0)
    a = (1 - conf) / 2
    # P(X >= k) = 1 - P(X <= k-1), creciente en p
    lo = 0.0 if k == 0 else _biseccion(
        lambda p: 1 - _binom_cdf(k - 1, n, p), a, creciente=True)
    # P(X <= k) es decreciente en p
    hi = 1.0 if k == n else _biseccion(
        lambda p: _binom_cdf(k, n, p), a, creciente=False)
    return lo, hi


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    k, n = int(argv[1]), int(argv[2])
    if not 0 <= k <= n or n <= 0:
        print("fallos debe estar entre 0 y total, y total > 0")
        return 1
    lo, hi = clopper_pearson(k, n)
    print(f"{k} de {n} = {k / n * 100:.2f} %")
    print(f"IC 95 % (Clopper-Pearson exacto): {lo * 100:.2f} % – {hi * 100:.2f} %")
    if len(argv) > 3:
        N = int(argv[3])
        print(f"\nProyección sobre {N} registros con esa tasa:")
        print(f"  esperados  ≈ {k / n * N:.1f}")
        print(f"  intervalo  {lo * N:.1f} – {hi * N:.1f}")
        if k == 0:
            print("\n  OJO: 0 fallos NO significa tasa 0. En una muestra sin")
            print("  fallos lo único informativo es el límite SUPERIOR.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
