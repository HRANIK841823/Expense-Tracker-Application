from fastapi import FastAPI,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
import models
from models import Transactions,Users
from typing import Annotated
from database import engine,SessionLocal
from fastapi.responses import JSONResponse
from typing import Optional,Literal
from router.auth import get_current_user
from router import auth
from datetime import date

# ============================
# FastAPI App
# ============================
app=FastAPI()



# ============================
# Model Setup
# ============================

class Transaction(BaseModel):
    title:str
    amount:float=Field(gt=0)
    type:Literal["income","expense"]
    category:str
   
    
class TransactionUpdate(BaseModel):
    title:Optional[str]=Field(default=None)
    amount:Optional[float]=Field(default=None,gt=0)
    type:Optional[Literal["income","expense"]]=Field(default=None)
    category:Optional[str]=Field(default=None)


# ============================
#  All Connection
# ============================
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)



# ============================
#  Get Database
# ============================

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
#  All Dependency
# ============================
db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


# ============================
#  Post Transaction
# ============================
@app.post('/transactions')
def create_transactions(db:db_dependency,user:user_dependency,new_transaction:Transaction):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")
    transaction_model=Transactions(**new_transaction.model_dump(),owner_id=user.get('id'))
    db.add(transaction_model)
    db.commit()
    return JSONResponse(status_code=201,content={'message':"Transaction Created Successfully"})


# ============================
#  Read All Transactions
# ============================
@app.get('/transactions')
def read_transactions(db:db_dependency,user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")
    return db.query(Transactions).filter(Transactions.owner_id==user.get('id')).all()


# ============================
#  Filter Transaction
# ============================

@app.get("/transactions/filter")
def filter_transactions(db: db_dependency,user: user_dependency,type: Optional[Literal["income", "expense"]] = None,category: Optional[str] = None,minimum_amount: Optional[float] = Query(default=None, ge=0),maximum_amount: Optional[float] = Query(default=None, ge=0)):
    if user is None:
        raise HTTPException(status_code=404,detail="User Not Authenticated")

    if (minimum_amount is not None and maximum_amount is not None and minimum_amount>maximum_amount):
        raise HTTPException(status_code=400,detail="Minimum amount is not high then maximum amount")
   

    transactions=db.query(Transactions).filter(Transactions.owner_id==user.get('id'))

    if type is not None:
        transactions=transactions.filter(Transactions.type==type)

    if category is not  None:
        transactions=transactions.filter(Transactions.category==category)

    if minimum_amount is not None:
        transactions=transactions.filter(Transactions.amount>=minimum_amount)
    if maximum_amount is not None:
        transactions=transactions.filter(Transactions.amount<=maximum_amount)

    return transactions.all()

# ============================
#  Read Specific Transaction
# ============================

@app.get('/transactions/{transaction_id}')
def read_specific_transactions(db:db_dependency,user:user_dependency,transaction_id:int):
    if user is None:
            raise HTTPException(status_code=401,detail="Failed Authentication")
    specific_transaction=db.query(Transactions).filter(Transactions.owner_id==user.get('id')).filter(Transactions.id==transaction_id).first()
    if specific_transaction is not None:
        return specific_transaction
    else: 
        raise HTTPException(status_code=404,detail="Transaction Not Found For This Id")

    
# ============================
#  Update  Transaction
# ============================

@app.put('/transactions/{transaction_id}')
def update_transactions(db:db_dependency,user:user_dependency,update_transaction:TransactionUpdate,transaction_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Authentication")
    transaction=db.query(Transactions).filter(Transactions.owner_id==user.get('id')).filter(Transactions.id==transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404,detail="Transaction not Found")
    update_data=update_transaction.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(transaction,key,value)
    db.commit()
    return JSONResponse(status_code=200,content={'message':"Transaction Updated Successfully"})


# ============================
#  Delete Transaction
# ============================
@app.delete('/transactions/{transaction_id}')
def delete_transaction(db:db_dependency,user:user_dependency,transaction_id:int):
    if user is None:
        raise HTTPException(status_code=401,detail="Failed Transaction")
    transaction=db.query(Transactions).filter(Transactions.owner_id==user.get('id')).filter(Transactions.id==transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404,detail="Transaction Not Found")
    db.query(Transactions).filter(Transactions.owner_id==user.get('id')).filter(Transactions.id==transaction_id).delete()
    db.commit()
    return JSONResponse(status_code=200,content={'message':'Transaction Deleted Successfully'})








