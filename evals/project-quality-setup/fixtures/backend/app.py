"""Synthetic authorization fixture; no live services."""

def can_read(owner_id, actor_id):
    return owner_id == actor_id
