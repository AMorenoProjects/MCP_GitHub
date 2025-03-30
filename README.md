# MCP GitHub

Este es un MCP (Managed Control Protocol) que permite interactuar con GitHub de manera programática. Este MCP facilita operaciones comunes de GitHub como crear Pull Requests, gestionar ramas y buscar código.

## ¿Qué hace este MCP?

Este MCP proporciona las siguientes funcionalidades:

1. **Gestión de Repositorios**:
   - Listar todos tus repositorios
   - Ver detalles de cada repositorio

2. **Gestión de Ramas**:
   - Crear nuevas ramas
   - Cambiar entre ramas
   - Listar ramas existentes

3. **Pull Requests**:
   - Crear nuevos Pull Requests
   - Listar Pull Requests existentes
   - Obtener detalles de un Pull Request

4. **Búsqueda de Código**:
   - Buscar código en repositorios
   - Filtrar resultados por lenguaje
   - Obtener detalles de archivos específicos

## Requisitos

Para usar este MCP necesitas:
- Python 3.7 o superior
- Token de acceso personal de GitHub
- La biblioteca `PyGithub` de Python

## Instalación

1. Asegúrate de tener Python instalado en tu computadora
2. Instala las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```
3. Configura tu token de GitHub:
   - Ve a GitHub → Settings → Developer Settings → Personal Access Tokens
   - Crea un nuevo token con los permisos necesarios
   - Guarda el token en un archivo `.env` en la raíz del proyecto

## Uso

Para usar el MCP, simplemente ejecuta:
```
python github_mcp.py
```

El programa mostrará un menú interactivo con las siguientes opciones:

1. **Listar mis repositorios**: Muestra todos tus repositorios de GitHub
2. **Crear una nueva rama**: Crea una nueva rama en un repositorio específico
3. **Crear un Pull Request**: Crea un nuevo Pull Request en un repositorio
4. **Buscar código**: Busca código en GitHub con filtros opcionales
5. **Salir**: Cierra el programa

## Notas importantes

- Mantén tu token de GitHub seguro y nunca lo compartas
- Este MCP es para fines educativos y de desarrollo
- Asegúrate de tener los permisos necesarios en los repositorios que quieras modificar
- Para crear ramas y Pull Requests, necesitas especificar el nombre completo del repositorio (usuario/repositorio) 