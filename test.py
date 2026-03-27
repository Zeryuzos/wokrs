import random
from collections import Counter

class Dado:
    def __init__(self, caras=6):
        if caras < 2:
            raise ValueError("Un dado debe tener al menos 2 caras.")
        self.caras = caras
        self.historial = []

    def lanzar(self):
        """Simula un lanzamiento único y lo guarda en el historial."""
        resultado = random.randint(1, self.caras)
        self.historial.append(resultado)
        return resultado

    def lanzar_multiple(self, veces):
        """Lanza el dado una cantidad N de veces."""
        resultados = [random.randint(1, self.caras) for _ in range(veces)]
        self.historial.extend(resultados)
        return resultados

    def calcular_frecuencias(self):
        """Retorna la cantidad de veces que salió cada cara y su porcentaje."""
        if not self.historial:
            return None

        conteo = Counter(self.historial)
        total = len(self.historial)

        # Ordenamos por el número de la cara para que sea legible
        frecuencias = {cara: {"cantidad": conteo[cara],
                              "porcentaje": (conteo[cara] / total) * 100}
                       for cara in range(1, self.caras + 1)}
        return frecuencias

    def calcular_promedio(self):
        """Calcula el promedio aritmético de los lanzamientos actuales."""
        if not self.historial:
            return 0
        return sum(self.historial) / len(self.historial)

    def verificar_si_es_justo(self, margen_error=0.05):
        """
        Compara la frecuencia real con la teórica (1/caras).
        El margen_error define qué tanta desviación permitimos (ej. 5%).
        """
        if not self.historial:
            return "No hay datos suficientes."

        frecuencias = self.calcular_frecuencias()
        probabilidad_teorica = 1 / self.caras
        es_justo = True
        detalles = {}

        for cara, datos in frecuencias.items():
            prob_real = datos["porcentaje"] / 100
            desviacion = abs(prob_real - probabilidad_teorica)

            # Si la desviación es mayor al margen, se considera sospechoso
            if desviacion > margen_error:
                es_justo = False
            detalles[cara] = desviacion

        return es_justo, detalles

# --- Ejemplo de uso ---
mi_dado = Dado(6)

# Simulamos 10,000 lanzamientos para tener una base estadística sólida
mi_dado.lanzar_multiple(10000)

print(f"--- Estadísticas del Dado de {mi_dado.caras} caras ---")
print(f"Promedio: {mi_dado.calcular_promedio():.2f}")

frec = mi_dado.calcular_frecuencias()
for cara, info in frec.items():
    print(f"Cara {cara}: {info['cantidad']} veces ({info['porcentaje']:.2f}%)")

justo, analisis = mi_dado.verificar_si_es_justo()
print(f"\n¿El dado es justo? {'Sí' if justo else 'Sospechoso'}")