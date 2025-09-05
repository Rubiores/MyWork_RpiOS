# MyWork_RpiOS

This repository documents the **first stage** of the differential drive robot project with LiDAR, developed on a **Raspberry Pi 4 (64-bit)** running **Raspberry Pi OS**.  

All the work in this stage was done inside **Docker containers**, which allowed testing ROS 2 in an isolated and controlled environment.

---

##  Initial Goals
- Set up a **ROS 2 (Foxy/Humble)** environment in Docker on Raspberry Pi OS.  
- Integrate the **RPLIDAR A1** sensor and visualize data in **RViz2**.  
- Test basic nodes: `rplidar_node`, `static_transform_publisher`, and first URDF models.  
- Document the Docker-based workflow as a foundation for the migration to Ubuntu.  

---

##  Repository Contents
- **Docker configurations**: images and containers used to run ROS 2 on Raspberry Pi.  
- **ROS 2 test nodes**: LiDAR connection, data publishing, and transformations.  
- **URDF/Xacro**: first robot model for visualization in RViz2.  
- **Notes and experiments**: commands, tests, and results obtained inside containers.  

---

##  Lessons Learned
- Docker was essential to keep a controlled and repeatable environment, though handling devices like `/dev/ttyUSB0` required extra setup.  
- RViz2 validated LiDAR connectivity and the correctness of published transformations.  
- Using commits as a log helped maintain a clear record of each step.  

---

##  Next Steps
This repository will remain as a **historical reference**. Development will continue on **Ubuntu for Raspberry Pi 4**, where:  
- ROS 2 will run directly on the OS (without Docker).  
- Motor control, odometry, and advanced mapping will be added.  
- The project will move toward autonomous navigation.  

Future progress will be tracked in a new repository: **MyWork_UbuntuROS**.

---

##  Note
This project was an **experimental stage with Docker**. While it is not the final result, it serves as the **foundation of knowledge** to move further in the Ubuntu migration.


# MyWork_RpiOS

Este repositorio documenta la **primera etapa** del proyecto de robot diferencial con LiDAR, desarrollada en una **Raspberry Pi 4 (64-bit)** con **Raspberry Pi OS**.  

Todo el trabajo se realizó dentro de **contenedores Docker**, lo que permitió experimentar con ROS 2 de forma aislada y controlada.

---

##  Objetivo inicial
- Levantar un entorno de **ROS 2 (Foxy/Humble)** en Docker sobre Raspberry Pi OS.  
- Integrar el sensor **RPLIDAR A1** y visualizar datos en **RViz2**.  
- Probar nodos básicos: `rplidar_node`, `static_transform_publisher` y primeros modelos URDF.  
- Documentar la experiencia con Docker como base para la migración futura a Ubuntu.  

---

##  Contenido
- **Configuraciones Docker**: imágenes y contenedores usados para correr ROS 2 en la Raspberry Pi.  
- **Nodos ROS 2 de prueba**: conexión al LIDAR, publicación de datos y transformaciones.  
- **URDF/Xacro**: primer modelo del robot para visualizar en RViz2.  
- **Notas y experimentos**: comandos, pruebas y resultados obtenidos dentro de los contenedores.  

---

##  Lecciones aprendidas
- Docker fue clave para mantener un entorno controlado y repetible, aunque el manejo de dispositivos (`/dev/ttyUSB0`) exigió configuraciones adicionales.  
- RViz2 permitió validar la conexión con el LiDAR y verificar las transformaciones publicadas.  
- El uso de commits como bitácora ayudó a mantener un registro claro de cada avance.  

---

##  Próximos pasos
Este repositorio queda como **referencia histórica**. No se seguirá ampliando porque el proyecto migrará a **Ubuntu en Raspberry Pi 4**, donde:  
- Se trabajará directamente en el sistema operativo, sin depender de Docker.  
- Se integrarán motores, odometría y mapeo más avanzado.  
- Se dará inicio a la fase de navegación autónoma.  

El nuevo desarrollo quedará en un repositorio separado: **MyWork_UbuntuROS**.

---

## 📌 Nota
Este proyecto fue una **etapa de aprendizaje con Docker**. Aunque no es el resultado final, constituye la base de conocimientos para avanzar más lejos en la migración a Ubuntu.
 el estado final del robot, sino un **punto de partida** que permitirá avanzar más lejos en la migración a Ubuntu.
