from enum import Enum


class InstanceFamily(Enum):
    # Uso general
    T4G = "db.t4g"  # Basadas en Graviton2
    T3 = "db.t3"
    T2 = "db.t2"
    M7G = "db.m7g"  # Basadas en Graviton3
    M6I = "db.m6i"
    M6G = "db.m6g"  # Basadas en Graviton2
    M5 = "db.m5"
    M5D = "db.m5d"  # Con almacenamiento SSD NVMe
    M4 = "db.m4"

    # Optimizadas para memoria
    R7G = "db.r7g"  # Basadas en Graviton3
    R6G = "db.r6g"  # Basadas en Graviton2
    R6I = "db.r6i"
    R5 = "db.r5"
    R4 = "db.r4"
    X2G = "db.x2g"  # Basadas en Graviton2
    X2I = "db.x2i"
    X1E = "db.x1e"
    X1 = "db.x1"
    Z1D = "db.z1d"
