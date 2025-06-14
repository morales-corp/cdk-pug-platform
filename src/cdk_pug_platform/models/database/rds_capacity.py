from pydantic import BaseModel, Field

DEFAULT_PORT_POSTGRES = 5432
DEFAULT_IOPS = 3000
DEFAULT_ALLOCATED_STORAGE = 20
DEFAULT_STORAGE_THROUGHPUT = 125


class RdsCapacity(BaseModel):
    iops: int = Field(
        default=DEFAULT_IOPS,
        ge=1000,
        le=16000,
        description="IOPS value for the database in IOPS.",
    )
    allocated_storage: int = Field(
        default=DEFAULT_ALLOCATED_STORAGE,
        ge=20,
        le=16384,
        description=("Allocated storage for the database in GiB."),
    )
    storage_throughput: int = Field(
        default=DEFAULT_STORAGE_THROUGHPUT,
        ge=0,
        le=1000,
        description="Storage throughput for the database in MiBps.",
    )
    port: int = Field(
        default=DEFAULT_PORT_POSTGRES,
        ge=1024,
        le=65535,
        description="Port number for the database.",
    )
