# Processing-Claude MCP Bridge

Integración entre Processing y Claude mediante el Model Context Protocol (MCP). Este proyecto permite controlar aplicaciones de Processing a través de conversaciones en lenguaje natural con Claude.

## Características

- Listar sketches de Processing disponibles
- Ejecutar sketches existentes con parámetros personalizados
- Crear nuevos sketches a través de descripción en lenguaje natural
- Actualizar sketches existentes

## Requisitos

- Python 3.10 o superior
- Processing 4.3 o superior
- Claude Desktop
- Módulos Python: mcp, httpx

## Instalación

1. Clona este repositorio
2. Instala las dependencias: `pip install "mcp[cli]" httpx`
3. Configura las rutas en `processing_server.py`
4. Configura Claude Desktop para usar el servidor MCP

## Configuración de Claude Desktop

Edita el archivo de configuración en:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
    "mcpServers": {
        "processing-bridge": {
            "command": "python",
            "args": [
                "RUTA/COMPLETA/A/processing_server.py"
            ]
        }
    }
}
```

## Uso

1. Ejecuta el servidor MCP: `python processing_server.py`
2. Inicia Claude Desktop
3. Interactúa con Processing mediante comandos como:
   - "Lista los sketches de Processing disponibles"
   - "Ejecuta mi sketch CirculoRebotando"
   - "Crea un nuevo sketch llamado ColorInteractivo con un círculo que cambie de color al hacer clic"

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request.
