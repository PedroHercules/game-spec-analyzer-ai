import psutil
import platform
import wmi
import ctypes
from dataclasses import dataclass
from typing import Optional, Dict, List
from ctypes import windll, c_void_p, Structure, c_uint, POINTER, sizeof
from datetime import datetime

# Estruturas para DXGI
class DXGI_ADAPTER_DESC(Structure):
    _fields_ = [
        ("Description", ctypes.c_wchar * 128),
        ("VendorId", ctypes.c_uint),
        ("DeviceId", ctypes.c_uint),
        ("SubSysId", ctypes.c_uint),
        ("Revision", ctypes.c_uint),
        ("DedicatedVideoMemory", ctypes.c_size_t),
        ("DedicatedSystemMemory", ctypes.c_size_t),
        ("SharedSystemMemory", ctypes.c_size_t),
        ("AdapterLuid", ctypes.c_int64)
    ]

def format_driver_date(date_str: Optional[str]) -> Optional[str]:
    """Formata a data do driver para um formato mais legível."""
    if not date_str:
        return None
    try:
        # Converte string '20250506000000.000000-000' para datetime
        date = datetime.strptime(date_str.split('.')[0], '%Y%m%d%H%M%S')
        return date.strftime('%d/%m/%Y')
    except:
        return date_str

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
    gpu_memory_type: Optional[str] = None   # GDDR5, GDDR6, etc
    gpu_driver: Optional[str] = None
    gpu_driver_date: Optional[str] = None
    gpu_resolution: Optional[str] = None     # Máxima resolução suportada
    gpu_refresh_rate: Optional[int] = None   # Taxa de atualização máxima
    gpu_architecture: Optional[str] = None   # Arquitetura (ex: Ampere, Ada Lovelace)
    gpu_tech_support: Optional[Dict[str, bool]] = None  # Suporte a tecnologias (DLSS, Ray Tracing, etc)
    os_build: Optional[str] = None
    directx_version: Optional[str] = None

def get_gpu_memory_dxgi() -> Optional[int]:
    """
    Tenta obter a memória da GPU usando DXGI.
    """
    try:
        # Carrega as DLLs necessárias
        dxgi = windll.dxgi
        d3d11 = windll.d3d11

        # Cria o device D3D
        device = c_void_p()
        dxgi_device = c_void_p()
        dxgi_adapter = c_void_p()
        adapter_desc = DXGI_ADAPTER_DESC()

        # Tenta criar o device e obter o adaptador
        if d3d11.D3D11CreateDevice(None, 0, None, 0, None, 0, 0, ctypes.byref(device), None, None) == 0:
            device = device.value
            device.QueryInterface(dxgi_device)
            dxgi_device = dxgi_device.value
            dxgi_device.GetParent(dxgi_adapter)
            dxgi_adapter = dxgi_adapter.value
            dxgi_adapter.GetDesc(ctypes.byref(adapter_desc))

            # Converte para GB
            memory_gb = adapter_desc.DedicatedVideoMemory / (1024**3)
            return round(memory_gb)
    except Exception as e:
        print(f"Erro ao obter memória via DXGI: {e}")
    return None

def get_dedicated_gpu(w: wmi.WMI) -> tuple[str, Optional[int], Optional[str], Dict[str, any]]:
    """
    Busca a GPU dedicada do sistema e suas capacidades.
    
    Returns:
        Tupla com (nome_gpu, memoria_gpu, driver, detalhes_adicionais)
    """
    try:
        gpus = w.Win32_VideoController()
        # Filtra e ordena as GPUs por memória
        gpu_list = []
        for gpu in gpus:
            try:
                name = gpu.Name
                # Tenta obter a memória de diferentes formas
                memory = None
                
                # 1. Tenta via DXGI primeiro
                if "nvidia" in name.lower() or "amd" in name.lower():
                    memory = get_gpu_memory_dxgi()
                    print(f"DXGI Memory for {name}: {memory}GB")

                # 2. Tenta AdapterRAM
                if not memory:
                    try:
                        memory = int(gpu.AdapterRAM)
                        print(f"AdapterRAM for {name}: {memory} bytes")
                    except Exception as e:
                        print(f"Erro AdapterRAM for {name}: {e}")

                # 3. Tenta VideoMemoryType
                if not memory:
                    try:
                        memory = int(gpu.VideoMemory)
                        print(f"VideoMemory for {name}: {memory} bytes")
                    except Exception as e:
                        print(f"Erro VideoMemory for {name}: {e}")
                        
                # 4. Se não conseguiu ou o valor é inválido, define baseado no modelo
                if not memory or memory < 0:
                    name_lower = name.lower()
                    if "nvidia" in name_lower:
                        print(f"Detectando memória pelo modelo: {name}")
                        if "4090" in name_lower:
                            memory = 24 * 1024**3  # 24GB
                        elif "4080" in name_lower:
                            memory = 16 * 1024**3  # 16GB
                        elif "4070" in name_lower:
                            memory = 12 * 1024**3  # 12GB
                        elif "4060" in name_lower:
                            memory = 8 * 1024**3   # 8GB
                        elif "4050" in name_lower:
                            if "laptop" in name_lower:
                                print("Definindo RTX 4050 Laptop para 6GB GDDR6")
                                memory = 6 * 1024**3   # 6GB (laptop)
                            else:
                                memory = 8 * 1024**3   # 8GB (desktop)
                    elif "amd" in name_lower or "radeon" in name_lower:
                        if "rx 7900" in name_lower:
                            memory = 20 * 1024**3  # 20GB
                        elif "rx 7800" in name_lower:
                            memory = 16 * 1024**3  # 16GB
                        elif "rx 7700" in name_lower:
                            memory = 12 * 1024**3  # 12GB
                        elif "rx 7600" in name_lower:
                            memory = 8 * 1024**3   # 8GB

                print(f"Memória final para {name}: {memory/(1024**3) if memory else 'N/A'}GB")
                
                driver = gpu.DriverVersion
                driver_date = format_driver_date(gpu.DriverDate)
                
                # Coleta informações adicionais
                details = {
                    'memory_type': None,
                    'driver_date': driver_date,
                    'resolution': f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}" if gpu.CurrentHorizontalResolution else None,
                    'refresh_rate': gpu.CurrentRefreshRate,
                    'architecture': None,
                    'tech_support': {
                        'dlss': False,
                        'ray_tracing': False,
                        'dx12_ultimate': False,
                        'fsr': False
                    }
                }
                
                # Detecta tipo de memória e tecnologias suportadas baseado no modelo
                name_lower = name.lower()
                if "nvidia" in name_lower:
                    if "4050" in name_lower or "4060" in name_lower:
                        details['memory_type'] = "GDDR6"
                        details['architecture'] = "Ada Lovelace"
                        details['tech_support'].update({
                            'dlss': True,
                            'ray_tracing': True,
                            'dx12_ultimate': True
                        })
                    elif any(x in name_lower for x in ["4090", "4080", "4070"]):
                        details['memory_type'] = "GDDR6X"
                        details['architecture'] = "Ada Lovelace"
                        details['tech_support'].update({
                            'dlss': True,
                            'ray_tracing': True,
                            'dx12_ultimate': True
                        })
                    elif any(x in name_lower for x in ["3090", "3080"]):
                        details['memory_type'] = "GDDR6X"
                        details['architecture'] = "Ampere"
                        details['tech_support'].update({
                            'dlss': True,
                            'ray_tracing': True,
                            'dx12_ultimate': True
                        })
                    elif any(x in name_lower for x in ["3070", "3060"]):
                        details['memory_type'] = "GDDR6"
                        details['architecture'] = "Ampere"
                        details['tech_support'].update({
                            'dlss': True,
                            'ray_tracing': True,
                            'dx12_ultimate': True
                        })
                elif "amd" in name_lower or "radeon" in name_lower:
                    if "rx 7" in name_lower:
                        details['memory_type'] = "GDDR6"
                        details['architecture'] = "RDNA 3"
                        details['tech_support'].update({
                            'ray_tracing': True,
                            'dx12_ultimate': True,
                            'fsr': True
                        })
                    elif "rx 6" in name_lower:
                        details['memory_type'] = "GDDR6"
                        details['architecture'] = "RDNA 2"
                        details['tech_support'].update({
                            'ray_tracing': True,
                            'dx12_ultimate': True,
                            'fsr': True
                        })
                
                gpu_list.append((name, memory, driver, details))
            except Exception as e:
                print(f"Erro ao coletar detalhes da GPU '{name}': {e}")
                continue
        
        # Ordena por quantidade de memória
        gpu_list.sort(key=lambda x: x[1] if x[1] else 0, reverse=True)
        
        # Procura primeiro por NVIDIA ou AMD
        for name, memory, driver, details in gpu_list:
            if "nvidia" in name.lower() or "amd" in name.lower() or "radeon" in name.lower():
                return (
                    name,
                    round(memory / (1024**3)) if memory else None,
                    driver,
                    details
                )
        
        # Se não encontrou, retorna a primeira da lista
        if gpu_list:
            name, memory, driver, details = gpu_list[0]
            return (
                name,
                round(memory / (1024**3)) if memory else None,
                driver,
                details
            )
            
    except Exception as e:
        print(f"Erro ao detectar GPU: {e}")
    
    return "GPU não detectada", None, None, {}

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
    # Frequências (converte MHz para GHz)
    freq = psutil.cpu_freq()
    freq_base = round(freq.current / 1000, 2) if freq else 0
    freq_max = round((freq.max or freq.current) / 1000, 2) if freq else freq_base
    
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
        gpu_name, gpu_memory, gpu_driver, gpu_details = get_dedicated_gpu(w)
        print(f"\nGPU Final: {gpu_name}")
        print(f"Memória Final: {gpu_memory}GB")
        print(f"Detalhes: {gpu_details}\n")
        
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
            gpu_memory_type=gpu_details.get('memory_type'),
            gpu_driver=gpu_driver,
            gpu_driver_date=gpu_details.get('driver_date'),
            gpu_resolution=gpu_details.get('resolution'),
            gpu_refresh_rate=gpu_details.get('refresh_rate'),
            gpu_architecture=gpu_details.get('architecture'),
            gpu_tech_support=gpu_details.get('tech_support'),
            os_build=os_build,
            directx_version=directx_version
        )
    
    except Exception as e:
        print(f"Erro ao coletar especificações: {str(e)}")
        raise
