import psutil
import platform
import wmi
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class StorageDevice:
    """Informações de um dispositivo de armazenamento."""
    name: str
    type: str          # SSD, HDD, NVMe
    total: int         # GB
    free: int          # GB
    mount_point: str

@dataclass
class SystemSpecs:
    """Especificações detalhadas do sistema."""
    # Campos obrigatórios primeiro
    cpu_name: str
    cpu_cores: int
    cpu_threads: int
    cpu_freq_base: float
    cpu_freq_max: float
    ram_total: int          # GB
    ram_free: int          # GB
    ram_used: int          # GB
    gpu_name: str
    storage_devices: List[StorageDevice]  # Lista de dispositivos
    os_name: str
    os_version: str
    
    # Campos opcionais depois
    cpu_temp: Optional[float] = None     # °C
    cpu_load: Optional[float] = None     # %
    cpu_architecture: Optional[str] = None
    ram_speed: Optional[int] = None  # MHz
    ram_type: Optional[str] = None   # DDR4, DDR5, etc
    gpu_memory_total: Optional[int] = None  # GB
    gpu_driver: Optional[str] = None
    os_build: Optional[str] = None
    directx_version: Optional[str] = None

def get_dedicated_gpu(w: wmi.WMI) -> tuple[str, Optional[int], Optional[str]]:
    """
    Busca a GPU dedicada do sistema.
    
    Returns:
        Tupla com (nome_gpu, memoria_gpu, driver)
    """
    try:
        gpus = w.Win32_VideoController()
        # Filtra e ordena as GPUs por memória
        gpu_list = []
        for gpu in gpus:
            try:
                memory = int(gpu.AdapterRAM)
                name = gpu.Name
                driver = gpu.DriverVersion
                gpu_list.append((name, memory, driver))
            except:
                continue
        
        # Ordena por quantidade de memória
        gpu_list.sort(key=lambda x: x[1] if x[1] else 0, reverse=True)
        
        # Procura primeiro por NVIDIA ou AMD
        for name, memory, driver in gpu_list:
            if "nvidia" in name.lower() or "amd" in name.lower() or "radeon" in name.lower():
                return name, round(memory / (1024**3)) if memory else None, driver
        
        # Se não encontrou, retorna a primeira da lista
        if gpu_list:
            name, memory, driver = gpu_list[0]
            return name, round(memory / (1024**3)) if memory else None, driver
            
    except Exception as e:
        print(f"Erro ao detectar GPU: {e}")
    
    return "GPU não detectada", None, None

def get_storage_devices(w: wmi.WMI) -> List[StorageDevice]:
    """
    Obtém informações de todos os dispositivos de armazenamento.
    
    Returns:
        Lista de StorageDevice
    """
    devices = []
    
    # Mapeia os discos físicos
    physical_disks = {}
    for disk in w.Win32_DiskDrive():
        try:
            model = disk.Model.lower()
            if "nvme" in model:
                disk_type = "NVMe SSD"
            elif "ssd" in model:
                disk_type = "SSD"
            else:
                disk_type = "HDD"
            physical_disks[disk.DeviceID] = disk_type
        except:
            continue

    # Obtém as partições montadas
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            if partition.device and partition.mountpoint:
                # Encontra o tipo do disco físico correspondente
                disk_type = "Unknown"
                for physical_id, physical_type in physical_disks.items():
                    if partition.device.replace('\\', '').startswith(physical_id.replace('\\', '')):
                        disk_type = physical_type
                        break

                usage = psutil.disk_usage(partition.mountpoint)
                devices.append(StorageDevice(
                    name=partition.device,
                    type=disk_type,
                    total=round(usage.total / (1024**3)),
                    free=round(usage.free / (1024**3)),
                    mount_point=partition.mountpoint
                ))
        except:
            continue
            
    return devices

def get_cpu_stats() -> tuple[float, float, Optional[float]]:
    """
    Obtém estatísticas da CPU.
    
    Returns:
        Tupla com (freq_base, freq_max, temperatura)
    """
    # Frequências
    freq = psutil.cpu_freq()
    freq_base = round(freq.current, 2) if freq else 0
    freq_max = round(freq.max, 2) if freq and freq.max else freq_base
    
    # Temperatura (tenta diferentes métodos)
    temp = None
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            temp = temps['coretemp'][0].current
        elif 'k10temp' in temps:
            temp = temps['k10temp'][0].current
    except:
        pass
        
    return freq_base, freq_max, temp

def format_cpu_arch(arch: str) -> str:
    """Formata a arquitetura da CPU de forma mais amigável."""
    arch = arch.lower()
    if arch in ['amd64', 'x86_64']:
        return 'x64'
    elif arch == 'x86':
        return 'x86'
    elif 'arm' in arch:
        return arch.upper()
    return arch

def get_system_specs() -> SystemSpecs:
    """
    Coleta especificações detalhadas do sistema.
    
    Returns:
        SystemSpecs com todas as informações coletadas
    """
    w = wmi.WMI()
    
    try:
        # CPU
        cpu_info = w.Win32_Processor()[0]
        cpu_name = cpu_info.Name
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_freq_base, cpu_freq_max, cpu_temp = get_cpu_stats()
        cpu_arch = format_cpu_arch(platform.machine())
        cpu_load = psutil.cpu_percent(interval=1)
        
        # RAM
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024**3))
        ram_free = round(ram.available / (1024**3))
        ram_used = round(ram.used / (1024**3))
        
        try:
            ram_info = w.Win32_PhysicalMemory()[0]
            ram_speed = ram_info.Speed
            ram_type = ram_info.MemoryType
        except:
            ram_speed = None
            ram_type = None
        
        # GPU
        gpu_name, gpu_memory, gpu_driver = get_dedicated_gpu(w)
        
        # Storage
        storage_devices = get_storage_devices(w)
        
        # Sistema
        os_info = platform.uname()
        os_name = os_info.system
        os_version = os_info.release
        os_build = os_info.version
        
        # DirectX
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\DirectX") as key:
                directx_version = winreg.QueryValueEx(key, "Version")[0]
        except:
            directx_version = None
        
        return SystemSpecs(
            # Campos obrigatórios
            cpu_name=cpu_name,
            cpu_cores=cpu_cores,
            cpu_threads=cpu_threads,
            cpu_freq_base=cpu_freq_base,
            cpu_freq_max=cpu_freq_max,
            ram_total=ram_total,
            ram_free=ram_free,
            ram_used=ram_used,
            gpu_name=gpu_name,
            storage_devices=storage_devices,
            os_name=os_name,
            os_version=os_version,
            
            # Campos opcionais
            cpu_temp=cpu_temp,
            cpu_load=cpu_load,
            cpu_architecture=cpu_arch,
            ram_speed=ram_speed,
            ram_type=ram_type,
            gpu_memory_total=gpu_memory,
            gpu_driver=gpu_driver,
            os_build=os_build,
            directx_version=directx_version
        )
    
    except Exception as e:
        print(f"Erro ao coletar especificações: {str(e)}")
        raise
