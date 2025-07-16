from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional


class Tier(BaseModel):
    name: str
    features: List[str]
    description: Optional[str]
    limits: dict
    createdDate: datetime = Field(default_factory=datetime.utcnow)

class FirewallVersion(BaseModel):
    versionName: str
    ruleset: List[dict]
    changelog: List[str]
    createdDate: datetime = Field(default_factory=datetime.utcnow)

class Tenant(BaseModel):
    tenantId: str
    tenantName: str
    tenantAdmin: dict  # maps to Login.userId
    tierId: str  # maps to Tier
    firewallVersionId: str  # maps to FirewallVersion
    llmUse: str 
    tokencount: int
    mongoUrl:str
    createdDate: datetime = Field(default_factory=datetime.utcnow)
    updatedDate: datetime = Field(default_factory=datetime.utcnow)

class GlobalRule(BaseModel):
    ruleName: str
    ruleType: str
    description: str
    config: dict
    defaultEnabled: bool

class License(BaseModel):
    tierId: str  # maps to Tier
    firewallVersionId: str  # maps to FirewallVersion
    licenseKey: str
    validTill: datetime
    issuedTo: str  # maps to Tenant.tenantId

class LLMProvider(BaseModel):
    apiId:str
    name: str
    apiBaseUrl: str
    supportedModels: List[str]
    usageNotes: Optional[str] = None

class RuleCategory(BaseModel):
    name: str
    description: Optional[str] = None