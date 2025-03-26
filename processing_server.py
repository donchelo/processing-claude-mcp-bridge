from typing import Any, Dict, List
import subprocess
import json
import os
from mcp.server.fastmcp import FastMCP

# Inicializar servidor FastMCP
mcp = FastMCP("processing-bridge")

# Configuración - RUTAS ACTUALIZADAS
PROCESSING_SKETCH_DIR = r"C:\Users\chelo\OneDrive\Documentos\Processing"
PROCESSING_CLI_PATH = r"C:\Users\chelo\Downloads\processing-4.3.4-windows-x64\processing-4.3.4\processing-java.exe"

@mcp.tool()
async def run_sketch(sketch_name: str, params: Dict[str, Any] = {}) -> str:
    """Ejecuta un sketch de Processing con los parámetros especificados.
    
    Args:
        sketch_name: Nombre del sketch a ejecutar (sin extensión .pde)
        params: Diccionario con parámetros a pasar al sketch
    """
    sketch_path = os.path.join(PROCESSING_SKETCH_DIR, sketch_name)
    
    # Verificar que el sketch existe
    if not os.path.exists(sketch_path):
        return f"Error: El sketch {sketch_name} no existe en {PROCESSING_SKETCH_DIR}"
    
    # Verificar que el ejecutable de Processing existe
    if not os.path.exists(PROCESSING_CLI_PATH):
        return f"Error: El ejecutable de Processing no existe en {PROCESSING_CLI_PATH}"
    
    # Construir comando para ejecutar el sketch
    cmd = [
        PROCESSING_CLI_PATH,
        f"--sketch={sketch_path}",
        "--run"
    ]
    
    # Agregar parámetros como argumentos de línea de comandos
    if params:
        param_str = json.dumps(params)
        cmd.append(f"--args={param_str}")
    
    try:
        # Ejecutar el sketch como un proceso separado
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=5)
        
        if stderr:
            stderr_text = stderr.decode('utf-8', errors='replace')
            return f"Error al ejecutar el sketch: {stderr_text}"
        
        # No esperamos a que termine ya que Processing se ejecuta en su propia ventana
        return f"Sketch {sketch_name} iniciado correctamente con parámetros: {params}"
    except subprocess.TimeoutExpired:
        # Esto es normal, significa que Processing se está ejecutando
        return f"Sketch {sketch_name} iniciado correctamente con parámetros: {params}"
    except Exception as e:
        return f"Error al ejecutar el sketch: {str(e)}"

@mcp.tool()
async def list_sketches() -> str:
    """Lista todos los sketches disponibles en el directorio configurado."""
    try:
        if not os.path.exists(PROCESSING_SKETCH_DIR):
            return f"Error: El directorio de sketches {PROCESSING_SKETCH_DIR} no existe"
        
        sketches = []
        for item in os.listdir(PROCESSING_SKETCH_DIR):
            item_path = os.path.join(PROCESSING_SKETCH_DIR, item)
            if os.path.isdir(item_path) and any(file.endswith('.pde') for file in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, file))):
                sketches.append(item)
        
        if not sketches:
            return f"No se encontraron sketches en {PROCESSING_SKETCH_DIR}."
        
        return "Sketches disponibles:\n" + "\n".join(sketches)
    except Exception as e:
        return f"Error al listar sketches: {str(e)}"

@mcp.tool()
async def create_sketch(sketch_name: str, code: str) -> str:
    """Crea un nuevo sketch de Processing con el código proporcionado.
    
    Args:
        sketch_name: Nombre para el nuevo sketch (sin extensión .pde)
        code: Código de Processing a incluir en el sketch
    """
    sketch_dir = os.path.join(PROCESSING_SKETCH_DIR, sketch_name)
    sketch_file = os.path.join(sketch_dir, f"{sketch_name}.pde")
    
    try:
        # Crear directorio si no existe
        os.makedirs(sketch_dir, exist_ok=True)
        
        # Escribir el código al archivo
        with open(sketch_file, 'w') as f:
            f.write(code)
        
        return f"Sketch {sketch_name} creado exitosamente en {sketch_dir}"
    except Exception as e:
        return f"Error al crear sketch: {str(e)}"

@mcp.tool()
async def update_sketch(sketch_name: str, code: str) -> str:
    """Actualiza un sketch existente con nuevo código.
    
    Args:
        sketch_name: Nombre del sketch a actualizar (sin extensión .pde)
        code: Nuevo código de Processing para el sketch
    """
    sketch_dir = os.path.join(PROCESSING_SKETCH_DIR, sketch_name)
    sketch_file = os.path.join(sketch_dir, f"{sketch_name}.pde")
    
    if not os.path.exists(sketch_dir):
        return f"Error: El sketch {sketch_name} no existe"
    
    try:
        # Hacer copia de seguridad del archivo existente
        if os.path.exists(sketch_file):
            backup_file = sketch_file + ".bak"
            os.rename(sketch_file, backup_file)
        
        # Escribir el nuevo código
        with open(sketch_file, 'w') as f:
            f.write(code)
        
        return f"Sketch {sketch_name} actualizado exitosamente"
    except Exception as e:
        return f"Error al actualizar sketch: {str(e)}"

if __name__ == "__main__":
    # Inicializar y ejecutar el servidor
    mcp.run(transport='stdio')