from app.database import sweets_collection
from app.models import SweetModel
from app.schemas import SweetPostRequest,SweetPostResponse
from app.auth import services as auth_services

from typing import Optional,List
from bson import ObjectId


async def get_sweet_by_id(id: str):
    return await sweets_collection.find_one({"_id": ObjectId(id)})

async def get_sweet_by_name(name:str) -> Optional[SweetModel]:
	sweet = await sweets_collection.find_one({"name":name})
	if sweet:
		sweet["id"] = sweet.get("_id")
		return SweetModel(**sweet)
	else:
		return None

async def create_sweet(name:str,category:str,price:int,quantity:int):
	sweet_doc = {
		"name":name,
		"category":category,
		"price":price,
		"quantity":quantity,
	}

	result = await sweets_collection.insert_one(sweet_doc)
	new_doc = await sweets_collection.find_one({"_id":result.inserted_id})
	new_doc["id"] = new_doc.get("_id")
	return SweetModel(**new_doc)

async def get_sweets():
	sweets = sweets_collection.find({})
	sweets = await sweets.to_list()

	for sweet in sweets:
		sweet["id"] = str(sweet["_id"])#convert ObjectId to str

	return sweets


async def search_sweets(name:Optional[str],category:Optional[str],min_price:Optional[int],max_price:Optional[int]):

    if name is not None:
        results = await sweets_collection.find({"name":name}).to_list()

    if category is not None:
        results = await sweets_collection.find({"category":category}).to_list()

    if min_price!=None or max_price!=None:
    	if min_price==None:
    		results = await sweets_collection.find({"price":{"$lte":max_price}})
    	if max_price==None:
    		results = await sweets_collection.find({"price":{"$gte":min_price}})
    	if min_price!=None and max_price!=None:
    		results = await sweets_collection.find({"price":{"$gte":min_price,"$lte":max_price}})

    return results

async def update_sweet(id:str,update_data:dict):
    result = await sweets_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":update_data},return_document=True)
    return result

async def delete_sweet(id:str):
    result = await sweets_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

async def decrease_sweet_quantity(sweet_id: str):
    result = await sweets_collection.find_one_and_update(
        {"_id": ObjectId(sweet_id), "quantity": {"$gt": 0}},
        {"$inc": {"quantity": -1}},
        return_document=True
    )
    return result

async def increase_sweet_quantity(sweet_id: str, amount: int):
    from bson import ObjectId
    result = await sweets_collection.find_one_and_update(
        {"_id": ObjectId(sweet_id)},
        {"$inc": {"quantity": amount}},
        return_document=True
    )
    return result
