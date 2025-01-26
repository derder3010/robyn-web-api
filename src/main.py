from robyn import Robyn
from robyn.authentication import BearerGetter

# from routes import add_users_routes
from routes import user_router, auth_router
from middleware import BasicAuthHandler

app = Robyn(__file__)




# Create database tables (consider using migrations like Alembic in production)
# Uncomment the following line if you don't use alembic.
# from db import init_database
# init_database()


# Add routes to the app
# add_users_routes(app)
app.include_router(auth_router)
app.include_router(user_router)


app.configure_authentication(BasicAuthHandler(token_getter=BearerGetter()))


@app.get("/", auth_required=True)
def read_root(request):
    request.identity.claims["user"]
    return {"message": "Welcome to the Robyn CockroachDB Authentication API"}

if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
