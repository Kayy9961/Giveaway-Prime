![image](https://github.com/user-attachments/assets/293235b5-6efc-4917-9c2d-7f18f64ba863)

✨ Funciones clave:
✅ Verificación por rol (solo usuarios con el rol "comprador" pueden participar).

🔒 Una participación por usuario.

⏳ Temporizador en vivo en el embed (días, horas, minutos, segundos).

🔁 Actualización automática del mensaje cada 10 segundos.

💾 Persistencia completa: los participantes y el tiempo del sorteo se guardan en disco.

🧠 Reanudación automática tras reinicio del bot.

🏆 Selección aleatoria de ganadores al final del sorteo (4 ganadores únicos).

❌ Botón se desactiva automáticamente al terminar el sorteo.

📦 Código limpio, personalizable y preparado para ampliarse.

👥 Requisitos
Rol de comprador (ID personalizable) para poder participar.

Canal específico (ID) donde se envía el mensaje del sorteo.

Bot con permisos para enviar mensajes, gestionar roles (opcional) y acceder a miembros.

🔧 Configuración rápida
Edita el archivo y coloca:

Tu token

El ID de tu servidor (guild), canal, y rol.

Lanza el bot y automáticamente:

Crea el mensaje embed del sorteo

Actualiza la cuenta de participantes en vivo

Elige ganadores 7 días después

📁 Archivos generados
participants.json: lista de usuarios participantes.

giveaway_data.json: fecha de inicio del sorteo.

🔐 Seguridad
No usa base de datos externa.

Solo responde a usuarios con los permisos adecuados.

No permite spam ni bugs de concurrencia.
