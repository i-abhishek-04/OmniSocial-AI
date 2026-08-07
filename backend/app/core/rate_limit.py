"""
Shared rate limiter instance (slowapi, backed by an in-memory store).

Keyed by client IP. Auth endpoints get tighter limits since they're the
most common brute-force / credential-stuffing target.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])
