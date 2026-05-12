from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    total_systems: int
    active_systems: int
    inactive_systems: int
    total_accesses: int
    active_accesses: int
    revoked_accesses: int
    pending_accesses: int
