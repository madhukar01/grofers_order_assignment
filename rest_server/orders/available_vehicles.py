from aiohttp import web
from aiohttp_cors import CorsViewMixin
import ujson


###############################################################################
# Fetch available vehicles
###############################################################################
class AvailableVehicles(web.View, CorsViewMixin):
    '''
    API to render available vehicles
    '''
    async def get(self):
        # Database connections
        db = self.request.app['db']
        conn = self.request.app['db_connection']

        # Fetch vehicles for given slot
        available_vehicles = await db.table('delivery_vehicles').run(conn)
        available_vehicles = [x async for x in available_vehicles]

        return web.json_response(
            status=200,
            data=available_vehicles,
            dumps=ujson.dumps)
