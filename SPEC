# SPEC – Especificación del Juego con IA

## 1. Nombre tentativo del juego
"AI Motion Challenge"  
*(Puedes cambiarlo después)*

---

## 2. Objetivo del juego
El jugador debe realizar ciertos gestos o poses frente a la cámara para superar retos, ganar puntos o activar eventos dentro del juego.

---

## 3. Plataforma
- **Versión principal:** Web (React + TensorFlow.js)
- **Alternativa:** Móvil (React Native + tfjs-react-native)

---

## 4. Mecánica General del Juego
1. El usuario enciende su cámara.
2. El sistema detecta:
   - Pose corporal (BlazePose o MoveNet)
   - Posición de manos (opcional)
   - Dirección del cuerpo
3. Se activa un modo de juego basado en retos:
   - Mantener una pose determinada (ej. levantar brazos)
   - Realizar un movimiento específico (girar, saltar simuladamente, etc.)
   - Evitar zonas marcadas (detección de colisiones usando puntos de pose)
4. El juego otorga puntuación según:
   - Precisión de los puntos detectados
   - Tiempo de ejecución
   - Número de intentos correctos

---

## 5. Estados del juego
- **Idle:** esperando jugador  
- **Calibration:** detectando cuerpo por primera vez  
- **Challenge Selection:** el sistema elige un reto  
- **Playing:** jugador ejecuta movimientos  
- **Result:** se muestra puntuación  
- **Restart:** volver a empezar  

---

## 6. Entradas del sistema (inputs)
- Flujo de cámara (imagen por cuadro)
- Coordenadas de puntos clave:
  - 33 puntos del modelo BlazePose (x, y, z, score)
- Datos derivados:
  - Ángulos del cuerpo (ej. codo, rodilla)
  - Distancias (ej. mano–hombro)
  - Velocidad de movimiento entre frames

---

## 7. Salidas del sistema (outputs)
- `pose_keypoints` (puntos detectados)
- `pose_confidence`
- `gesture_detected`
- `player_state`
- `game_score`

---

## 8. Reglas
- El jugador debe estar visible al menos 75% del cuerpo.
- El reto debe completarse en menos de 10 s.
- Los movimientos deben superar umbrales de precisión (por ejemplo ángulo del codo ±15°).
- Si no se detecta pose por 3 s → game pause.

---

## 9. Requerimientos Técnicos
### Web
- TensorFlow.js
- Modelo BlazePose o MoveNet
- Procesamiento en cliente (sin backend)

### Python (opcional)
- OpenCV para pruebas
- Mediapipe para detección offline
- Dataset opcional para entrenar clasificadores de gestos

---

## 10. Métricas de éxito
- FPS ≥ 15 en laptop promedio
- Detección estable del usuario
- Juego completamente funcional sin errores críticos

---

## 11. Posibles extensiones
- Modos extra (Simon Says, Dance, Dodge)
- Entrenamiento de clasificación personalizada
- Sonidos y animaciones

