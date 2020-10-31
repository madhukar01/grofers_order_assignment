from aiohttp import web
import aiohttp_cors


###############################################################################
# URL Routes for rest server
###############################################################################
def setup_routes(app):
    # Add URL Routes
    app.add_routes(())

    #  Enable CORS over all routes
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
         allow_credentials=True,
         expose_headers='*',
         allow_headers='*')
        }
    )

    for route in list(app.router.routes()):
        cors.add(route, webview=True)
