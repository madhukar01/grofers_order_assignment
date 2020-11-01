from aiohttp import web
from aiohttp_cors import CorsViewMixin
from libraries import assign_orders
import ujson


###############################################################################
# Deliver orders
###############################################################################
class DeliverOrders(web.View, CorsViewMixin):
    '''
    API to assign orders to delivery agents
    '''
    async def post(self):
        # Decode post data
        try:
            orders_data = await self.request.json()
        except Exception as e:
            return_data = {
                'error_message': 'Unable to unpack data'
            }
            return web.json_response(
                status=400,
                data=return_data,
                dumps=ujson.dumps)

        # Log to docker - debug
        print(orders_data)

        try:
            # Validate order data
            slot_id = orders_data.get('slot_id', None)
            orders = orders_data.get('orders', [])

            # Validate slot ID
            if slot_id is None\
               or slot_id not in ['6-9', '9-13', '16-19', '19-23']:
                return_data = {
                    'error_message': 'Invalid slot ID'
                }
                return web.json_response(
                    status=400,
                    data=return_data,
                    dumps=ujson.dumps)

            # Validate order weight
            for order in orders:
                order_weight = order.get('order_weight', None)
                order_id = order.get('order_id', None)

                # Order weight cannot be more than 100 for any slot
                if order_weight > 100:
                    return_data = {
                        'error_message': 'Order weight cannot exceed 100 KG'
                    }
                    return web.json_response(
                        status=400,
                        data=return_data,
                        dumps=ujson.dumps)

                # Order weight cannot be more than 50 for first slot
                elif slot_id == '6-9' and order_weight > 50:
                    return_data = {
                        'error_message':
                        'Order weight cannot exceed 50 KG for this slot'
                    }
                    return web.json_response(
                        status=400,
                        data=return_data,
                        dumps=ujson.dumps)

        except Exception as e:
            return_data = {
                'error_message': 'Unable to unpack data'
            }
            return web.json_response(
                status=400,
                data=return_data,
                dumps=ujson.dumps)

        # Database connections
        db = self.request.app['db']
        conn = self.request.app['db_connection']

        # Fetch vehicles for given slot
        available_vehicles = await db.table('delivery_vehicles')\
            .get(slot_id).run(conn)

        if available_vehicles is None:
            return_data = {
                'error_message': 'Error occurred, Please try again later'
            }
            return web.json_response(
                status=500,
                data=return_data,
                dumps=ujson.dumps)

        # Assign order to vehicles
        try:
            delivery_data = assign_orders(
                vehicles=available_vehicles['available_vehicles'],
                orders=orders)
        except Exception as e:
            return_data = {
                'error_message': str(e)
            }
            return web.json_response(
                status=400,
                data=return_data,
                dumps=ujson.dumps)

        return web.json_response(
                status=200,
                data=delivery_data,
                dumps=ujson.dumps)
