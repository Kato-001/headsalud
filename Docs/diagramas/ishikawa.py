# Dibuja el diagrama de Ishikawa (causa-efecto) del problema de la Clínica Vida Salud.
# Uso: python ishikawa.py  -> 04_ishikawa.png
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

EFECTO = 'Programación deficiente\nde las citas médicas en la\nClínica Vida Salud'
ARRIBA = [
    ('C1. Métodos y procesos', ['Citas anotadas en cuadernos', 'Reprogramación solo por teléfono',
                                'Sin control de estados de la cita', 'Cancelaciones no registradas']),
    ('C2. Personal', ['Recepción sobrecargada en horas pico', 'Errores al transcribir datos',
                      'Desconoce cambios de horario', 'Sin roles ni permisos definidos']),
    ('C3. Tecnología', ['Hojas de cálculo aisladas', 'Sin sistema centralizado',
                        'Sin respaldo de la información', 'Sin acceso desde otro lugar']),
]
ABAJO = [
    ('C4. Información y datos', ['Pacientes duplicados o incompletos', 'Historial clínico disperso',
                                 'Sin reportes de atenciones', 'Sin trazabilidad de cambios']),
    ('C5. Pacientes', ['No conocen los horarios libres', 'Inasistencias sin aviso',
                       'Largas esperas al teléfono', 'No reciben recordatorios']),
    ('C6. Gestión administrativa', ['Horarios de médicos cambian sin aviso', 'Sin indicadores de gestión',
                                    'Decisiones sin datos', 'Control manual de feriados y permisos']),
]

TEAL, GRIS, AMBAR = '#0f766e', '#334155', '#b45309'
fig, ax = plt.subplots(figsize=(19.5, 8.2), dpi=150)
ax.set_xlim(0, 19.5)
ax.set_ylim(0, 8.2)
ax.axis('off')
plt.rcParams['font.family'] = 'Segoe UI'

Y = 4.1
ax.annotate('', xy=(15.0, Y), xytext=(0.4, Y), arrowprops=dict(arrowstyle='-|>', lw=3, color=GRIS, mutation_scale=25))
ax.text(17.2, Y, EFECTO, ha='center', va='center', fontsize=15, fontweight='bold', color='white',
        bbox=dict(boxstyle='round,pad=0.7', fc=TEAL, ec=TEAL))
ax.text(9.5, 8.0, 'Diagrama de Ishikawa · causa y efecto', ha='center', fontsize=15, fontweight='bold', color=GRIS)

XS = [4.4, 9.0, 13.6]
for grupo, signo in ((ARRIBA, 1), (ABAJO, -1)):
    for (cat, causas), x in zip(grupo, XS):
        y_ext = Y + signo * 3.2
        x_ext = x - 1.6
        ax.plot([x_ext, x], [y_ext, Y], color=GRIS, lw=2)
        ax.text(x_ext, y_ext + signo * 0.32, cat, ha='center', va='center', fontsize=13.5, fontweight='bold', color=AMBAR,
                bbox=dict(boxstyle='round,pad=0.35', fc='#fffbeb', ec=AMBAR))
        for k, causa in enumerate(causas):
            t = (k + 0.7) / (len(causas) + 0.4)
            px = x_ext + (x - x_ext) * t
            py = y_ext + (Y - y_ext) * t
            ax.plot([px - 0.6, px], [py, py], color='#94a3b8', lw=1.1)
            ax.text(px - 0.65, py + 0.08, causa, ha='right', va='bottom', fontsize=11, color='#1e293b')

plt.tight_layout()
plt.savefig(Path(__file__).with_name('04_ishikawa.png'), facecolor='white')
print('04_ishikawa.png')
