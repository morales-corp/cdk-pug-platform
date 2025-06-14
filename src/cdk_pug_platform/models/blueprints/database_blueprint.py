from cdk_pug_platform.models.database.rds_capacity import RdsCapacity
from cdk_pug_platform.models.database.rds_performance import RdsPerformance


class DatabaseBlueprint:
    def __init__(self, capacity: RdsCapacity, performance: RdsPerformance):
        self.capacity = capacity
        self.performance = performance
