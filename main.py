from yaml import safe_load
from fastapi import FastAPI, APIRouter, HTTPException
import peewee, os
import traceback

with open("api.yaml") as f:
    y = safe_load(os.path.expandvars(f.read()))

app = FastAPI()

db_columns = {
    "str" : peewee.CharField,
    "int" : peewee.IntegerField,
}

db = peewee.SqliteDatabase('database.db')

class TableModel(peewee.Model):
    class Meta:
        database = db

routes = []
def make_routes(model):
    router = APIRouter(tags=[model.__name__])
    path = f"/{model.__name__.lower().strip()}"
    def route_get():
        try:
            return [item.__data__ for item in model.select().execute()]
        except:
            traceback.print_exc()
            return []
    def route_get_id(id : int):
        try:
            return model.get(model.id==id).__data__
        except:
            traceback.print_exc()
            raise HTTPException(404)
    def route_put(id : int, dict_ : dict):
        with db.atomic() as tsx:
            try:
                o = model.get(model.id==id)
                for key,value in dict_.items():
                    setattr(o,key,value)  
                return o.save()
            except:
                traceback.print_exc()
                tsx.rollback()
                raise HTTPException(404)

    def route_post(dict_ : dict):
        with db.atomic() as tsx:
            try:
                return model.create(**dict_).__data__
            except:
                traceback.print_exc()
                tsx.rollback()
                raise HTTPException(404)
        
    def route_delete(id : int):
        try:
            o = model.get(model.id==id)
            o.delete_instance()
            return {"detail" : f"delete {id}"}
        except:
            traceback.print_exc()
            return None
    
    route_get.__name__ = f"get_{model.__name__}"
    route_post.__name__ = f"post_{model.__name__}"
    route_put.__name__ = f"put_{model.__name__}"
    route_delete.__name__ = f"delete_{model.__name__}"

    router.get(path)(route_get)
    router.get(path + "/{id}")(route_get_id)
    router.post(path, status_code=201)(route_post)
    router.put(path + "/{id}")(route_put)
    router.delete(path + "/{id}")(route_delete)

    routes.append(router)
    
models = []
for table,attr in y['tables'].items():
    attributes = {}
    for key,value in attr.items():
        attributes[key] = db_columns[value]()
    modelo = type(table,(TableModel,),attributes)
    models.append(modelo)



for model in models:
    print("MODEL=",model.__name__)
    model.create_table()  
    make_routes(model)

for route in routes:
    app.include_router(route)

@app.get("/")
async def health_check():
    return {"health" : "ok"}

