from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from app.models import SweetModel
from app.auth import services as auth_services
from app.api import services as sweet_services
from app.schemas import SweetPostRequest,SweetPostResponse

from fastapi import APIRouter, Depends, HTTPException,Query,Path,Body
from bson import ObjectId
from typing import List,Optional

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/sweet", response_model=SweetModel)
async def sweet(sweet_post: SweetPostRequest,current_user = Depends(auth_services.get_current_user)):

    existing_sweet = await sweet_services.get_sweet_by_name(sweet_post.name)

    if existing_sweet:
        raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Sweet exists"
            )
    else:
        sweet = await sweet_services.create_sweet(name=sweet_post.name,category=sweet_post.category,price=sweet_post.price,quantity=sweet_post.quantity)
        return {
            "name":sweet.name,
            "category":sweet.category,
            "price":sweet.price,
            "quantity":sweet.quantity
        }

@router.get("/sweets",response_model=list[SweetModel])
async def sweets(current_user = Depends(auth_services.get_current_user)):
    sweets_result = await sweet_services.get_sweets()
    return sweets_result

@router.get("/sweets/search",response_model=list[SweetModel])
async def search_sweets(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    current_user = Depends(auth_services.get_current_user)):

    sweets = await sweet_services.search_sweets(name=name,category=category,min_price=min_price,max_price=max_price)

    return sweets

@router.put("/sweets/{id}", response_model=SweetPostResponse)
async def update_sweet(
    id: str = Path(...,description="id of sweet to be updated"),
    sweet_data: SweetPostRequest = None,
    current_user=Depends(auth_services.get_current_user)
    ):

    #if the ojectid is valid only then proceed
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid sweet ID"
        )

    #check if sweet exists
    existing_sweet = await sweet_services.get_sweet_by_id(id)
    if not existing_sweet:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )

    #updating sweet
    updated = await sweet_services.update_sweet(
        id=id,
        update_data={
            "name": sweet_data.name,
            "category": sweet_data.category,
            "price": sweet_data.price,
            "quantity": sweet_data.quantity
        }
    )

    if not updated:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Failed to update sweet"
        )

    return SweetPostResponse(**updated)


@router.delete("/sweets/{id}")
async def delete_sweet(id: str = Path(...,description="id of sweet to be deleted"), current_user = Depends(auth_services.require_admin)):
    deleted = await sweet_services.delete_sweet(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return {"message": "Sweet deleted"}


@router.post("/sweets/{id}/purchase", response_model=SweetModel)
async def purchase_sweet(
    id: str = Path(..., description="ID of the sweet to purchase"),
    current_user=Depends(auth_services.get_current_user)
):
    # Fetch the sweet
    sweet = await sweet_services.get_sweet_by_id(id)
    if not sweet:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sweet not found")

    # Check quantity
    if sweet["quantity"] <= 0:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Sweet is out of stock"
        )

    # Decrease quantity
    updated_sweet = await sweet_services.decrease_sweet_quantity(id)
    return updated_sweet

@router.post("/sweets/{id}/restock", response_model=SweetModel)
async def restock_sweet(
    id: str = Path(..., description="ID of the sweet to restock"),
    amount: int = Body(..., embed=True, description="Amount to restock"),
    current_user = Depends(auth_services.require_admin)
):
    sweet = await sweet_services.get_sweet_by_id(id)
    if not sweet:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Sweet not found")

    updated_sweet = await sweet_services.increase_sweet_quantity(id, amount)
    return updated_sweet