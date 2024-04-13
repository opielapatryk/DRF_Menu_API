# DRF_menu_api_clean

## Project is created based on Clean Architecture <br>
### Inward -> Simple data x Outward -> Interfaces

## External systems
Web Framework: DRF <br>
Repository: Memory <br>

## Gateways
Dictionary + DB Interface <br>
i.e. class MemRepo <br>

## Use Cases: "business logic"
### Receive repo + parameters, returns results
GET: List all dishes <br>
GET{id}: List dish <br>
POST: Add dish <br>
PUT: Edit dish <br>
DELETE{id}: Remove dish <br>

## Entities
Module: Dish <br>

# TODO
- [x] Apply Clean Architecture <br> 
- [x] Layer Abstraction<br> 
- [x] Dependency Injection<br> 
- [x] UseCase Implementation<br> 
- [x] Serialization / Deserialization<br> 
- [x] Mock Repo Implementation<br>  
- [x] Apply Tests<br> 

# Useful commands:
### Testing 
- pytest <br>

### Build, run, stop
- python manage.py runserver<br>
- docker-compose up<br>
- docker-compose up --build<br>