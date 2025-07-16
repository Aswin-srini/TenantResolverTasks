from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class TokenLimit(BaseModel):
    tentantId:str
    roles: object
    tokenLimit: int
    createdDate: datetime = Field(default_factory=datetime.utcnow)

class APIKey(BaseModel):
    keyLabel: str
    key: str
    createdBy: str  # maps to TenantUser.userId
    createdDate: datetime = Field(default_factory=datetime.utcnow)
    usageStats: dict = {}

class Role(BaseModel):
    roleName: str
    permissions: List[str]

class TenantUser(BaseModel):
    userId: str
    userName: str
    roleId: str  # maps to Role
    email: EmailStr
    lastLogin: Optional[datetime]
    status: str

class TenantRule(BaseModel):
    tentantId:str
    globalRuleId: str # maps to GlobalRule
    enabled: bool
    overrideConfig: dict = {}

class TokenQuota(BaseModel):
    userId: str  # maps to TenantUser.userId
    llm: str
    tokensUsed: int
    resetDate: datetime

class LLMConfig(BaseModel):
    tentantId:str
    provider: str  
    model: str
    apiUrl: str
    apiKeyId: str  # maps to APIKey
    isActive: bool = True
    deletedAt: Optional[datetime] = None
    createdBy: Optional[str] = None  # maps to TenantUser.userId
    createdDate: datetime = Field(default_factory=datetime.utcnow)
    updatedDate: Optional[datetime] = None
    notes: Optional[str] = None

class TenantAuditLog(BaseModel):
    userId: str
    action: str
    llm: str
    contentModerated: bool
    prompt: str
    result: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
