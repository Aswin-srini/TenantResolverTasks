from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient;
from odmantic import AIOEngine

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from pydantic import BaseModel

server = AsyncIOMotorClient('mongodb+srv://admin:paAKVPjrPEYDJ9QK@cluster0.llnavj9.mongodb.net/')

globalDB = AIOEngine(client = server,database='Global_moduls')
tenantDB = AIOEngine(client = server,database='tenant_module')

app=FastAPI()  

class TenantContext(BaseModel):         #Task no.3 create model for tenantContext
    tenantId:str
    mongoDburl:str
    llmConfig:list
    tokenLimit:list
    enabledRules:list
    tier:list

@app.get("/tenant/{tenant_id}")
async def resolve_tenant_context(tenant_id:str):
    llmpipeline = [
        {'$match':{'tenantId':tenant_id}},
        {'$lookup':{
            'from': 'TokenLimit',
            'localField':'tenantId',
            'foreignField':'tenantId',
            'as':'tenantToken'
        }},
        {'$unwind':'$tenantToken'},
        {'$lookup':{
            'from': 'TenantRule',
            'localField':'tenantId',
            'foreignField':'tenantId',
            'as':'ruleID'                                        
        }},
        {'$unwind':'$ruleID'}
    ]
    tenantpipeline=[
        {'$match':{'tenantId':tenant_id}},
        {'$lookup':{
            'from':'Tier',
            'localField':'tierId',
            'foreignField':'_id',
            'as':'Tier'
        }},
        {'$unwind':'$Tier'}
    ]
    
    llmcon = await tenantDB.database["LLMConfig"].aggregate(llmpipeline).to_list(length=None)
    tenant = await globalDB.database["Tenant"].aggregate(tenantpipeline).to_list(length=None)
    
    if not tenant or not llmcon:
        return JSONResponse(
            status_code=404,
            content= f"This '{tenant_id}' id is not found"
        )
        
    ruleID = llmcon[0]['ruleID']['globalRuleId']
    
    globalrule = await globalDB.database["GlobalRule"].find_one({'_id':ruleID})
    
    mongourl = tenant[0]['mongoUrl']
    tokenlimit= llmcon[0]['tenantToken']
    rules = {
        'tenantrule':llmcon[0]['ruleID'],
        'globalrule':globalrule
        }
    
    
    llmcon[0].pop('tenantToken')
    llmcon[0].pop('ruleID')
    
    Tenant_Context = TenantContext(
            tenantId=tenant_id,
            mongoDburl=mongourl,
            llmConfig=[llmcon[0]],
            tokenLimit=[tokenlimit],
            enabledRules=[rules],
            tier=[tenant[0]['Tier']]
    )
    
    '''Tenantcontext ={
        'mongoDburl':mongourl,          Task no.2 Signature: resolve_tenant_context(tenant_id: str) -> TenantContext 
        'llmConfig':llmcon[0],
        'tokenLimit':tokenlimit,
        'enabledRules':rules
    }'''

    return  jsonable_encoder(Tenant_Context.model_dump(),custom_encoder={ObjectId: str})

    