import copy


def assign_orders(vehicles, orders):
    if len(orders) < 1:
        raise Exception('No orders to deliver')

    if len(vehicles) < 1:
        raise Exception('No vehicles to deliver orders')

    # Data pre processing
    # Sort orders in decreasing order of weights
    orders.sort(key=lambda x: x['order_weight'], reverse=True)
    order_weights = [x['order_weight'] for x in orders]

    vehicles.sort(key=lambda x: x['max_capacity'], reverse=True)
    available_vehicles = []
    for vehicle in vehicles:
        number_of_vehicles = vehicle.pop('vehicles_available')
        for i in range(number_of_vehicles):
            available_vehicles.append(copy.deepcopy(vehicle))

    vehicle_weights = [x['max_capacity'] for x in available_vehicles]

    # Now we have pre-processed the data. Sample below
    # order_weights = [30, 30, 20, 10]
    # vehicle_weights = [100, 50, 50, 30, 30, 30]

    # Assign order to vehicles
    total_order_weight = sum(order_weights)
    total_vehicle_capacity = sum(vehicle_weights)
    delivery_data = []

    # Check if all order can be delivered with available vehicles
    if total_order_weight > total_vehicle_capacity:
        raise Exception('Total order weight exceed total vehicle capacity')

    while total_order_weight > 0:
        # Choose vehicle based on total weight
        vehicle_index = -1
        for i in range(len(vehicle_weights)):
            if total_order_weight <= vehicle_weights[i]:
                vehicle_index = i
            else:
                break

        if vehicle_index < 0:
            vehicle_index = 0

        current_vehicle_weight = vehicle_weights.pop(vehicle_index)
        vehicle_chosen = available_vehicles.pop(vehicle_index)
        vehicle_chosen['space_remaining'] = current_vehicle_weight
        vehicle_chosen['oders_assigned'] = []
        delivery_data.append(vehicle_chosen)

        # Fill orders in vehicles that have already been picked
        order_filled = False
        for i in range(len(order_weights)):
            current_order_weight = order_weights[i]
            if current_order_weight == -1:
                continue

            for delivery in delivery_data:
                if delivery['space_remaining'] > 0\
                   and current_order_weight <= delivery['space_remaining']:
                    delivery['space_remaining'] -= current_order_weight
                    delivery['oders_assigned'].append(orders[i]['order_id'])
                    order_weights[i] = -1
                    order_filled = True
                    break

        # If a new vehicle was picked and order cannot be fulfilled,
        #   we dont have sufficiently large vehicles
        if not order_filled:
            raise Exception('Unable to deliver orders')

        # Remove filled orders
        while -1 in order_weights:
            idx = order_weights.index(-1)
            order_weights.pop(idx)
            orders.pop(idx)
        total_order_weight = sum(order_weights)

    return delivery_data


# Test run
if __name__ == '__main__':
    vehicles = [{
            "max_capacity": 30,
            "vehicle_type": "bike",
            "vehicles_available": 3
        },
        {
            "max_capacity": 50,
            "vehicle_type": "scooter",
            "vehicles_available": 2
        }]
    orders = [{
            'order_id': 1,
            'order_weight': 50
        },
        {
            'order_id': 2,
            'order_weight': 30
        },
        {
            'order_id': 3,
            'order_weight': 40
        }
       ]

    delivery_data = assign_orders(vehicles=vehicles, orders=orders)
    for ele in delivery_data:
        print(ele)
