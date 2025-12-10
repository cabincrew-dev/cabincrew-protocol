from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class AggregationMethod(Enum):
    """Policy aggregation strategy.
    Defines how multiple policy decisions are combined into a final decision.
    
    Aggregation method used to combine individual policy decisions.
    REQUIRED if multiple policies were evaluated.
    Ensures deterministic aggregation across orchestrators.
    """
    ALL_ALLOW = "all_allow"
    ANY_DENY = "any_deny"
    CUSTOM = "custom"
    MAJORITY = "majority"
    MOST_RESTRICTIVE = "most_restrictive"
    UNANIMOUS = "unanimous"


@dataclass
class ApprovalReceivedData:
    approval_id: str
    approved: bool
    approver: str

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalReceivedData':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        approved = from_bool(obj.get("approved"))
        approver = from_str(obj.get("approver"))
        return ApprovalReceivedData(approval_id, approved, approver)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["approved"] = from_bool(self.approved)
        result["approver"] = from_str(self.approver)
        return result


@dataclass
class ApprovalRecord:
    """Durable approval record.
    Tracks who approved what, when, bound to specific plan-token hash.
    """
    approval_id: str
    approved: bool
    approved_at: datetime
    approver: str
    plan_token_hash: str
    step_id: str
    evidence_hashes: Optional[List[str]] = None
    reason: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalRecord':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        approved = from_bool(obj.get("approved"))
        approved_at = from_datetime(obj.get("approved_at"))
        approver = from_str(obj.get("approver"))
        plan_token_hash = from_str(obj.get("plan_token_hash"))
        step_id = from_str(obj.get("step_id"))
        evidence_hashes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("evidence_hashes"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return ApprovalRecord(approval_id, approved, approved_at, approver, plan_token_hash, step_id, evidence_hashes, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["approved"] = from_bool(self.approved)
        result["approved_at"] = self.approved_at.isoformat()
        result["approver"] = from_str(self.approver)
        result["plan_token_hash"] = from_str(self.plan_token_hash)
        result["step_id"] = from_str(self.step_id)
        if self.evidence_hashes is not None:
            result["evidence_hashes"] = from_union([lambda x: from_list(from_str, x), from_none], self.evidence_hashes)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class PreflightEvidence:
    hash: str
    name: str
    path: str

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightEvidence':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        name = from_str(obj.get("name"))
        path = from_str(obj.get("path"))
        return PreflightEvidence(hash, name, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["name"] = from_str(self.name)
        result["path"] = from_str(self.path)
        return result


@dataclass
class ApprovalRequest:
    """Request for human approval before proceeding with execution.
    
    Security: The plan_token_hash MUST be verified to match the current plan-token
    to prevent approval replay attacks against mutated plans.
    """
    approval_id: str
    plan_token_hash: str
    """SHA256 hash of the plan-token that this approval is bound to.
    REQUIRED to prevent approval replay attacks.
    The orchestrator MUST verify this matches the current plan-token before accepting
    approval.
    """
    reason: str
    required_role: str
    step_id: str
    workflow_id: str
    engine_output: Optional[Dict[str, Any]] = None
    evidence: Optional[List[PreflightEvidence]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalRequest':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        plan_token_hash = from_str(obj.get("plan_token_hash"))
        reason = from_str(obj.get("reason"))
        required_role = from_str(obj.get("required_role"))
        step_id = from_str(obj.get("step_id"))
        workflow_id = from_str(obj.get("workflow_id"))
        engine_output = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("engine_output"))
        evidence = from_union([lambda x: from_list(PreflightEvidence.from_dict, x), from_none], obj.get("evidence"))
        return ApprovalRequest(approval_id, plan_token_hash, reason, required_role, step_id, workflow_id, engine_output, evidence)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["plan_token_hash"] = from_str(self.plan_token_hash)
        result["reason"] = from_str(self.reason)
        result["required_role"] = from_str(self.required_role)
        result["step_id"] = from_str(self.step_id)
        result["workflow_id"] = from_str(self.workflow_id)
        if self.engine_output is not None:
            result["engine_output"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.engine_output)
        if self.evidence is not None:
            result["evidence"] = from_union([lambda x: from_list(lambda x: to_class(PreflightEvidence, x), x), from_none], self.evidence)
        return result


@dataclass
class ApprovalRequestedData:
    approval_id: str
    required_role: str
    step_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalRequestedData':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        required_role = from_str(obj.get("required_role"))
        step_id = from_str(obj.get("step_id"))
        return ApprovalRequestedData(approval_id, required_role, step_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["required_role"] = from_str(self.required_role)
        result["step_id"] = from_str(self.step_id)
        return result


@dataclass
class ApprovalResponse:
    approval_id: str
    approved: bool
    approver: Optional[str] = None
    reason: Optional[str] = None
    timestamp: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalResponse':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        approved = from_bool(obj.get("approved"))
        approver = from_union([from_str, from_none], obj.get("approver"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        timestamp = from_union([from_str, from_none], obj.get("timestamp"))
        return ApprovalResponse(approval_id, approved, approver, reason, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["approved"] = from_bool(self.approved)
        if self.approver is not None:
            result["approver"] = from_union([from_str, from_none], self.approver)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.timestamp is not None:
            result["timestamp"] = from_union([from_str, from_none], self.timestamp)
        return result


@dataclass
class Artifact:
    """Canonical artifact interface.
    Defined in schemas/draft/artifact.schema.json
    """
    action: str
    """Operation to perform with this artifact (create, update, delete, apply, execute, etc).
    Free-form and engine-defined.
    """
    artifact_type: str
    """Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined."""

    mime: str
    """MIME type describing content."""

    body: Optional[Union[Dict[str, Any], List[Any], str]] = None
    """Inline content for small artifacts.
    Can be string, object, array, or null.
    """
    body_file: Optional[str] = None
    """Indicates an external data file within the artifact directory."""

    metadata: Optional[Dict[str, Any]] = None
    """Arbitrary metadata. Optional."""

    target: Optional[str] = None
    """Path, resource, or identifier this artifact applies to. Optional."""

    @staticmethod
    def from_dict(obj: Any) -> 'Artifact':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        artifact_type = from_str(obj.get("artifact_type"))
        mime = from_str(obj.get("mime"))
        body = from_union([lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_none, from_str], obj.get("body"))
        body_file = from_union([from_str, from_none], obj.get("body_file"))
        metadata = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("metadata"))
        target = from_union([from_str, from_none], obj.get("target"))
        return Artifact(action, artifact_type, mime, body, body_file, metadata, target)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["artifact_type"] = from_str(self.artifact_type)
        result["mime"] = from_str(self.mime)
        if self.body is not None:
            result["body"] = from_union([lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_none, from_str], self.body)
        if self.body_file is not None:
            result["body_file"] = from_union([from_str, from_none], self.body_file)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.metadata)
        if self.target is not None:
            result["target"] = from_union([from_str, from_none], self.target)
        return result


@dataclass
class ArtifactCreatedData:
    artifact_hash: str
    artifact_id: str
    artifact_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'ArtifactCreatedData':
        assert isinstance(obj, dict)
        artifact_hash = from_str(obj.get("artifact_hash"))
        artifact_id = from_str(obj.get("artifact_id"))
        artifact_type = from_str(obj.get("artifact_type"))
        return ArtifactCreatedData(artifact_hash, artifact_id, artifact_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artifact_hash"] = from_str(self.artifact_hash)
        result["artifact_id"] = from_str(self.artifact_id)
        result["artifact_type"] = from_str(self.artifact_type)
        return result


@dataclass
class ArtifactRecord:
    """Durable artifact record.
    Tracks artifacts with SHA256 hashes for integrity verification.
    """
    artifact_hash: str
    artifact_id: str
    artifact_type: str
    created_at: datetime
    step_id: str
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ArtifactRecord':
        assert isinstance(obj, dict)
        artifact_hash = from_str(obj.get("artifact_hash"))
        artifact_id = from_str(obj.get("artifact_id"))
        artifact_type = from_str(obj.get("artifact_type"))
        created_at = from_datetime(obj.get("created_at"))
        step_id = from_str(obj.get("step_id"))
        metadata = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("metadata"))
        return ArtifactRecord(artifact_hash, artifact_id, artifact_type, created_at, step_id, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artifact_hash"] = from_str(self.artifact_hash)
        result["artifact_id"] = from_str(self.artifact_id)
        result["artifact_type"] = from_str(self.artifact_type)
        result["created_at"] = self.created_at.isoformat()
        result["step_id"] = from_str(self.step_id)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.metadata)
        return result


@dataclass
class AuditApproval:
    """Audit record for approval events.
    Extended to ensure approval binding is auditable.
    """
    approval_id: str
    """Unique approval identifier.
    REQUIRED to correlate request and response.
    """
    approved: bool
    """Whether approval was granted.
    REQUIRED for audit trail.
    """
    approver: str
    """Identity of the approver.
    REQUIRED for accountability.
    """
    plan_token_hash: str
    """SHA256 hash of the plan-token this approval is bound to.
    REQUIRED to prove approval binding and prevent replay attacks.
    """
    required_role: str
    """Required role for this approval.
    REQUIRED to verify authorization.
    """
    timestamp: datetime
    """ISO 8601 timestamp when approval was granted/denied.
    REQUIRED for temporal ordering.
    """
    reason: Optional[str] = None
    """Optional reason for approval/denial."""

    @staticmethod
    def from_dict(obj: Any) -> 'AuditApproval':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        approved = from_bool(obj.get("approved"))
        approver = from_str(obj.get("approver"))
        plan_token_hash = from_str(obj.get("plan_token_hash"))
        required_role = from_str(obj.get("required_role"))
        timestamp = from_datetime(obj.get("timestamp"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return AuditApproval(approval_id, approved, approver, plan_token_hash, required_role, timestamp, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["approved"] = from_bool(self.approved)
        result["approver"] = from_str(self.approver)
        result["plan_token_hash"] = from_str(self.plan_token_hash)
        result["required_role"] = from_str(self.required_role)
        result["timestamp"] = self.timestamp.isoformat()
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class AuditArtifact:
    hash: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    role: Optional[str] = None
    size: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditArtifact':
        assert isinstance(obj, dict)
        hash = from_union([from_str, from_none], obj.get("hash"))
        name = from_union([from_str, from_none], obj.get("name"))
        path = from_union([from_str, from_none], obj.get("path"))
        role = from_union([from_str, from_none], obj.get("role"))
        size = from_union([from_float, from_none], obj.get("size"))
        return AuditArtifact(hash, name, path, role, size)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.hash is not None:
            result["hash"] = from_union([from_str, from_none], self.hash)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.path is not None:
            result["path"] = from_union([from_str, from_none], self.path)
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        return result


@dataclass
class AuditEngine:
    engine_id: Optional[str] = None
    error: Optional[str] = None
    receipt_id: Optional[str] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditEngine':
        assert isinstance(obj, dict)
        engine_id = from_union([from_str, from_none], obj.get("engine_id"))
        error = from_union([from_str, from_none], obj.get("error"))
        receipt_id = from_union([from_str, from_none], obj.get("receipt_id"))
        status = from_union([from_str, from_none], obj.get("status"))
        return AuditEngine(engine_id, error, receipt_id, status)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.engine_id is not None:
            result["engine_id"] = from_union([from_str, from_none], self.engine_id)
        if self.error is not None:
            result["error"] = from_union([from_str, from_none], self.error)
        if self.receipt_id is not None:
            result["receipt_id"] = from_union([from_str, from_none], self.receipt_id)
        if self.status is not None:
            result["status"] = from_union([from_str, from_none], self.status)
        return result


class Decision(Enum):
    """Final aggregated decision after all policy evaluations.
    REQUIRED for chain-of-custody.
    
    Decision from this specific policy.
    """
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    WARN = "warn"


@dataclass
class AuditGateway:
    gateway_type: Optional[str] = None
    model: Optional[str] = None
    policy_decision: Optional[Decision] = None
    request_id: Optional[str] = None
    tool: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditGateway':
        assert isinstance(obj, dict)
        gateway_type = from_union([from_str, from_none], obj.get("gateway_type"))
        model = from_union([from_str, from_none], obj.get("model"))
        policy_decision = from_union([Decision, from_none], obj.get("policy_decision"))
        request_id = from_union([from_str, from_none], obj.get("request_id"))
        tool = from_union([from_str, from_none], obj.get("tool"))
        return AuditGateway(gateway_type, model, policy_decision, request_id, tool)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.gateway_type is not None:
            result["gateway_type"] = from_union([from_str, from_none], self.gateway_type)
        if self.model is not None:
            result["model"] = from_union([from_str, from_none], self.model)
        if self.policy_decision is not None:
            result["policy_decision"] = from_union([lambda x: to_enum(Decision, x), from_none], self.policy_decision)
        if self.request_id is not None:
            result["request_id"] = from_union([from_str, from_none], self.request_id)
        if self.tool is not None:
            result["tool"] = from_union([from_str, from_none], self.tool)
        return result


@dataclass
class AuditIntegrity:
    actual_plan_token: Optional[str] = None
    artifacts_match: Optional[bool] = None
    differences: Optional[List[str]] = None
    expected_plan_token: Optional[str] = None
    plan_token_match: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditIntegrity':
        assert isinstance(obj, dict)
        actual_plan_token = from_union([from_str, from_none], obj.get("actual_plan_token"))
        artifacts_match = from_union([from_bool, from_none], obj.get("artifacts_match"))
        differences = from_union([lambda x: from_list(from_str, x), from_none], obj.get("differences"))
        expected_plan_token = from_union([from_str, from_none], obj.get("expected_plan_token"))
        plan_token_match = from_union([from_bool, from_none], obj.get("plan_token_match"))
        return AuditIntegrity(actual_plan_token, artifacts_match, differences, expected_plan_token, plan_token_match)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.actual_plan_token is not None:
            result["actual_plan_token"] = from_union([from_str, from_none], self.actual_plan_token)
        if self.artifacts_match is not None:
            result["artifacts_match"] = from_union([from_bool, from_none], self.artifacts_match)
        if self.differences is not None:
            result["differences"] = from_union([lambda x: from_list(from_str, x), from_none], self.differences)
        if self.expected_plan_token is not None:
            result["expected_plan_token"] = from_union([from_str, from_none], self.expected_plan_token)
        if self.plan_token_match is not None:
            result["plan_token_match"] = from_union([from_bool, from_none], self.plan_token_match)
        return result


@dataclass
class PlanArtifactHash:
    hash: str
    name: str
    size: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PlanArtifactHash':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        name = from_str(obj.get("name"))
        size = from_union([from_float, from_none], obj.get("size"))
        return PlanArtifactHash(hash, name, size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["name"] = from_str(self.name)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        return result


@dataclass
class PlanToken:
    """Plan-token binds artifacts to subsequent take-off.
    Extended with version and governance provenance for safe upgrades and auditability.
    """
    artifacts: List[PlanArtifactHash]
    """Per-artifact hashes that contributed to this plan token."""

    created_at: datetime
    """Timestamp when the plan was created (RFC3339)."""

    engine_id: str
    """Engine identity that produced this plan."""

    model: str
    """AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').
    Required for provenance.
    """
    protocol_version: str
    """Engine protocol version used when this plan was produced."""

    token: str
    """Primary plan token identifier, e.g. SHA256 over all plan artifacts + context."""

    version: str
    """Plan-token format version.
    REQUIRED for forward-compatibility handshake in mixed-version deployments.
    Format: "1", "2", etc. (semantic versioning for plan-token structure)
    """
    workspace_hash: str
    """Hash of the workspace state when the plan was created."""

    governance_hash: Optional[str] = None
    """SHA256 hash of governance context (OPA policies, ONNX models, gateway rules).
    OPTIONAL but recommended for compliance verification.
    Enables auditors to verify governance configuration at plan-time.
    """
    policy_digest: Optional[str] = None
    """SHA256 digest of all policy configurations evaluated during flight-plan.
    OPTIONAL but recommended for governance provenance.
    Proves which policy set was active when plan-token was created.
    """

    @staticmethod
    def from_dict(obj: Any) -> 'PlanToken':
        assert isinstance(obj, dict)
        artifacts = from_list(PlanArtifactHash.from_dict, obj.get("artifacts"))
        created_at = from_datetime(obj.get("created_at"))
        engine_id = from_str(obj.get("engine_id"))
        model = from_str(obj.get("model"))
        protocol_version = from_str(obj.get("protocol_version"))
        token = from_str(obj.get("token"))
        version = from_str(obj.get("version"))
        workspace_hash = from_str(obj.get("workspace_hash"))
        governance_hash = from_union([from_str, from_none], obj.get("governance_hash"))
        policy_digest = from_union([from_str, from_none], obj.get("policy_digest"))
        return PlanToken(artifacts, created_at, engine_id, model, protocol_version, token, version, workspace_hash, governance_hash, policy_digest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artifacts"] = from_list(lambda x: to_class(PlanArtifactHash, x), self.artifacts)
        result["created_at"] = self.created_at.isoformat()
        result["engine_id"] = from_str(self.engine_id)
        result["model"] = from_str(self.model)
        result["protocol_version"] = from_str(self.protocol_version)
        result["token"] = from_str(self.token)
        result["version"] = from_str(self.version)
        result["workspace_hash"] = from_str(self.workspace_hash)
        if self.governance_hash is not None:
            result["governance_hash"] = from_union([from_str, from_none], self.governance_hash)
        if self.policy_digest is not None:
            result["policy_digest"] = from_union([from_str, from_none], self.policy_digest)
        return result


class Source(Enum):
    """Policy source type."""

    CUSTOM = "custom"
    LLM_GATEWAY = "llm_gateway"
    MCP_GATEWAY = "mcp_gateway"
    ONNX = "onnx"
    OPA = "opa"


@dataclass
class PolicyEvaluation:
    """Individual policy evaluation result.
    Captures decision source and evidence.
    """
    decision: Decision
    """Decision from this specific policy."""

    evaluated_at: datetime
    """Evaluation timestamp."""

    policy_id: str
    """Policy identifier (e.g., OPA policy name, ONNX model name)."""

    severity: float
    """Decision severity for aggregation ordering.
    0=allow, 1=warn, 2=require_approval, 3=deny
    REQUIRED for deterministic "most restrictive" aggregation.
    """
    source: Source
    """Policy source type."""

    evidence: Optional[Dict[str, Any]] = None
    """Evidence supporting this decision (e.g., rule matches, model scores)."""

    reason: Optional[str] = None
    """Reason for this decision."""

    @staticmethod
    def from_dict(obj: Any) -> 'PolicyEvaluation':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        evaluated_at = from_datetime(obj.get("evaluated_at"))
        policy_id = from_str(obj.get("policy_id"))
        severity = from_float(obj.get("severity"))
        source = Source(obj.get("source"))
        evidence = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("evidence"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return PolicyEvaluation(decision, evaluated_at, policy_id, severity, source, evidence, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        result["evaluated_at"] = self.evaluated_at.isoformat()
        result["policy_id"] = from_str(self.policy_id)
        result["severity"] = to_float(self.severity)
        result["source"] = to_enum(Source, self.source)
        if self.evidence is not None:
            result["evidence"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.evidence)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class AuditPolicy:
    """Policy evaluation audit record.
    Extended to support chain-of-custody reconstruction.
    """
    decision: Decision
    """Final aggregated decision after all policy evaluations.
    REQUIRED for chain-of-custody.
    """
    workflow_state: str
    """Workflow state when this policy evaluation occurred.
    REQUIRED for temporal chain-of-custody.
    """
    aggregation_method: Optional[AggregationMethod] = None
    """Aggregation method used to combine individual policy decisions.
    REQUIRED if multiple policies were evaluated.
    Ensures deterministic aggregation across orchestrators.
    """
    engine: Optional[str] = None
    """Legacy field for backward compatibility."""

    policy_evaluations: Optional[List[PolicyEvaluation]] = None
    """Individual policy evaluation results.
    Captures which specific policies (OPA/ONNX/gateway) produced which decisions.
    """
    violations: Optional[List[str]] = None
    """Policy violations detected."""

    warnings: Optional[List[str]] = None
    """Policy warnings (non-blocking)."""

    @staticmethod
    def from_dict(obj: Any) -> 'AuditPolicy':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        workflow_state = from_str(obj.get("workflow_state"))
        aggregation_method = from_union([AggregationMethod, from_none], obj.get("aggregation_method"))
        engine = from_union([from_str, from_none], obj.get("engine"))
        policy_evaluations = from_union([lambda x: from_list(PolicyEvaluation.from_dict, x), from_none], obj.get("policy_evaluations"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return AuditPolicy(decision, workflow_state, aggregation_method, engine, policy_evaluations, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        result["workflow_state"] = from_str(self.workflow_state)
        if self.aggregation_method is not None:
            result["aggregation_method"] = from_union([lambda x: to_enum(AggregationMethod, x), from_none], self.aggregation_method)
        if self.engine is not None:
            result["engine"] = from_union([from_str, from_none], self.engine)
        if self.policy_evaluations is not None:
            result["policy_evaluations"] = from_union([lambda x: from_list(lambda x: to_class(PolicyEvaluation, x), x), from_none], self.policy_evaluations)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


class Severity(Enum):
    CRITICAL = "critical"
    DEBUG = "debug"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


@dataclass
class AuditWorkflow:
    mode: Optional[str] = None
    step_id: Optional[str] = None
    workflow_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditWorkflow':
        assert isinstance(obj, dict)
        mode = from_union([from_str, from_none], obj.get("mode"))
        step_id = from_union([from_str, from_none], obj.get("step_id"))
        workflow_id = from_union([from_str, from_none], obj.get("workflow_id"))
        return AuditWorkflow(mode, step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.mode is not None:
            result["mode"] = from_union([from_str, from_none], self.mode)
        if self.step_id is not None:
            result["step_id"] = from_union([from_str, from_none], self.step_id)
        if self.workflow_id is not None:
            result["workflow_id"] = from_union([from_str, from_none], self.workflow_id)
        return result


@dataclass
class AuditEvent:
    """Canonical schema for all audit log events.
    Defined in schemas/draft/audit-event.schema.json
    """
    event_id: str
    """Unique identifier for this audit event."""

    event_type: str
    """Free-form event category."""

    timestamp: datetime
    """RFC3339 timestamp of when the event occurred."""

    workflow_state: str
    """Workflow state when this event was emitted.
    REQUIRED for temporal chain-of-custody reconstruction.
    """
    approval: Optional[AuditApproval] = None
    """Audit record for approval events.
    Extended to ensure approval binding is auditable.
    """
    artifacts: Optional[List[AuditArtifact]] = None
    chain_hash: Optional[str] = None
    """Hash of the previous event in the chain. Allows for ledger-style verification."""

    engine: Optional[AuditEngine] = None
    gateway: Optional[AuditGateway] = None
    integrity_check: Optional[AuditIntegrity] = None
    message: Optional[str] = None
    plan_token: Optional[PlanToken] = None
    """Plan-token binds artifacts to subsequent take-off.
    Extended with version and governance provenance for safe upgrades and auditability.
    """
    policy: Optional[AuditPolicy] = None
    """Policy evaluation audit record.
    Extended to support chain-of-custody reconstruction.
    """
    severity: Optional[Severity] = None
    signature: Optional[str] = None
    """Cryptographic signature of this event hash."""

    signature_key_ref: Optional[str] = None
    """Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod')."""

    workflow: Optional[AuditWorkflow] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AuditEvent':
        assert isinstance(obj, dict)
        event_id = from_str(obj.get("event_id"))
        event_type = from_str(obj.get("event_type"))
        timestamp = from_datetime(obj.get("timestamp"))
        workflow_state = from_str(obj.get("workflow_state"))
        approval = from_union([AuditApproval.from_dict, from_none], obj.get("approval"))
        artifacts = from_union([lambda x: from_list(AuditArtifact.from_dict, x), from_none], obj.get("artifacts"))
        chain_hash = from_union([from_str, from_none], obj.get("chain_hash"))
        engine = from_union([AuditEngine.from_dict, from_none], obj.get("engine"))
        gateway = from_union([AuditGateway.from_dict, from_none], obj.get("gateway"))
        integrity_check = from_union([AuditIntegrity.from_dict, from_none], obj.get("integrity_check"))
        message = from_union([from_str, from_none], obj.get("message"))
        plan_token = from_union([PlanToken.from_dict, from_none], obj.get("plan_token"))
        policy = from_union([AuditPolicy.from_dict, from_none], obj.get("policy"))
        severity = from_union([Severity, from_none], obj.get("severity"))
        signature = from_union([from_str, from_none], obj.get("signature"))
        signature_key_ref = from_union([from_str, from_none], obj.get("signature_key_ref"))
        workflow = from_union([AuditWorkflow.from_dict, from_none], obj.get("workflow"))
        return AuditEvent(event_id, event_type, timestamp, workflow_state, approval, artifacts, chain_hash, engine, gateway, integrity_check, message, plan_token, policy, severity, signature, signature_key_ref, workflow)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event_id"] = from_str(self.event_id)
        result["event_type"] = from_str(self.event_type)
        result["timestamp"] = self.timestamp.isoformat()
        result["workflow_state"] = from_str(self.workflow_state)
        if self.approval is not None:
            result["approval"] = from_union([lambda x: to_class(AuditApproval, x), from_none], self.approval)
        if self.artifacts is not None:
            result["artifacts"] = from_union([lambda x: from_list(lambda x: to_class(AuditArtifact, x), x), from_none], self.artifacts)
        if self.chain_hash is not None:
            result["chain_hash"] = from_union([from_str, from_none], self.chain_hash)
        if self.engine is not None:
            result["engine"] = from_union([lambda x: to_class(AuditEngine, x), from_none], self.engine)
        if self.gateway is not None:
            result["gateway"] = from_union([lambda x: to_class(AuditGateway, x), from_none], self.gateway)
        if self.integrity_check is not None:
            result["integrity_check"] = from_union([lambda x: to_class(AuditIntegrity, x), from_none], self.integrity_check)
        if self.message is not None:
            result["message"] = from_union([from_str, from_none], self.message)
        if self.plan_token is not None:
            result["plan_token"] = from_union([lambda x: to_class(PlanToken, x), from_none], self.plan_token)
        if self.policy is not None:
            result["policy"] = from_union([lambda x: to_class(AuditPolicy, x), from_none], self.policy)
        if self.severity is not None:
            result["severity"] = from_union([lambda x: to_enum(Severity, x), from_none], self.severity)
        if self.signature is not None:
            result["signature"] = from_union([from_str, from_none], self.signature)
        if self.signature_key_ref is not None:
            result["signature_key_ref"] = from_union([from_str, from_none], self.signature_key_ref)
        if self.workflow is not None:
            result["workflow"] = from_union([lambda x: to_class(AuditWorkflow, x), from_none], self.workflow)
        return result


@dataclass
class EngineArtifact:
    hash: str
    name: str
    path: str
    role: str
    size: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EngineArtifact':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        name = from_str(obj.get("name"))
        path = from_str(obj.get("path"))
        role = from_str(obj.get("role"))
        size = from_union([from_float, from_none], obj.get("size"))
        return EngineArtifact(hash, name, path, role, size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["name"] = from_str(self.name)
        result["path"] = from_str(self.path)
        result["role"] = from_str(self.role)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        return result


@dataclass
class EngineMeta:
    step_id: str
    workflow_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'EngineMeta':
        assert isinstance(obj, dict)
        step_id = from_str(obj.get("step_id"))
        workflow_id = from_str(obj.get("workflow_id"))
        return EngineMeta(step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["step_id"] = from_str(self.step_id)
        result["workflow_id"] = from_str(self.workflow_id)
        return result


class Mode(Enum):
    """Execution mode: 'flight-plan' or 'take-off'."""

    FLIGHT_PLAN = "flight-plan"
    TAKE_OFF = "take-off"


@dataclass
class EngineOrchestrator:
    artifacts_salt: Optional[str] = None
    run_index: Optional[float] = None
    workspace_hash: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EngineOrchestrator':
        assert isinstance(obj, dict)
        artifacts_salt = from_union([from_str, from_none], obj.get("artifacts_salt"))
        run_index = from_union([from_float, from_none], obj.get("run_index"))
        workspace_hash = from_union([from_str, from_none], obj.get("workspace_hash"))
        return EngineOrchestrator(artifacts_salt, run_index, workspace_hash)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.artifacts_salt is not None:
            result["artifacts_salt"] = from_union([from_str, from_none], self.artifacts_salt)
        if self.run_index is not None:
            result["run_index"] = from_union([to_float, from_none], self.run_index)
        if self.workspace_hash is not None:
            result["workspace_hash"] = from_union([from_str, from_none], self.workspace_hash)
        return result


@dataclass
class EngineInput:
    """Input delivered via STDIN or CABINCREW_INPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    meta: EngineMeta
    mode: Mode
    """Execution mode: 'flight-plan' or 'take-off'."""

    protocol_version: str
    allowed_secrets: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    expected_plan_token: Optional[str] = None
    identity_token: Optional[str] = None
    """Ephemeral identity token (e.g. OIDC, JWT) for the workload.
    Preferred over static secrets.
    """
    orchestrator: Optional[EngineOrchestrator] = None
    secrets: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EngineInput':
        assert isinstance(obj, dict)
        meta = EngineMeta.from_dict(obj.get("meta"))
        mode = Mode(obj.get("mode"))
        protocol_version = from_str(obj.get("protocol_version"))
        allowed_secrets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("allowed_secrets"))
        config = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("config"))
        context = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("context"))
        expected_plan_token = from_union([from_str, from_none], obj.get("expected_plan_token"))
        identity_token = from_union([from_str, from_none], obj.get("identity_token"))
        orchestrator = from_union([EngineOrchestrator.from_dict, from_none], obj.get("orchestrator"))
        secrets = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("secrets"))
        return EngineInput(meta, mode, protocol_version, allowed_secrets, config, context, expected_plan_token, identity_token, orchestrator, secrets)

    def to_dict(self) -> dict:
        result: dict = {}
        result["meta"] = to_class(EngineMeta, self.meta)
        result["mode"] = to_enum(Mode, self.mode)
        result["protocol_version"] = from_str(self.protocol_version)
        if self.allowed_secrets is not None:
            result["allowed_secrets"] = from_union([lambda x: from_list(from_str, x), from_none], self.allowed_secrets)
        if self.config is not None:
            result["config"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.config)
        if self.context is not None:
            result["context"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.context)
        if self.expected_plan_token is not None:
            result["expected_plan_token"] = from_union([from_str, from_none], self.expected_plan_token)
        if self.identity_token is not None:
            result["identity_token"] = from_union([from_str, from_none], self.identity_token)
        if self.orchestrator is not None:
            result["orchestrator"] = from_union([lambda x: to_class(EngineOrchestrator, x), from_none], self.orchestrator)
        if self.secrets is not None:
            result["secrets"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.secrets)
        return result


@dataclass
class EngineMetric:
    name: str
    value: float
    tags: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EngineMetric':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        value = from_float(obj.get("value"))
        tags = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("tags"))
        return EngineMetric(name, value, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["value"] = to_float(self.value)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.tags)
        return result


class Status(Enum):
    """Execution status: 'success' or 'failure'."""

    FAILURE = "failure"
    SUCCESS = "success"


@dataclass
class EngineOutput:
    """Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    engine_id: str
    mode: Mode
    protocol_version: str
    receipt_id: str
    status: Status
    """Execution status: 'success' or 'failure'."""

    artifacts: Optional[List[EngineArtifact]] = None
    diagnostics: Any
    error: Optional[str] = None
    metrics: Optional[List[EngineMetric]] = None
    plan_token: Optional[str] = None
    """SHA256 hash referencing a plan-token.json file."""

    warnings: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EngineOutput':
        assert isinstance(obj, dict)
        engine_id = from_str(obj.get("engine_id"))
        mode = Mode(obj.get("mode"))
        protocol_version = from_str(obj.get("protocol_version"))
        receipt_id = from_str(obj.get("receipt_id"))
        status = Status(obj.get("status"))
        artifacts = from_union([lambda x: from_list(EngineArtifact.from_dict, x), from_none], obj.get("artifacts"))
        diagnostics = obj.get("diagnostics")
        error = from_union([from_str, from_none], obj.get("error"))
        metrics = from_union([lambda x: from_list(EngineMetric.from_dict, x), from_none], obj.get("metrics"))
        plan_token = from_union([from_str, from_none], obj.get("plan_token"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return EngineOutput(engine_id, mode, protocol_version, receipt_id, status, artifacts, diagnostics, error, metrics, plan_token, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["engine_id"] = from_str(self.engine_id)
        result["mode"] = to_enum(Mode, self.mode)
        result["protocol_version"] = from_str(self.protocol_version)
        result["receipt_id"] = from_str(self.receipt_id)
        result["status"] = to_enum(Status, self.status)
        if self.artifacts is not None:
            result["artifacts"] = from_union([lambda x: from_list(lambda x: to_class(EngineArtifact, x), x), from_none], self.artifacts)
        if self.diagnostics is not None:
            result["diagnostics"] = self.diagnostics
        if self.error is not None:
            result["error"] = from_union([from_str, from_none], self.error)
        if self.metrics is not None:
            result["metrics"] = from_union([lambda x: from_list(lambda x: to_class(EngineMetric, x), x), from_none], self.metrics)
        if self.plan_token is not None:
            result["plan_token"] = from_union([from_str, from_none], self.plan_token)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


@dataclass
class GatewayApproval:
    approval_id: Optional[str] = None
    reason: Optional[str] = None
    required_role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GatewayApproval':
        assert isinstance(obj, dict)
        approval_id = from_union([from_str, from_none], obj.get("approval_id"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        required_role = from_union([from_str, from_none], obj.get("required_role"))
        return GatewayApproval(approval_id, reason, required_role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval_id is not None:
            result["approval_id"] = from_union([from_str, from_none], self.approval_id)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.required_role is not None:
            result["required_role"] = from_union([from_str, from_none], self.required_role)
        return result


@dataclass
class LLMGatewayRule:
    action: str
    match: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayRule':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        match = from_dict(lambda x: x, obj.get("match"))
        metadata = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("metadata"))
        return LLMGatewayRule(action, match, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["match"] = from_dict(lambda x: x, self.match)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.metadata)
        return result


@dataclass
class LLMGatewayPolicyConfig:
    model_routing: Optional[Dict[str, Any]] = None
    onnx_models: Optional[List[str]] = None
    opa_policies: Optional[List[str]] = None
    rules: Optional[List[LLMGatewayRule]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayPolicyConfig':
        assert isinstance(obj, dict)
        model_routing = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("model_routing"))
        onnx_models = from_union([lambda x: from_list(from_str, x), from_none], obj.get("onnx_models"))
        opa_policies = from_union([lambda x: from_list(from_str, x), from_none], obj.get("opa_policies"))
        rules = from_union([lambda x: from_list(LLMGatewayRule.from_dict, x), from_none], obj.get("rules"))
        return LLMGatewayPolicyConfig(model_routing, onnx_models, opa_policies, rules)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.model_routing is not None:
            result["model_routing"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.model_routing)
        if self.onnx_models is not None:
            result["onnx_models"] = from_union([lambda x: from_list(from_str, x), from_none], self.onnx_models)
        if self.opa_policies is not None:
            result["opa_policies"] = from_union([lambda x: from_list(from_str, x), from_none], self.opa_policies)
        if self.rules is not None:
            result["rules"] = from_union([lambda x: from_list(lambda x: to_class(LLMGatewayRule, x), x), from_none], self.rules)
        return result


@dataclass
class LLMGatewayRequest:
    input: Dict[str, Any]
    model: str
    request_id: str
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None
    provider: Optional[str] = None
    source: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayRequest':
        assert isinstance(obj, dict)
        input = from_dict(lambda x: x, obj.get("input"))
        model = from_str(obj.get("model"))
        request_id = from_str(obj.get("request_id"))
        timestamp = from_datetime(obj.get("timestamp"))
        context = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("context"))
        provider = from_union([from_str, from_none], obj.get("provider"))
        source = from_union([from_str, from_none], obj.get("source"))
        return LLMGatewayRequest(input, model, request_id, timestamp, context, provider, source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["input"] = from_dict(lambda x: x, self.input)
        result["model"] = from_str(self.model)
        result["request_id"] = from_str(self.request_id)
        result["timestamp"] = self.timestamp.isoformat()
        if self.context is not None:
            result["context"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.context)
        if self.provider is not None:
            result["provider"] = from_union([from_str, from_none], self.provider)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        return result


@dataclass
class LLMGatewayResponse:
    decision: Decision
    request_id: str
    timestamp: datetime
    approval: Optional[GatewayApproval] = None
    gateway_payload: Optional[Dict[str, Any]] = None
    rewritten_input: Optional[Dict[str, Any]] = None
    routed_model: Optional[str] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayResponse':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        request_id = from_str(obj.get("request_id"))
        timestamp = from_datetime(obj.get("timestamp"))
        approval = from_union([GatewayApproval.from_dict, from_none], obj.get("approval"))
        gateway_payload = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("gateway_payload"))
        rewritten_input = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("rewritten_input"))
        routed_model = from_union([from_str, from_none], obj.get("routed_model"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return LLMGatewayResponse(decision, request_id, timestamp, approval, gateway_payload, rewritten_input, routed_model, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        result["request_id"] = from_str(self.request_id)
        result["timestamp"] = self.timestamp.isoformat()
        if self.approval is not None:
            result["approval"] = from_union([lambda x: to_class(GatewayApproval, x), from_none], self.approval)
        if self.gateway_payload is not None:
            result["gateway_payload"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.gateway_payload)
        if self.rewritten_input is not None:
            result["rewritten_input"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.rewritten_input)
        if self.routed_model is not None:
            result["routed_model"] = from_union([from_str, from_none], self.routed_model)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


@dataclass
class MCPGatewayRule:
    action: str
    match: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayRule':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        match = from_dict(lambda x: x, obj.get("match"))
        metadata = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("metadata"))
        return MCPGatewayRule(action, match, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["match"] = from_dict(lambda x: x, self.match)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.metadata)
        return result


@dataclass
class MCPGatewayPolicyConfig:
    onnx_models: Optional[List[str]] = None
    opa_policies: Optional[List[str]] = None
    rules: Optional[List[MCPGatewayRule]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayPolicyConfig':
        assert isinstance(obj, dict)
        onnx_models = from_union([lambda x: from_list(from_str, x), from_none], obj.get("onnx_models"))
        opa_policies = from_union([lambda x: from_list(from_str, x), from_none], obj.get("opa_policies"))
        rules = from_union([lambda x: from_list(MCPGatewayRule.from_dict, x), from_none], obj.get("rules"))
        return MCPGatewayPolicyConfig(onnx_models, opa_policies, rules)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.onnx_models is not None:
            result["onnx_models"] = from_union([lambda x: from_list(from_str, x), from_none], self.onnx_models)
        if self.opa_policies is not None:
            result["opa_policies"] = from_union([lambda x: from_list(from_str, x), from_none], self.opa_policies)
        if self.rules is not None:
            result["rules"] = from_union([lambda x: from_list(lambda x: to_class(MCPGatewayRule, x), x), from_none], self.rules)
        return result


@dataclass
class MCPGatewayRequest:
    method: str
    request_id: str
    server_id: str
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayRequest':
        assert isinstance(obj, dict)
        method = from_str(obj.get("method"))
        request_id = from_str(obj.get("request_id"))
        server_id = from_str(obj.get("server_id"))
        timestamp = from_datetime(obj.get("timestamp"))
        context = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("context"))
        params = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("params"))
        source = from_union([from_str, from_none], obj.get("source"))
        return MCPGatewayRequest(method, request_id, server_id, timestamp, context, params, source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["method"] = from_str(self.method)
        result["request_id"] = from_str(self.request_id)
        result["server_id"] = from_str(self.server_id)
        result["timestamp"] = self.timestamp.isoformat()
        if self.context is not None:
            result["context"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.context)
        if self.params is not None:
            result["params"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.params)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        return result


@dataclass
class MCPGatewayResponse:
    decision: Decision
    request_id: str
    timestamp: datetime
    approval: Optional[GatewayApproval] = None
    rewritten_request: Optional[Dict[str, Any]] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayResponse':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        request_id = from_str(obj.get("request_id"))
        timestamp = from_datetime(obj.get("timestamp"))
        approval = from_union([GatewayApproval.from_dict, from_none], obj.get("approval"))
        rewritten_request = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("rewritten_request"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return MCPGatewayResponse(decision, request_id, timestamp, approval, rewritten_request, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        result["request_id"] = from_str(self.request_id)
        result["timestamp"] = self.timestamp.isoformat()
        if self.approval is not None:
            result["approval"] = from_union([lambda x: to_class(GatewayApproval, x), from_none], self.approval)
        if self.rewritten_request is not None:
            result["rewritten_request"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.rewritten_request)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


@dataclass
class PolicyEvaluatedData:
    decision: Decision
    evaluation_id: str
    policy_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'PolicyEvaluatedData':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        evaluation_id = from_str(obj.get("evaluation_id"))
        policy_name = from_str(obj.get("policy_name"))
        return PolicyEvaluatedData(decision, evaluation_id, policy_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        result["evaluation_id"] = from_str(self.evaluation_id)
        result["policy_name"] = from_str(self.policy_name)
        return result


@dataclass
class PolicyEvaluationRecord:
    """Durable policy evaluation record.
    Tracks policy decisions with evidence for audit trail.
    """
    decision: Decision
    evaluated_at: datetime
    evaluation_id: str
    policy_name: str
    step_id: str
    evidence_hashes: Optional[List[str]] = None
    reason: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PolicyEvaluationRecord':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        evaluated_at = from_datetime(obj.get("evaluated_at"))
        evaluation_id = from_str(obj.get("evaluation_id"))
        policy_name = from_str(obj.get("policy_name"))
        step_id = from_str(obj.get("step_id"))
        evidence_hashes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("evidence_hashes"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return PolicyEvaluationRecord(decision, evaluated_at, evaluation_id, policy_name, step_id, evidence_hashes, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        result["evaluated_at"] = self.evaluated_at.isoformat()
        result["evaluation_id"] = from_str(self.evaluation_id)
        result["policy_name"] = from_str(self.policy_name)
        result["step_id"] = from_str(self.step_id)
        if self.evidence_hashes is not None:
            result["evidence_hashes"] = from_union([lambda x: from_list(from_str, x), from_none], self.evidence_hashes)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        return result


@dataclass
class PreflightInput:
    engine_output: Dict[str, Any]
    mode: Mode
    step_id: str
    workflow_id: str
    context: Optional[Dict[str, Any]] = None
    evidence: Optional[List[PreflightEvidence]] = None
    plan_token: Optional[PlanToken] = None
    """Plan-token binds artifacts to subsequent take-off.
    Extended with version and governance provenance for safe upgrades and auditability.
    """

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightInput':
        assert isinstance(obj, dict)
        engine_output = from_dict(lambda x: x, obj.get("engine_output"))
        mode = Mode(obj.get("mode"))
        step_id = from_str(obj.get("step_id"))
        workflow_id = from_str(obj.get("workflow_id"))
        context = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("context"))
        evidence = from_union([lambda x: from_list(PreflightEvidence.from_dict, x), from_none], obj.get("evidence"))
        plan_token = from_union([PlanToken.from_dict, from_none], obj.get("plan_token"))
        return PreflightInput(engine_output, mode, step_id, workflow_id, context, evidence, plan_token)

    def to_dict(self) -> dict:
        result: dict = {}
        result["engine_output"] = from_dict(lambda x: x, self.engine_output)
        result["mode"] = to_enum(Mode, self.mode)
        result["step_id"] = from_str(self.step_id)
        result["workflow_id"] = from_str(self.workflow_id)
        if self.context is not None:
            result["context"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.context)
        if self.evidence is not None:
            result["evidence"] = from_union([lambda x: from_list(lambda x: to_class(PreflightEvidence, x), x), from_none], self.evidence)
        if self.plan_token is not None:
            result["plan_token"] = from_union([lambda x: to_class(PlanToken, x), from_none], self.plan_token)
        return result


@dataclass
class PreflightRequires:
    reason: Optional[str] = None
    role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightRequires':
        assert isinstance(obj, dict)
        reason = from_union([from_str, from_none], obj.get("reason"))
        role = from_union([from_str, from_none], obj.get("role"))
        return PreflightRequires(reason, role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        return result


@dataclass
class PreflightOutput:
    decision: Decision
    requires: Optional[PreflightRequires] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightOutput':
        assert isinstance(obj, dict)
        decision = Decision(obj.get("decision"))
        requires = from_union([PreflightRequires.from_dict, from_none], obj.get("requires"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return PreflightOutput(decision, requires, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(Decision, self.decision)
        if self.requires is not None:
            result["requires"] = from_union([lambda x: to_class(PreflightRequires, x), from_none], self.requires)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


class State(Enum):
    APPROVED = "APPROVED"
    ARTIFACTS_VALIDATED = "ARTIFACTS_VALIDATED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    EXECUTION_COMPLETE = "EXECUTION_COMPLETE"
    FAILED = "FAILED"
    INIT = "INIT"
    PLAN_GENERATED = "PLAN_GENERATED"
    PLAN_RUNNING = "PLAN_RUNNING"
    PREFLIGHT_COMPLETE = "PREFLIGHT_COMPLETE"
    PRE_FLIGHT_RUNNING = "PRE_FLIGHT_RUNNING"
    READY_FOR_TAKEOFF = "READY_FOR_TAKEOFF"
    TAKEOFF_RUNNING = "TAKEOFF_RUNNING"
    TOKEN_CREATED = "TOKEN_CREATED"


@dataclass
class StepCompletedData:
    step_id: str
    artifacts: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StepCompletedData':
        assert isinstance(obj, dict)
        step_id = from_str(obj.get("step_id"))
        artifacts = from_union([lambda x: from_list(from_str, x), from_none], obj.get("artifacts"))
        return StepCompletedData(step_id, artifacts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["step_id"] = from_str(self.step_id)
        if self.artifacts is not None:
            result["artifacts"] = from_union([lambda x: from_list(from_str, x), from_none], self.artifacts)
        return result


@dataclass
class StepStartedData:
    step_id: str
    step_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'StepStartedData':
        assert isinstance(obj, dict)
        step_id = from_str(obj.get("step_id"))
        step_type = from_str(obj.get("step_type"))
        return StepStartedData(step_id, step_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["step_id"] = from_str(self.step_id)
        result["step_type"] = from_str(self.step_type)
        return result


@dataclass
class WALEntryData:
    initial_state: Optional[State] = None
    plan_token_hash: Optional[str] = None
    step_id: Optional[str] = None
    step_type: Optional[str] = None
    artifacts: Optional[List[str]] = None
    approval_id: Optional[str] = None
    required_role: Optional[str] = None
    approved: Optional[bool] = None
    approver: Optional[str] = None
    artifact_hash: Optional[str] = None
    artifact_id: Optional[str] = None
    artifact_type: Optional[str] = None
    decision: Optional[Decision] = None
    evaluation_id: Optional[str] = None
    policy_name: Optional[str] = None
    final_state: Optional[State] = None
    error: Optional[str] = None
    failed_step: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WALEntryData':
        assert isinstance(obj, dict)
        initial_state = from_union([State, from_none], obj.get("initial_state"))
        plan_token_hash = from_union([from_str, from_none], obj.get("plan_token_hash"))
        step_id = from_union([from_str, from_none], obj.get("step_id"))
        step_type = from_union([from_str, from_none], obj.get("step_type"))
        artifacts = from_union([lambda x: from_list(from_str, x), from_none], obj.get("artifacts"))
        approval_id = from_union([from_str, from_none], obj.get("approval_id"))
        required_role = from_union([from_str, from_none], obj.get("required_role"))
        approved = from_union([from_bool, from_none], obj.get("approved"))
        approver = from_union([from_str, from_none], obj.get("approver"))
        artifact_hash = from_union([from_str, from_none], obj.get("artifact_hash"))
        artifact_id = from_union([from_str, from_none], obj.get("artifact_id"))
        artifact_type = from_union([from_str, from_none], obj.get("artifact_type"))
        decision = from_union([Decision, from_none], obj.get("decision"))
        evaluation_id = from_union([from_str, from_none], obj.get("evaluation_id"))
        policy_name = from_union([from_str, from_none], obj.get("policy_name"))
        final_state = from_union([State, from_none], obj.get("final_state"))
        error = from_union([from_str, from_none], obj.get("error"))
        failed_step = from_union([from_str, from_none], obj.get("failed_step"))
        return WALEntryData(initial_state, plan_token_hash, step_id, step_type, artifacts, approval_id, required_role, approved, approver, artifact_hash, artifact_id, artifact_type, decision, evaluation_id, policy_name, final_state, error, failed_step)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.initial_state is not None:
            result["initial_state"] = from_union([lambda x: to_enum(State, x), from_none], self.initial_state)
        if self.plan_token_hash is not None:
            result["plan_token_hash"] = from_union([from_str, from_none], self.plan_token_hash)
        if self.step_id is not None:
            result["step_id"] = from_union([from_str, from_none], self.step_id)
        if self.step_type is not None:
            result["step_type"] = from_union([from_str, from_none], self.step_type)
        if self.artifacts is not None:
            result["artifacts"] = from_union([lambda x: from_list(from_str, x), from_none], self.artifacts)
        if self.approval_id is not None:
            result["approval_id"] = from_union([from_str, from_none], self.approval_id)
        if self.required_role is not None:
            result["required_role"] = from_union([from_str, from_none], self.required_role)
        if self.approved is not None:
            result["approved"] = from_union([from_bool, from_none], self.approved)
        if self.approver is not None:
            result["approver"] = from_union([from_str, from_none], self.approver)
        if self.artifact_hash is not None:
            result["artifact_hash"] = from_union([from_str, from_none], self.artifact_hash)
        if self.artifact_id is not None:
            result["artifact_id"] = from_union([from_str, from_none], self.artifact_id)
        if self.artifact_type is not None:
            result["artifact_type"] = from_union([from_str, from_none], self.artifact_type)
        if self.decision is not None:
            result["decision"] = from_union([lambda x: to_enum(Decision, x), from_none], self.decision)
        if self.evaluation_id is not None:
            result["evaluation_id"] = from_union([from_str, from_none], self.evaluation_id)
        if self.policy_name is not None:
            result["policy_name"] = from_union([from_str, from_none], self.policy_name)
        if self.final_state is not None:
            result["final_state"] = from_union([lambda x: to_enum(State, x), from_none], self.final_state)
        if self.error is not None:
            result["error"] = from_union([from_str, from_none], self.error)
        if self.failed_step is not None:
            result["failed_step"] = from_union([from_str, from_none], self.failed_step)
        return result


class WALEntryType(Enum):
    APPROVAL_RECEIVED = "approval_received"
    APPROVAL_REQUESTED = "approval_requested"
    ARTIFACT_CREATED = "artifact_created"
    POLICY_EVALUATED = "policy_evaluated"
    STEP_COMPLETED = "step_completed"
    STEP_STARTED = "step_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_STARTED = "workflow_started"


@dataclass
class WALEntry:
    """Write-Ahead Log entry for deterministic replay.
    Enables crash recovery and multi-orchestrator consistency.
    """
    checksum: str
    data: WALEntryData
    entry_type: WALEntryType
    sequence: float
    timestamp: datetime
    workflow_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'WALEntry':
        assert isinstance(obj, dict)
        checksum = from_str(obj.get("checksum"))
        data = WALEntryData.from_dict(obj.get("data"))
        entry_type = WALEntryType(obj.get("entry_type"))
        sequence = from_float(obj.get("sequence"))
        timestamp = from_datetime(obj.get("timestamp"))
        workflow_id = from_str(obj.get("workflow_id"))
        return WALEntry(checksum, data, entry_type, sequence, timestamp, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["checksum"] = from_str(self.checksum)
        result["data"] = to_class(WALEntryData, self.data)
        result["entry_type"] = to_enum(WALEntryType, self.entry_type)
        result["sequence"] = to_float(self.sequence)
        result["timestamp"] = self.timestamp.isoformat()
        result["workflow_id"] = from_str(self.workflow_id)
        return result


@dataclass
class WorkflowCompletedData:
    artifacts: List[str]
    final_state: State

    @staticmethod
    def from_dict(obj: Any) -> 'WorkflowCompletedData':
        assert isinstance(obj, dict)
        artifacts = from_list(from_str, obj.get("artifacts"))
        final_state = State(obj.get("final_state"))
        return WorkflowCompletedData(artifacts, final_state)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artifacts"] = from_list(from_str, self.artifacts)
        result["final_state"] = to_enum(State, self.final_state)
        return result


@dataclass
class WorkflowFailedData:
    error: str
    failed_step: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WorkflowFailedData':
        assert isinstance(obj, dict)
        error = from_str(obj.get("error"))
        failed_step = from_union([from_str, from_none], obj.get("failed_step"))
        return WorkflowFailedData(error, failed_step)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error"] = from_str(self.error)
        if self.failed_step is not None:
            result["failed_step"] = from_union([from_str, from_none], self.failed_step)
        return result


@dataclass
class WorkflowStartedData:
    initial_state: State
    plan_token_hash: str

    @staticmethod
    def from_dict(obj: Any) -> 'WorkflowStartedData':
        assert isinstance(obj, dict)
        initial_state = State(obj.get("initial_state"))
        plan_token_hash = from_str(obj.get("plan_token_hash"))
        return WorkflowStartedData(initial_state, plan_token_hash)

    def to_dict(self) -> dict:
        result: dict = {}
        result["initial_state"] = to_enum(State, self.initial_state)
        result["plan_token_hash"] = from_str(self.plan_token_hash)
        return result


@dataclass
class WorkflowState:
    state: State
    last_decision: Optional[Decision] = None
    plan_token_hash: Optional[str] = None
    step_id: Optional[str] = None
    workflow_id: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WorkflowState':
        assert isinstance(obj, dict)
        state = State(obj.get("state"))
        last_decision = from_union([Decision, from_none], obj.get("last_decision"))
        plan_token_hash = from_union([from_str, from_none], obj.get("plan_token_hash"))
        step_id = from_union([from_str, from_none], obj.get("step_id"))
        workflow_id = from_union([from_str, from_none], obj.get("workflow_id"))
        return WorkflowState(state, last_decision, plan_token_hash, step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["state"] = to_enum(State, self.state)
        if self.last_decision is not None:
            result["last_decision"] = from_union([lambda x: to_enum(Decision, x), from_none], self.last_decision)
        if self.plan_token_hash is not None:
            result["plan_token_hash"] = from_union([from_str, from_none], self.plan_token_hash)
        if self.step_id is not None:
            result["step_id"] = from_union([from_str, from_none], self.step_id)
        if self.workflow_id is not None:
            result["workflow_id"] = from_union([from_str, from_none], self.workflow_id)
        return result


@dataclass
class WorkflowStateRecord:
    """Durable workflow state record for restart-safety.
    Contains all information needed to deterministically resume workflow execution.
    """
    approvals: List[ApprovalRecord]
    artifacts: List[ArtifactRecord]
    created_at: datetime
    current_state: State
    plan_token_hash: str
    policy_evaluations: List[PolicyEvaluationRecord]
    steps_completed: List[str]
    steps_pending: List[str]
    updated_at: datetime
    workflow_id: str
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WorkflowStateRecord':
        assert isinstance(obj, dict)
        approvals = from_list(ApprovalRecord.from_dict, obj.get("approvals"))
        artifacts = from_list(ArtifactRecord.from_dict, obj.get("artifacts"))
        created_at = from_datetime(obj.get("created_at"))
        current_state = State(obj.get("current_state"))
        plan_token_hash = from_str(obj.get("plan_token_hash"))
        policy_evaluations = from_list(PolicyEvaluationRecord.from_dict, obj.get("policy_evaluations"))
        steps_completed = from_list(from_str, obj.get("steps_completed"))
        steps_pending = from_list(from_str, obj.get("steps_pending"))
        updated_at = from_datetime(obj.get("updated_at"))
        workflow_id = from_str(obj.get("workflow_id"))
        metadata = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("metadata"))
        return WorkflowStateRecord(approvals, artifacts, created_at, current_state, plan_token_hash, policy_evaluations, steps_completed, steps_pending, updated_at, workflow_id, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approvals"] = from_list(lambda x: to_class(ApprovalRecord, x), self.approvals)
        result["artifacts"] = from_list(lambda x: to_class(ArtifactRecord, x), self.artifacts)
        result["created_at"] = self.created_at.isoformat()
        result["current_state"] = to_enum(State, self.current_state)
        result["plan_token_hash"] = from_str(self.plan_token_hash)
        result["policy_evaluations"] = from_list(lambda x: to_class(PolicyEvaluationRecord, x), self.policy_evaluations)
        result["steps_completed"] = from_list(from_str, self.steps_completed)
        result["steps_pending"] = from_list(from_str, self.steps_pending)
        result["updated_at"] = self.updated_at.isoformat()
        result["workflow_id"] = from_str(self.workflow_id)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.metadata)
        return result


@dataclass
class CabinCrewProtocol:
    aggregation_method: Optional[AggregationMethod] = None
    any_map: Optional[Dict[str, Any]] = None
    approval_received_data: Optional[ApprovalReceivedData] = None
    approval_record: Optional[ApprovalRecord] = None
    approval_request: Optional[ApprovalRequest] = None
    approval_requested_data: Optional[ApprovalRequestedData] = None
    approval_response: Optional[ApprovalResponse] = None
    artifact: Optional[Artifact] = None
    artifact_created_data: Optional[ArtifactCreatedData] = None
    artifact_record: Optional[ArtifactRecord] = None
    audit_approval: Optional[AuditApproval] = None
    audit_artifact: Optional[AuditArtifact] = None
    audit_engine: Optional[AuditEngine] = None
    audit_event: Optional[AuditEvent] = None
    audit_gateway: Optional[AuditGateway] = None
    audit_integrity: Optional[AuditIntegrity] = None
    audit_policy: Optional[AuditPolicy] = None
    audit_workflow: Optional[AuditWorkflow] = None
    decision: Optional[Decision] = None
    decision_severity: Optional[float] = None
    engine_artifact: Optional[EngineArtifact] = None
    engine_input: Optional[EngineInput] = None
    engine_meta: Optional[EngineMeta] = None
    engine_metric: Optional[EngineMetric] = None
    engine_orchestrator: Optional[EngineOrchestrator] = None
    engine_output: Optional[EngineOutput] = None
    gateway_approval: Optional[GatewayApproval] = None
    llm_gateway_policy_config: Optional[LLMGatewayPolicyConfig] = None
    llm_gateway_request: Optional[LLMGatewayRequest] = None
    llm_gateway_response: Optional[LLMGatewayResponse] = None
    llm_gateway_rule: Optional[LLMGatewayRule] = None
    mcp_gateway_policy_config: Optional[MCPGatewayPolicyConfig] = None
    mcp_gateway_request: Optional[MCPGatewayRequest] = None
    mcp_gateway_response: Optional[MCPGatewayResponse] = None
    mcp_gateway_rule: Optional[MCPGatewayRule] = None
    mode: Optional[Mode] = None
    plan_artifact_hash: Optional[PlanArtifactHash] = None
    plan_token: Optional[PlanToken] = None
    policy_evaluated_data: Optional[PolicyEvaluatedData] = None
    policy_evaluation: Optional[PolicyEvaluation] = None
    policy_evaluation_record: Optional[PolicyEvaluationRecord] = None
    preflight_evidence: Optional[PreflightEvidence] = None
    preflight_input: Optional[PreflightInput] = None
    preflight_output: Optional[PreflightOutput] = None
    preflight_requires: Optional[PreflightRequires] = None
    record_string_any: Optional[Dict[str, Any]] = None
    state: Optional[State] = None
    step_completed_data: Optional[StepCompletedData] = None
    step_started_data: Optional[StepStartedData] = None
    wal_entry: Optional[WALEntry] = None
    wal_entry_data: Optional[WALEntryData] = None
    wal_entry_type: Optional[WALEntryType] = None
    workflow_completed_data: Optional[WorkflowCompletedData] = None
    workflow_failed_data: Optional[WorkflowFailedData] = None
    workflow_started_data: Optional[WorkflowStartedData] = None
    workflow_state: Optional[WorkflowState] = None
    workflow_state_record: Optional[WorkflowStateRecord] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CabinCrewProtocol':
        assert isinstance(obj, dict)
        aggregation_method = from_union([AggregationMethod, from_none], obj.get("AggregationMethod"))
        any_map = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("AnyMap"))
        approval_received_data = from_union([ApprovalReceivedData.from_dict, from_none], obj.get("ApprovalReceivedData"))
        approval_record = from_union([ApprovalRecord.from_dict, from_none], obj.get("ApprovalRecord"))
        approval_request = from_union([ApprovalRequest.from_dict, from_none], obj.get("ApprovalRequest"))
        approval_requested_data = from_union([ApprovalRequestedData.from_dict, from_none], obj.get("ApprovalRequestedData"))
        approval_response = from_union([ApprovalResponse.from_dict, from_none], obj.get("ApprovalResponse"))
        artifact = from_union([Artifact.from_dict, from_none], obj.get("Artifact"))
        artifact_created_data = from_union([ArtifactCreatedData.from_dict, from_none], obj.get("ArtifactCreatedData"))
        artifact_record = from_union([ArtifactRecord.from_dict, from_none], obj.get("ArtifactRecord"))
        audit_approval = from_union([AuditApproval.from_dict, from_none], obj.get("AuditApproval"))
        audit_artifact = from_union([AuditArtifact.from_dict, from_none], obj.get("AuditArtifact"))
        audit_engine = from_union([AuditEngine.from_dict, from_none], obj.get("AuditEngine"))
        audit_event = from_union([AuditEvent.from_dict, from_none], obj.get("AuditEvent"))
        audit_gateway = from_union([AuditGateway.from_dict, from_none], obj.get("AuditGateway"))
        audit_integrity = from_union([AuditIntegrity.from_dict, from_none], obj.get("AuditIntegrity"))
        audit_policy = from_union([AuditPolicy.from_dict, from_none], obj.get("AuditPolicy"))
        audit_workflow = from_union([AuditWorkflow.from_dict, from_none], obj.get("AuditWorkflow"))
        decision = from_union([Decision, from_none], obj.get("Decision"))
        decision_severity = from_union([from_float, from_none], obj.get("DecisionSeverity"))
        engine_artifact = from_union([EngineArtifact.from_dict, from_none], obj.get("EngineArtifact"))
        engine_input = from_union([EngineInput.from_dict, from_none], obj.get("EngineInput"))
        engine_meta = from_union([EngineMeta.from_dict, from_none], obj.get("EngineMeta"))
        engine_metric = from_union([EngineMetric.from_dict, from_none], obj.get("EngineMetric"))
        engine_orchestrator = from_union([EngineOrchestrator.from_dict, from_none], obj.get("EngineOrchestrator"))
        engine_output = from_union([EngineOutput.from_dict, from_none], obj.get("EngineOutput"))
        gateway_approval = from_union([GatewayApproval.from_dict, from_none], obj.get("GatewayApproval"))
        llm_gateway_policy_config = from_union([LLMGatewayPolicyConfig.from_dict, from_none], obj.get("LLMGatewayPolicyConfig"))
        llm_gateway_request = from_union([LLMGatewayRequest.from_dict, from_none], obj.get("LLMGatewayRequest"))
        llm_gateway_response = from_union([LLMGatewayResponse.from_dict, from_none], obj.get("LLMGatewayResponse"))
        llm_gateway_rule = from_union([LLMGatewayRule.from_dict, from_none], obj.get("LLMGatewayRule"))
        mcp_gateway_policy_config = from_union([MCPGatewayPolicyConfig.from_dict, from_none], obj.get("MCPGatewayPolicyConfig"))
        mcp_gateway_request = from_union([MCPGatewayRequest.from_dict, from_none], obj.get("MCPGatewayRequest"))
        mcp_gateway_response = from_union([MCPGatewayResponse.from_dict, from_none], obj.get("MCPGatewayResponse"))
        mcp_gateway_rule = from_union([MCPGatewayRule.from_dict, from_none], obj.get("MCPGatewayRule"))
        mode = from_union([Mode, from_none], obj.get("Mode"))
        plan_artifact_hash = from_union([PlanArtifactHash.from_dict, from_none], obj.get("PlanArtifactHash"))
        plan_token = from_union([PlanToken.from_dict, from_none], obj.get("PlanToken"))
        policy_evaluated_data = from_union([PolicyEvaluatedData.from_dict, from_none], obj.get("PolicyEvaluatedData"))
        policy_evaluation = from_union([PolicyEvaluation.from_dict, from_none], obj.get("PolicyEvaluation"))
        policy_evaluation_record = from_union([PolicyEvaluationRecord.from_dict, from_none], obj.get("PolicyEvaluationRecord"))
        preflight_evidence = from_union([PreflightEvidence.from_dict, from_none], obj.get("PreflightEvidence"))
        preflight_input = from_union([PreflightInput.from_dict, from_none], obj.get("PreflightInput"))
        preflight_output = from_union([PreflightOutput.from_dict, from_none], obj.get("PreflightOutput"))
        preflight_requires = from_union([PreflightRequires.from_dict, from_none], obj.get("PreflightRequires"))
        record_string_any = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("RecordStringAny"))
        state = from_union([State, from_none], obj.get("State"))
        step_completed_data = from_union([StepCompletedData.from_dict, from_none], obj.get("StepCompletedData"))
        step_started_data = from_union([StepStartedData.from_dict, from_none], obj.get("StepStartedData"))
        wal_entry = from_union([WALEntry.from_dict, from_none], obj.get("WALEntry"))
        wal_entry_data = from_union([WALEntryData.from_dict, from_none], obj.get("WALEntryData"))
        wal_entry_type = from_union([WALEntryType, from_none], obj.get("WALEntryType"))
        workflow_completed_data = from_union([WorkflowCompletedData.from_dict, from_none], obj.get("WorkflowCompletedData"))
        workflow_failed_data = from_union([WorkflowFailedData.from_dict, from_none], obj.get("WorkflowFailedData"))
        workflow_started_data = from_union([WorkflowStartedData.from_dict, from_none], obj.get("WorkflowStartedData"))
        workflow_state = from_union([WorkflowState.from_dict, from_none], obj.get("WorkflowState"))
        workflow_state_record = from_union([WorkflowStateRecord.from_dict, from_none], obj.get("WorkflowStateRecord"))
        return CabinCrewProtocol(aggregation_method, any_map, approval_received_data, approval_record, approval_request, approval_requested_data, approval_response, artifact, artifact_created_data, artifact_record, audit_approval, audit_artifact, audit_engine, audit_event, audit_gateway, audit_integrity, audit_policy, audit_workflow, decision, decision_severity, engine_artifact, engine_input, engine_meta, engine_metric, engine_orchestrator, engine_output, gateway_approval, llm_gateway_policy_config, llm_gateway_request, llm_gateway_response, llm_gateway_rule, mcp_gateway_policy_config, mcp_gateway_request, mcp_gateway_response, mcp_gateway_rule, mode, plan_artifact_hash, plan_token, policy_evaluated_data, policy_evaluation, policy_evaluation_record, preflight_evidence, preflight_input, preflight_output, preflight_requires, record_string_any, state, step_completed_data, step_started_data, wal_entry, wal_entry_data, wal_entry_type, workflow_completed_data, workflow_failed_data, workflow_started_data, workflow_state, workflow_state_record)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.aggregation_method is not None:
            result["AggregationMethod"] = from_union([lambda x: to_enum(AggregationMethod, x), from_none], self.aggregation_method)
        if self.any_map is not None:
            result["AnyMap"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.any_map)
        if self.approval_received_data is not None:
            result["ApprovalReceivedData"] = from_union([lambda x: to_class(ApprovalReceivedData, x), from_none], self.approval_received_data)
        if self.approval_record is not None:
            result["ApprovalRecord"] = from_union([lambda x: to_class(ApprovalRecord, x), from_none], self.approval_record)
        if self.approval_request is not None:
            result["ApprovalRequest"] = from_union([lambda x: to_class(ApprovalRequest, x), from_none], self.approval_request)
        if self.approval_requested_data is not None:
            result["ApprovalRequestedData"] = from_union([lambda x: to_class(ApprovalRequestedData, x), from_none], self.approval_requested_data)
        if self.approval_response is not None:
            result["ApprovalResponse"] = from_union([lambda x: to_class(ApprovalResponse, x), from_none], self.approval_response)
        if self.artifact is not None:
            result["Artifact"] = from_union([lambda x: to_class(Artifact, x), from_none], self.artifact)
        if self.artifact_created_data is not None:
            result["ArtifactCreatedData"] = from_union([lambda x: to_class(ArtifactCreatedData, x), from_none], self.artifact_created_data)
        if self.artifact_record is not None:
            result["ArtifactRecord"] = from_union([lambda x: to_class(ArtifactRecord, x), from_none], self.artifact_record)
        if self.audit_approval is not None:
            result["AuditApproval"] = from_union([lambda x: to_class(AuditApproval, x), from_none], self.audit_approval)
        if self.audit_artifact is not None:
            result["AuditArtifact"] = from_union([lambda x: to_class(AuditArtifact, x), from_none], self.audit_artifact)
        if self.audit_engine is not None:
            result["AuditEngine"] = from_union([lambda x: to_class(AuditEngine, x), from_none], self.audit_engine)
        if self.audit_event is not None:
            result["AuditEvent"] = from_union([lambda x: to_class(AuditEvent, x), from_none], self.audit_event)
        if self.audit_gateway is not None:
            result["AuditGateway"] = from_union([lambda x: to_class(AuditGateway, x), from_none], self.audit_gateway)
        if self.audit_integrity is not None:
            result["AuditIntegrity"] = from_union([lambda x: to_class(AuditIntegrity, x), from_none], self.audit_integrity)
        if self.audit_policy is not None:
            result["AuditPolicy"] = from_union([lambda x: to_class(AuditPolicy, x), from_none], self.audit_policy)
        if self.audit_workflow is not None:
            result["AuditWorkflow"] = from_union([lambda x: to_class(AuditWorkflow, x), from_none], self.audit_workflow)
        if self.decision is not None:
            result["Decision"] = from_union([lambda x: to_enum(Decision, x), from_none], self.decision)
        if self.decision_severity is not None:
            result["DecisionSeverity"] = from_union([to_float, from_none], self.decision_severity)
        if self.engine_artifact is not None:
            result["EngineArtifact"] = from_union([lambda x: to_class(EngineArtifact, x), from_none], self.engine_artifact)
        if self.engine_input is not None:
            result["EngineInput"] = from_union([lambda x: to_class(EngineInput, x), from_none], self.engine_input)
        if self.engine_meta is not None:
            result["EngineMeta"] = from_union([lambda x: to_class(EngineMeta, x), from_none], self.engine_meta)
        if self.engine_metric is not None:
            result["EngineMetric"] = from_union([lambda x: to_class(EngineMetric, x), from_none], self.engine_metric)
        if self.engine_orchestrator is not None:
            result["EngineOrchestrator"] = from_union([lambda x: to_class(EngineOrchestrator, x), from_none], self.engine_orchestrator)
        if self.engine_output is not None:
            result["EngineOutput"] = from_union([lambda x: to_class(EngineOutput, x), from_none], self.engine_output)
        if self.gateway_approval is not None:
            result["GatewayApproval"] = from_union([lambda x: to_class(GatewayApproval, x), from_none], self.gateway_approval)
        if self.llm_gateway_policy_config is not None:
            result["LLMGatewayPolicyConfig"] = from_union([lambda x: to_class(LLMGatewayPolicyConfig, x), from_none], self.llm_gateway_policy_config)
        if self.llm_gateway_request is not None:
            result["LLMGatewayRequest"] = from_union([lambda x: to_class(LLMGatewayRequest, x), from_none], self.llm_gateway_request)
        if self.llm_gateway_response is not None:
            result["LLMGatewayResponse"] = from_union([lambda x: to_class(LLMGatewayResponse, x), from_none], self.llm_gateway_response)
        if self.llm_gateway_rule is not None:
            result["LLMGatewayRule"] = from_union([lambda x: to_class(LLMGatewayRule, x), from_none], self.llm_gateway_rule)
        if self.mcp_gateway_policy_config is not None:
            result["MCPGatewayPolicyConfig"] = from_union([lambda x: to_class(MCPGatewayPolicyConfig, x), from_none], self.mcp_gateway_policy_config)
        if self.mcp_gateway_request is not None:
            result["MCPGatewayRequest"] = from_union([lambda x: to_class(MCPGatewayRequest, x), from_none], self.mcp_gateway_request)
        if self.mcp_gateway_response is not None:
            result["MCPGatewayResponse"] = from_union([lambda x: to_class(MCPGatewayResponse, x), from_none], self.mcp_gateway_response)
        if self.mcp_gateway_rule is not None:
            result["MCPGatewayRule"] = from_union([lambda x: to_class(MCPGatewayRule, x), from_none], self.mcp_gateway_rule)
        if self.mode is not None:
            result["Mode"] = from_union([lambda x: to_enum(Mode, x), from_none], self.mode)
        if self.plan_artifact_hash is not None:
            result["PlanArtifactHash"] = from_union([lambda x: to_class(PlanArtifactHash, x), from_none], self.plan_artifact_hash)
        if self.plan_token is not None:
            result["PlanToken"] = from_union([lambda x: to_class(PlanToken, x), from_none], self.plan_token)
        if self.policy_evaluated_data is not None:
            result["PolicyEvaluatedData"] = from_union([lambda x: to_class(PolicyEvaluatedData, x), from_none], self.policy_evaluated_data)
        if self.policy_evaluation is not None:
            result["PolicyEvaluation"] = from_union([lambda x: to_class(PolicyEvaluation, x), from_none], self.policy_evaluation)
        if self.policy_evaluation_record is not None:
            result["PolicyEvaluationRecord"] = from_union([lambda x: to_class(PolicyEvaluationRecord, x), from_none], self.policy_evaluation_record)
        if self.preflight_evidence is not None:
            result["PreflightEvidence"] = from_union([lambda x: to_class(PreflightEvidence, x), from_none], self.preflight_evidence)
        if self.preflight_input is not None:
            result["PreflightInput"] = from_union([lambda x: to_class(PreflightInput, x), from_none], self.preflight_input)
        if self.preflight_output is not None:
            result["PreflightOutput"] = from_union([lambda x: to_class(PreflightOutput, x), from_none], self.preflight_output)
        if self.preflight_requires is not None:
            result["PreflightRequires"] = from_union([lambda x: to_class(PreflightRequires, x), from_none], self.preflight_requires)
        if self.record_string_any is not None:
            result["RecordStringAny"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.record_string_any)
        if self.state is not None:
            result["State"] = from_union([lambda x: to_enum(State, x), from_none], self.state)
        if self.step_completed_data is not None:
            result["StepCompletedData"] = from_union([lambda x: to_class(StepCompletedData, x), from_none], self.step_completed_data)
        if self.step_started_data is not None:
            result["StepStartedData"] = from_union([lambda x: to_class(StepStartedData, x), from_none], self.step_started_data)
        if self.wal_entry is not None:
            result["WALEntry"] = from_union([lambda x: to_class(WALEntry, x), from_none], self.wal_entry)
        if self.wal_entry_data is not None:
            result["WALEntryData"] = from_union([lambda x: to_class(WALEntryData, x), from_none], self.wal_entry_data)
        if self.wal_entry_type is not None:
            result["WALEntryType"] = from_union([lambda x: to_enum(WALEntryType, x), from_none], self.wal_entry_type)
        if self.workflow_completed_data is not None:
            result["WorkflowCompletedData"] = from_union([lambda x: to_class(WorkflowCompletedData, x), from_none], self.workflow_completed_data)
        if self.workflow_failed_data is not None:
            result["WorkflowFailedData"] = from_union([lambda x: to_class(WorkflowFailedData, x), from_none], self.workflow_failed_data)
        if self.workflow_started_data is not None:
            result["WorkflowStartedData"] = from_union([lambda x: to_class(WorkflowStartedData, x), from_none], self.workflow_started_data)
        if self.workflow_state is not None:
            result["WorkflowState"] = from_union([lambda x: to_class(WorkflowState, x), from_none], self.workflow_state)
        if self.workflow_state_record is not None:
            result["WorkflowStateRecord"] = from_union([lambda x: to_class(WorkflowStateRecord, x), from_none], self.workflow_state_record)
        return result


def cabin_crew_protocol_from_dict(s: Any) -> CabinCrewProtocol:
    return CabinCrewProtocol.from_dict(s)


def cabin_crew_protocol_to_dict(x: CabinCrewProtocol) -> Any:
    return to_class(CabinCrewProtocol, x)
