from typing import Annotated, Optional, List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from pydantic import Field as PydanticField

class OrderBase(SQLModel):
    symbol: str = PydanticField(..., min_length=1)
    quantity: int = PydanticField(..., gt=0)
    price: float = PydanticField(..., gt=0)
    order_type: str = PydanticField(..., pattern="^(buy|sell)$")

class OrderCreate(OrderBase):
    pass

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate, session: SessionDep):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@app.get("/orders", response_model=List[Order])
def read_orders(session: Session = Depends(get_session)):
    statement = select(Order)
    orders = session.exec(statement).all()
    return orders
