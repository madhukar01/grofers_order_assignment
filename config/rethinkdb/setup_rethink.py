from rethinkdb import RethinkDB

r = RethinkDB()
r.connect(host='localhost', port=28015).repl()

###############################################################################
# Create databases
###############################################################################
r.db_create('grofers').run()

###############################################################################
# Create tables
###############################################################################
r.db('grofers').table_create('delivery_vehicles',
                             primary_key="slot_id").run()

delivery_vehicles = [
    {
        "slot_id": "6-9",
        "available_vehicles": [
            {
                "vehicle_type": "bike",
                "max_capacity": 30,
                "vehicles_available": 3
            },
            {
                "vehicle_type": "scooter",
                "max_capacity": 50,
                "vehicles_available": 2
            }
        ]
    },
    {
        "slot_id": "9-13",
        "available_vehicles": [
            {
                "vehicle_type": "bike",
                "max_capacity": 30,
                "vehicles_available": 3
            },
            {
                "vehicle_type": "scooter",
                "max_capacity": 50,
                "vehicles_available": 2
            },
            {
                "vehicle_type": "truck",
                "max_capacity": 100,
                "vehicles_available": 1
            }
        ]
    },
    {
        "slot_id": "16-19",
        "available_vehicles": [
            {
                "vehicle_type": "bike",
                "max_capacity": 30,
                "vehicles_available": 3
            },
            {
                "vehicle_type": "scooter",
                "max_capacity": 50,
                "vehicles_available": 2
            },
            {
                "vehicle_type": "truck",
                "max_capacity": 100,
                "vehicles_available": 1
            }
        ]
    },
    {
        "slot_id": "19-23",
        "available_vehicles": [
            {
                "vehicle_type": "scooter",
                "max_capacity": 50,
                "vehicles_available": 2
            },
            {
                "vehicle_type": "truck",
                "max_capacity": 100,
                "vehicles_available": 1
            }
        ]
    }
]

r.db('grofers').table('delivery_vehicles').insert(delivery_vehicles).run()
