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
    - Request Data Type: JSON
    - Parameters (data to be in JSON)
        - slot_id -> one of (6-9, 9-13, 16-19, 19-23)
        - orders -> array of order items to deliver in the slot
    - Sample JSON below
    - ```
        {
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
                }
            ]
        }
      ```

## Database structure
- NOSQL Databse with 1 table - to store Delivery vehicle constraints
- slot_id is document identifier
- Example document:
- ```
    {
        "available_vehicles": [
            {
                "max_capacity": 50,
                "vehicle_type": "scooter",
                "vehicles_available": 2
            },
            {
                "max_capacity": 100,
                "vehicle_type": "truck",
                "vehicles_available": 1
            }
        ],
        "slot_id": "19-23"
    }
  ```

## Delivery vehicle assignment logic
- If total sum of order weight is more than total vehicle capacity, We cannot deliver the orders
- If any of the individual order weights are more than max capacity of available vehicle, We cannot deliver the order
- Vehicles are sorted in increasing order of their max capacity
- Order are sorted in increasing order of their max capacity
- Repeat below until all orders are assigned
    - A vehicle is chosen based on the total weight of orders in the given slot
        - Choose a vehicle large enough to accommodate all orders
        - If no vehicle can accommodate all orders, choose the largest vehicle available
    - Orders are filled in the chosen vehicle till we cannot accommodate any more orders
    - If a vehicle is chosen and If we are not able to accommodate the largest order in that vehicle, we cannot deliver orders
- *P.S - Does not provide best solution always*


### Dry run of the above algorithm
- Available vehicles: [ 100, 50, 50, 30, 30, 30 ]
- Order weights: [ 65, 50, 20, 10, 10 ]
- <br/>
- Iteration 1
- Total order weight: 160
- Chosen vehicle: Truck - Capacity: 100 (largest available)
- Filled orders: [ 65, 20, 10 ]
- Remaining space: 5
- <br/>
- Iteration 2
- Total order weight: 60
- Chosen vehicle: Scooter - Capacity: 50 (largest available)
- Filled orders: [ 50 ]
- Remaining space: 0
- <br/>
- Iteration 3
- Total order weight: 10
- Chosen vehicle: Bike - Capacity: 30 (can accommodate all remaining orders)
- Filled orders: [ 10 ]
- Remaining space: 20


### Time complexity
- Assumption - minimum order weight is 1 Kg
- Number of vehicles - V
- Max capacity of each vehicle - K
- Worst case - O (V * K * log(V) * log(K))
    - Each iteration (total V iterations)
        - Find a vehicle - log V
        - Fill orders - K log K
- Example
    - 5 vehicles of 10kg capacity each
    - 50 orders of 1kg weight each

### Other assumptions for order assignment
- Maximum of 1 truck, 2 scooters and 3 bikes can be used in a slot (when they are all available)
- Vehicles will not take trips to deliver orders
