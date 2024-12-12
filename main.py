from fastapi import FastAPI, HTTPException
from Pydentic import BaseModel
import uvicorn
from uuid import  UUID



app = FastAPI()

class DeliveryRequest(BaseModel):
    id: UUID
    description:str
    status:str = 'создана'
#хранилице заявок
deliveries= []


@app.post('/Deliveries/',
          tags=['Доставки'],
          summary='Создание заявки ')
def create_delivery(new_order:DeliveryRequest):
    delivery_data = {
            'id' : new_order.id,
            'description': new_order.description,
            'status': new_order.status }
    deliveries.append(delivery_data)
    return {"message": "Заявка успешно создана", "Заказ": delivery_data}

@app.get('/Deliveries/', tags=["Все Заявки"], summary= "Получение всех заявок")
def get_all_deliveries():
    return deliveries

#Получение заявки по id
@app.get('/Deliveries/{delivery_id}', summary="Получение заявки по id")
def get_delivery_by_id(delivery_id: UUID):
    for delivery in deliveries:
         if delivery['id'] == delivery_id:
            return delivery
    raise HTTPException(status_code=404, detail='Заявка не найдена')

#Удаление заявки
@app.delete("/Deliveries/{delivery_id}", summary='Удаление заявки')
def delete_delivery(delivery_id: UUID):
    for delivery in deliveries:
        if delivery['id'] == delivery_id:
            if delivery['status'] == "создана":
                deliveries.remove(delivery)
                return{"messege": "Заявка успешно удалена"}
            else:
                raise HTTPException(status_code=404, detail="Нельзя удалить заявку, товар уже в доставке")
    raise HTTPException(status_code=404, detail="Заявка не найдена")

#Обновление статуса заявки по id
@app.put("/Deliveries/{delivery_id}/status", summary="Обновление статуса заявки по id")
def Update_delivery(delivery_id: UUID, new_status:str):
    for delivery in deliveries:
        if delivery["id"] == delivery_id:
            delivery["status"] = new_status
            return {"message":"Статус заявки обновлен", "Заявка":delivery}
    raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    
if __name__=='__main__':
    uvicorn.run('main:app', reload=True)
