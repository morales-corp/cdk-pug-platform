from enum import Enum


class CrossPlatform(Enum):
    BITBUCKET = "bitbucket"
    MS_TEAMS = "ms-teams"
    POWERBI = "power-bi"


class MsTeamsSecrets(Enum):
    WEBHOOK_URL = "monitoring_webhook_url"
