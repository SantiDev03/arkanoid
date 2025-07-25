# Argenoid

**Argenoid** es un juego inspirado en el clásico Arkanoid, desarrollado en Python usando Pygame. Tiene temática argentina, con gráficos personalizados, sonidos nacionales y una ambientación animada.

---

## Características

- Juego 2D tipo Arkanoid
- Menú animado con bandera argentina
- Colisiones entre pelota, bloques y paddle
- Sistema de puntaje y vidas
- Música de fondo (Himno Nacional Argentino)
- Efectos de sonido al destruir bloques
- Reutilización de sprites con Pygame

---

## Instrucciones de Uso

1. Clona el repositorio:
```bash
git clone https://github.com/tu_usuario/argenoid.git
```

2. Instala dependencias:
```bash
pip install pygame
```

3. Ejecuta el juego:
```bash
python app.py
```

---

## Controles del Juego

- 🕹️ Mover paddle: Flechas izquierda y derecha
- 🟢 Iniciar juego: Botón PLAY en el menú
- 🔁 Reiniciar: Botón REINICIAR en pantalla de Game Over
- ❌ Salir: Botón SALIR o cerrar ventana

---

## Recursos Usados

- **Gráficos**: Pelota, fondo bandera, animación de soles
- **Sonidos**:
  - Himno Nacional Argentino (loop en el menú)
  - Efectos tipo Arkanoid al romper bloques

---

## Patrones de Diseño Utilizados

| Patrón de Diseño     | Uso                                                                 |
|----------------------|---------------------------------------------------------------------|
| Singleton (implícito)| `screen`, `clock` usados globalmente como instancia única           |
| Factory              | Creación masiva de bloques dentro de bucles                         |
| Composición          | La clase `Ball` recibe paddle y bloques como dependencias externas |
| State                | Manejo de estados (`menu`, `jugando`, `game_over`)                 |
| Game Loop            | Bucle principal de juego con eventos, lógica y renderizado         |

---

## Créditos

Desarrolladores:
- Rubén Ledesma
- Rodrigo Espinosa
- Santiago Puebla
- Santiago Romano

---

## Licencia

Este proyecto es libre para uso educativo. Podés modificarlo y adaptarlo según tus necesidades.