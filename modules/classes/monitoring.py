from gpiozero import CPUTemperature
import psutil


class CPU:

    # constructor
    def __init__(self):
        frequency = psutil.cpu_freq()
        self.temperature : float = round(CPUTemperature().temperature, ndigits=2)
        self.frequency_current : float = frequency.current
        self.frequency_min : float = frequency.min
        self.frequency_max : float = frequency.max
        self.cores : int = psutil.cpu_count()
        self.percent : float = round(psutil.cpu_percent(), ndigits=2)
        

class RAM:

    # constructor
    def __init__(self):
        ram = psutil.virtual_memory()
        self.unit : str = 'MB'
        self.total : float = round(ram.total*10**(-6), ndigits=2)
        self.available : float = round(ram.available*10**(-6), ndigits=2)
        self.percent : float = round(ram.percent, ndigits=2)
        self.used : float = round(ram.used*10**(-6), ndigits=2)
        self.active : float = round(ram.active*10**(-6), ndigits=2)
        self.shared : float = round(ram.shared*10**(-6), ndigits=2)
        self.cached : float = round(ram.cached*10**(-6), ndigits=2)
        self.slab : float = round(ram.slab*10**(-6), ndigits=2)


class DISK:

    # constructor
    def __init__(self):
        disk = psutil.disk_usage('/')
        self.unit : str = 'GB'
        self.total : float = round(disk.total*10**(-9), ndigits=2)
        self.free : float = round(disk.free*10**(-9), ndigits=2)
        self.used : float = round(disk.used*10**(-9), ndigits=2)
        self.percent : float = round(disk.percent, ndigits=2)