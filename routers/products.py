from fastapi import APIRouter
router = APIRouter(prefix="/products",
                   responses={404: {"message": "No encontrado"} },
                   tags = ["products"])

products_list = ["Producto 0","Producto 1", "Producto 2 "]
@router.get("/")
async def products():
    return ["Producto 1","Producto 2", "Producto 3 "]

@router.get("/{id}")
async def products(id: int):
    return products_list[id]
