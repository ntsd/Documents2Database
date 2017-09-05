import json
import io
try:
    from .Models import Customer, Boundary
except Exception: #ImportError
    from Models import Customer, Boundary

def loadJson(path):
    # json.loads(data, object_hook=lambda d: Namespace(**d))
    with open(path) as data:
        return json.loads(data, object_hook=lambda d: Customer(**d))

def saveJson(path, customer):
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(customer.toJSON())

if __name__ == "__main__":
    customer = Customer(name="tesco", boundaries=[Boundary("detail", (10,10,60,50))])
    saveJson("customers/"+customer.name+".json", customer)
