import bisect
import copy


def assign_orders(vehicles, orders):
    if len(orders) < 1:
        raise Exception('No orders to deliver')

    if len(vehicles) < 1:
        raise Exception('No vehicles to deliver orders')

    # Data pre processing
    # Sort orders in increasing order of weights
    orders.sort(key=lambda x: x['order_weight'])
    order_weights = [x['order_weight'] for x in orders]

    # Sort vehicles in increasing order of max capacity
    vehicles.sort(key=lambda x: x['max_capacity'])
    available_vehicles = []
    for vehicle in vehicles:
        number_of_vehicles = vehicle.pop('vehicles_available')
        for i in range(number_of_vehicles):
            available_vehicles.append(copy.deepcopy(vehicle))

    vehicle_weights = [x['max_capacity'] for x in available_vehicles]

    # Now we have pre-processed the data. Sample below
    # order_weights = [10, 20, 30, 30]
    # vehicle_weights = [30, 30, 30, 50, 50, 100]

    # Assign order to vehicles
    total_order_weight = sum(order_weights)
    total_vehicle_capacity = sum(vehicle_weights)
    delivery_data = []

    # Check if all order can be delivered with available vehicles
    if total_order_weight > total_vehicle_capacity:
        raise Exception('Total order weight exceed total vehicle capacity')

    while total_order_weight > 0:
        number_of_vehicles = len(vehicle_weights)
        if number_of_vehicles == 0:
            raise Exception('Insufficient vehicles to deliver orders')

        # Choose largest available vehicle to accommodate remaining orders
        vehicle_index = bisect.bisect_left(vehicle_weights, total_order_weight)
        if vehicle_index == number_of_vehicles:
            vehicle_index = number_of_vehicles - 1

        # Check if largest remaining order can be delivered in this vehicle
        current_vehicle_weight = vehicle_weights.pop(vehicle_index)
        if current_vehicle_weight < order_weights[-1]:
            raise Exception('Unable to deliver orders')

        vehicle_chosen = available_vehicles.pop(vehicle_index)
        vehicle_chosen['space_remaining'] = current_vehicle_weight
        vehicle_chosen['oders_assigned'] = []
        delivery_data.append(vehicle_chosen)

        # Fill orders in the chosen vehicle
        while vehicle_chosen['space_remaining'] > 0:
            order_index = bisect.bisect_right(
                order_weights,
                vehicle_chosen['space_remaining']) - 1

            # Vehicle is full, cannot load any more orders
            if order_index < 0:
                break

            chosen_order = orders.pop(order_index)
            order_weights.pop(order_index)
            vehicle_chosen['space_remaining'] -= chosen_order['order_weight']
            vehicle_chosen['oders_assigned'].append(chosen_order)

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
            'order_weight': 50
        },
        {
            'order_id': 3,
            'order_weight': 15
        }
       ]

    delivery_data = assign_orders(vehicles=vehicles, orders=orders)
    for ele in delivery_data:
        print(ele)
