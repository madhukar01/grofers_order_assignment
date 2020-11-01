# Grofers Ordera Assignment
Assign orders into delivery vehicles based on constraints

## API Specifications
- Available slots and Vehicles
    - URL: https://madhukar.dev/api/order/vehicles
    - Request Type: GET
    - Parameters: NA

- Assign delivery vehicles for given orders
    - URL: https://madhukar.dev/api/order/deliver
    - Request Type: POST
    - Parameters - Sample JSON
    - ```{
            "slot_id": "16-19",
            "orders": [
                {
                    "order_id": 1,
                    "order_weight": 50
                },
                {
                    "order_id": 2,
                    "order_weight": 10
                },
                {
                    "order_id": 3,
                    "order_weight": 30
                },
                {
                    "order_id": 4,
                    "order_weight": 65
                }]
            }```