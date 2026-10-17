"""Hợp đồng nguồn tĩnh v1; không I/O và không tính điểm RCA."""

from .build import build, project
from .compare import compare

__all__ = ['build', 'project', 'compare']
