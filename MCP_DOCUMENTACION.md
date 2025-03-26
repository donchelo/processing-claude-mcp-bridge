# Ficha Técnica: Model Context Protocol (MCP)

## Descripción General

El **Model Context Protocol (MCP)** es un protocolo abierto desarrollado por Anthropic que estandariza la forma en que las aplicaciones proporcionan contexto a los Modelos de Lenguaje Grande (LLMs). Funciona como una interfaz universal para conectar LLMs con diferentes fuentes de datos y herramientas.

## Características Principales

- **Estandarización**: Proporciona un método unificado para la comunicación entre LLMs y recursos externos
- **Integración flexible**: Permite conectar modelos de IA con diversas fuentes de datos y herramientas
- **Seguridad**: Mantiene los datos dentro de la infraestructura del usuario
- **Extensibilidad**: Soporta la creación de plugins y extensiones personalizadas

## Arquitectura

MCP sigue una arquitectura cliente-servidor:

- **Hosts MCP**: Aplicaciones como Claude Desktop que desean acceder a datos a través de MCP
- **Clientes MCP**: Componentes del protocolo que mantienen conexiones 1:1 con servidores
- **Servidores MCP**: Programas ligeros que exponen capacidades específicas a través del protocolo estandarizado
- **Fuentes de datos**: Recursos locales o remotos a los que los servidores MCP pueden acceder

## Capacidades Principales

MCP ofrece tres tipos principales de capacidades:

1. **Recursos**: Datos tipo archivo que pueden ser leídos por los clientes (como respuestas de API o contenidos de archivos)
2. **Herramientas**: Funciones que pueden ser llamadas por el LLM (con aprobación del usuario)
3. **Prompts**: Plantillas pre-escritas que ayudan a los usuarios a realizar tareas específicas

## Implementación Técnica

### Requisitos del Sistema
- Python 3.10 o superior
- Bibliotecas: `mcp[cli]`, `httpx`

### Configuración Básica de un Servidor MCP

```python
from mcp.server.fastmcp import FastMCP

# Inicializar servidor FastMCP
mcp = FastMCP("mi-servidor")

@mcp.tool()
async def mi_funcion(parametro: str) -> str:
    """Descripción de la función
    
    Args:
        parametro: Descripción del parámetro
    """
    # Implementación
    return resultado

if __name__ == "__main__":
    # Inicializar y ejecutar el servidor
    mcp.run(transport='stdio')
```

### Configuración de Claude Desktop

Archivo de configuración ubicado en:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
    "mcpServers": {
        "nombre-servidor": {
            "command": "python",
            "args": [
                "RUTA/COMPLETA/A/servidor.py"
            ]
        }
    }
}
```

## Caso de Uso: Integración con Processing

### Descripción
Implementación de un servidor MCP que permite a Claude controlar la aplicación Processing mediante comandos en lenguaje natural.

### Capacidades Implementadas
- Listar sketches disponibles
- Ejecutar sketches existentes con parámetros
- Crear nuevos sketches a través de instrucciones en lenguaje natural
- Actualizar sketches existentes

### Implementación Técnica

```python
# Configuración del servidor
PROCESSING_SKETCH_DIR = r"C:\Users\usuario\Documentos\Processing"
PROCESSING_CLI_PATH = r"C:\Ruta\a\processing-java.exe"

@mcp.tool()
async def run_sketch(sketch_name: str, params: Dict[str, Any] = {}) -> str:
    """Ejecuta un sketch de Processing con los parámetros especificados."""
    # Implementación
    
@mcp.tool()
async def list_sketches() -> str:
    """Lista todos los sketches disponibles en el directorio configurado."""
    # Implementación
    
@mcp.tool()
async def create_sketch(sketch_name: str, code: str) -> str:
    """Crea un nuevo sketch de Processing con el código proporcionado."""
    # Implementación
    
@mcp.tool()
async def update_sketch(sketch_name: str, code: str) -> str:
    """Actualiza un sketch existente con nuevo código."""
    # Implementación
```

## Flujo de Trabajo

1. El usuario realiza una consulta en lenguaje natural a Claude
2. Claude analiza la consulta y determina qué herramienta MCP utilizar
3. Claude solicita permiso al usuario para ejecutar la herramienta
4. El cliente MCP ejecuta la herramienta a través del servidor correspondiente
5. Los resultados se devuelven a Claude
6. Claude formula una respuesta en lenguaje natural basada en los resultados

## Solución de Problemas Comunes

- **Error "No module named 'mcp'"**: Instalar el módulo con `pip install "mcp[cli]" httpx`
- **Error "Server disconnected"**: Verificar que el servidor esté ejecutándose correctamente
- **Error con rutas de archivos**: Asegurarse de usar rutas absolutas y correctas
- **Problemas con Processing**: Verificar que la ruta al ejecutable `processing-java.exe` sea correcta

## Recursos Adicionales

- Documentación oficial: [MCP Documentation](https://docs.anthropic.com/claude/docs/model-context-protocol)
- Repositorio de ejemplo: [processing-claude-mcp-bridge](https://github.com/usuario/processing-claude-mcp-bridge)