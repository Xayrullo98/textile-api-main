from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import supplier_balances,suppliers,supplies,currencies,category_details,measures,stage_users,stages,users,categories,login

app = FastAPI( )

from db import Base, engine
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get('/')
def home():
    return {"message": "Welcome"}

app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(categories.categories_router)
app.include_router(stages.stages_router)
app.include_router(stage_users.stage_users_router)
app.include_router(currencies.currencies_router)

app.include_router(category_details.category_details_router)
app.include_router(measures.measures_router)
app.include_router(supplier_balances.supplier_balances_router)
app.include_router(suppliers.suppliers_router)
app.include_router(supplies.supplies_router)