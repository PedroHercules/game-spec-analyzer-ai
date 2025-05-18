import psutil
import platform
import wmi
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class SystemSpecs:
    """Especificações do sistema."""
    # Campos obrigatórios
    cpu_name: str
    cpu_cores: int
    cpu_threads: int
    cpu_freq_base: float
    cpu_freq_max: float
    ram_total: int  # GB
    ram_free: int   # GB
    gpu_name: str
    disk_free: int  # GB
    disk_total: int # GB
    os_name: str
    os_version: str
    
    # Campos opcionais
    ram_speed: Optional[int] = None  # MHz
    gpu_memory: Optional[int] = None  # GB
    gpu_driver: Optional[str] = None
    directx_version: Optional[str] = None

def get_dedicated_gpu(w: wmi.WMI) -> tuple[str, Optional[int], Optional[str]]:
    """
    Busca a GPU dedicada do sistema.
    A GPU dedicada geralmente tem mais memória e é da NVIDIA ou AMD.
    
    Args:
        w: Conexão WMI
        
    Returns:
        Tupla com (nome_gpu, memoria_gpu, driver_gpu)
    """
    gpus = w.Win32_VideoController()
    
    # Ordena as GPUs por memória (maior primeiro)
    gpus_by_memory = sorted(
        [(gpu, int(gpu.AdapterRAM) if gpu.AdapterRAM else 0) for gpu in gpus],
        key=lambda x: x[1],
        reverse=True
    )
    
    for gpu, memory in gpus_by_memory:
        name = gpu.Name.lower()
        # Prioriza GPUs dedicadas conhecidas
        if "nvidia" in name or "amd" in name or "radeon" in name:
            memory_gb = round(memory / (1024**3)) if memory > 0 else None
            return gpu.Name, memory_gb, gpu.DriverVersion
    
    # Se não encontrou GPU dedicada, pega a com mais memória
    if gpus_by_memory:
        gpu, memory = gpus_by_memory[0]
        memory_gb = round(memory / (1024**3)) if memory > 0 else None
        return gpu.Name, memory_gb, gpu.DriverVersion
    
    return "GPU não detectada", None, None

def get_system_specs() -> SystemSpecs:
    """
    Coleta as especificações do sistema atual.
    
    Returns:
        SystemSpecs com as informações coletadas
    """
    # Inicializa WMI
    w = wmi.WMI()
    
    try:
        # CPU
        cpu_info = w.Win32_Processor()[0]
        cpu_name = cpu_info.Name
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_freq_base = round(cpu_freq.current, 2) if cpu_freq else 0
        cpu_freq_max = round(cpu_freq.max, 2) if cpu_freq and cpu_freq.max else cpu_freq_base
        
        # RAM
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024**3))  # Converte para GB
        ram_free = round(ram.available / (1024**3))
        
        try:
            ram_info = w.Win32_PhysicalMemory()[0]
            ram_speed = ram_info.Speed
        except:
            ram_speed = None
        
        # GPU - Busca GPU dedicada
        gpu_name, gpu_memory, gpu_driver = get_dedicated_gpu(w)
        
        # Storage
        disk = psutil.disk_usage('/')
        disk_free = round(disk.free / (1024**3))
        disk_total = round(disk.total / (1024**3))
        
        # Sistema Operacional
        os_info = platform.uname()
        os_name = os_info.system
        os_version = f"{os_info.release} ({os_info.version})"
        
        # DirectX
        try:
            # Busca a versão do DirectX no registro do Windows
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\DirectX") as key:
                directx_version = winreg.QueryValueEx(key, "Version")[0]
        except:
            directx_version = None
        
        return SystemSpecs(
            cpu_name=cpu_name,
            cpu_cores=cpu_cores,
            cpu_threads=cpu_threads,
            cpu_freq_base=cpu_freq_base,
            cpu_freq_max=cpu_freq_max,
            ram_total=ram_total,
            ram_free=ram_free,
            gpu_name=gpu_name,
            disk_free=disk_free,
            disk_total=disk_total,
            os_name=os_name,
            os_version=os_version,
            ram_speed=ram_speed,
            gpu_memory=gpu_memory,
            gpu_driver=gpu_driver,
            directx_version=directx_version
        )
    
    except Exception as e:
        print(f"Erro ao coletar especificações: {str(e)}")
        raise
