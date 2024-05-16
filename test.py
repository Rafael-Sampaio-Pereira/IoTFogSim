# PERGUNTA
# crie um objeto em python que simule a luminância e temperatura do sol num pais tropical

# RESPOSTA:
# Para simular a luminância e a temperatura do sol em um país tropical, podemos criar uma classe Python chamada SimuladorSolTropical. Essa classe pode ter métodos para calcular a luminância e a temperatura com base em diferentes fatores, como a hora do dia e a estação do ano.

# Vamos criar um exemplo simples onde a luminância e a temperatura variam ao longo do dia, assumindo que o comportamento do sol segue um padrão típico de um país tropical.


# Explicação do Código:
    
# 1 - Importações:
#     math para funções matemáticas.
#     datetime para manipular datas e horas.
    
# 2 - Classe SimuladorSolTropical:

#     O construtor __init__ inicializa a latitude, que pode influenciar a simulação (aqui, usamos 0 para simplificação).

#     O método calcular_luminancia calcula a luminância baseada na hora do dia. Supondo que a luminância varia de 0 lux durante a noite para um pico de 1000 lux ao meio-dia.

#     O método calcular_temperatura calcula a temperatura baseada na hora do dia, variando de 20°C à noite para um pico de 30°C ao meio-dia.

#     O método obter_luminancia_e_temperatura obtém a hora atual e usa os métodos anteriores para calcular a luminância e a temperatura correspondentes.

# 3 - Uso da Classe:

#     Um objeto SimuladorSolTropical é criado.
#     O exemplo demonstra como obter a luminância e a temperatura para uma data e hora específicas.
    
# Este código é simplificado e assume um comportamento idealizado do sol. Em uma implementação mais avançada, você poderia incluir variações sazonais, efeitos atmosféricos e outras influências.

# =====================================================================================================================

# PERGUNTA
# explique o uso linha 1000 * math.sin(math.pi * (hora - 6) / 12) da resposta anterior. Por que você utilizou math.sin e math.pi na formula?

# RESPOSTA
# A linha 1000 * math.sin(math.pi * (hora - 6) / 12) é usada para simular a variação da luminância ao longo do dia em um país tropical. Vamos detalhar o uso de math.sin e math.pi nesta fórmula e por que ela foi construída dessa forma.

# Explicação da Fórmula
# Objetivo:
# A fórmula simula a luminância solar, que varia de 0 lux (durante a noite) a um valor máximo ao meio-dia, seguindo um padrão sinusoidal para refletir o ciclo diário do sol.

# Componentes da Fórmula:
# 1 - math.sin:

#     A função sin (seno) é usada para criar uma variação suave e contínua que se repete periodicamente.
#     A função seno varia entre -1 e 1, o que é ideal para simular ciclos como o do dia e da noite.
# 2 - math.pi:

#     math.pi é uma constante que representa o número π (pi), que é aproximadamente 3.14159.
#     Usar π ajuda a mapear a função seno a um ciclo de 24 horas.
    
# 3 - (hora - 6):

#     hora é a hora do dia (0 a 23).
#     Subtrair 6 ajusta o ciclo para que o pico da função seno (que ocorre em π/2) corresponda ao meio-dia (12 horas).
#     Isto desloca o gráfico do seno para que ele comece a aumentar a partir das 6 da manhã, atinja o pico ao meio-dia e volte a 0 às 18 horas.
# 4 - (hora - 6) / 12:

#     Dividir por 12 ajusta a periodicidade da função seno para que ela complete meio ciclo em 12 horas.
#     Isto significa que math.sin(math.pi * (hora - 6) / 12) irá variar de 0 a 1 entre as 6 da manhã e o meio-dia, e de volta a 0 às 18 horas.
# 5 - 1000 *:

#     Multiplicar por 1000 ajusta a amplitude da função seno para que a luminância varie de 0 a 1000 lux.
#     O valor 1000 lux é arbitrário e pode ser ajustado conforme necessário para representar a intensidade máxima da luz solar.

# Funcionamento ao Longo do Dia:
# - Manhã (6h-12h):

#     Às 6h: math.sin(math.pi * (6 - 6) / 12) = math.sin(0) = 0
#     Às 9h: math.sin(math.pi * (9 - 6) / 12) = math.sin(math.pi / 4) ≈ 0.707
#     Ao meio-dia: math.sin(math.pi * (12 - 6) / 12) = math.sin(math.pi / 2) = 1
    
# - Tarde (12h-18h):

#     Às 15h: math.sin(math.pi * (15 - 6) / 12) = math.sin(3 * math.pi / 4) ≈ 0.707
#     Às 18h: math.sin(math.pi * (18 - 6) / 12) = math.sin(math.pi) = 0
    
# - Noite (18h-6h):

#     Às 21h: math.sin(math.pi * (21 - 6) / 12) = math.sin(5 * math.pi / 4) ≈ -0.707 (mas a fórmula limita isso a 0 lux)
#     A função seno nos dá uma curva suave que sobe e desce gradualmente, refletindo a variação natural da luz solar durante o dia. A multiplicação por 1000 ajusta a escala para representar a intensidade da luz.

# Resumo
# A fórmula 1000 * math.sin(math.pi * (hora - 6) / 12) é uma maneira simplificada de simular a variação diária da luminância solar. Ela usa a função seno para criar um ciclo suave e contínuo que atinge seu pico ao meio-dia e retorna a zero ao anoitecer, ajustado para o contexto de um país tropical.

import math
import datetime

class SimuladorSolTropical:
    def __init__(self, latitude):
        self.latitude = latitude
    
    def calcular_luminancia(self, hora):
        # Simula a luminância com base na hora do dia
        if 6 <= hora <= 18:
            return 1000 * math.sin(math.pi * (hora - 6) / 12)
        else:
            return 0
    
    def calcular_temperatura(self, hora):
        # Simula a temperatura com base na hora do dia
        if 6 <= hora <= 18:
            return 20 + 10 * math.sin(math.pi * (hora - 6) / 12)
        else:
            return 20
    
    def obter_luminancia_e_temperatura(self, data_hora):
        hora = data_hora.hour
        luminancia = self.calcular_luminancia(hora)
        temperatura = self.calcular_temperatura(hora)
        return luminancia, temperatura

if __name__ == "__main__":
    simulador = SimuladorSolTropical(latitude=0)  # Latitude para um país tropical
    
    # Exemplo: Obter a luminância e a temperatura às 10h do dia 15 de maio de 2024
    data_hora = datetime.datetime(2024, 5, 15, 10)
    luminancia, temperatura = simulador.obter_luminancia_e_temperatura(data_hora)
    
    print(f"Data e Hora: {data_hora}")
    print(f"Luminância: {luminancia:.2f} lux")
    print(f"Temperatura: {temperatura:.2f} °C")