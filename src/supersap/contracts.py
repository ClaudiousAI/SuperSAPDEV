"""Shared CLI contracts; registry and agent contracts belong to TASK-002 onward."""

from enum import IntEnum, StrEnum
from typing import TypedDict


class ExitCode(IntEnum):
    SUCCESS = 0
    INVALID_INPUT = 2
    POLICY_GATE = 3
    TRANSIENT_FAILURE = 4
    INTERNAL_ERROR = 5


class EvidenceClass(StrEnum):
    STATIC = "STATIC"
    MOCK = "MOCK"
    LIVE = "LIVE"


class SmokeReport(TypedDict):
    schema_version: str
    status: str
    evidence_class: str
    fixture_sha256: str
    domains_in_scope: list[str]
    hosts_in_scope: list[str]


class CliFailure(Exception):
    """An intentionally public, redacted diagnostic and recovery instruction."""

    def __init__(self, code: ExitCode, message: str, recovery: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.recovery = recovery
