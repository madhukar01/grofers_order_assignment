from libraries import Database


###############################################################################
# Setup any modules required for rest server - called during startup
###############################################################################
async def setup_modules(app):
    # Initialize modules
    db_module = await Database()
    app['db'] = db_module.get_database()
    app['db_connection'] = db_module.get_connection()
