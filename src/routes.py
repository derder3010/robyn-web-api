# Router api endpoint

from robyn import jsonify, Request, SubRouter
from robyn_schemas import RobynUserCreate, RobynUserUpdate
from schemas import UserCreate, UserResponse, UserUpdate
import handlers
from db import SessionLocal
from middleware import JWTAuthHandler
from robyn.authentication import BearerGetter


user_router = SubRouter(__file__, prefix="/user")
user_router.configure_authentication(JWTAuthHandler(token_getter=BearerGetter()))
auth_router = SubRouter(__file__, prefix="/auth")
auth_router.configure_authentication(JWTAuthHandler(token_getter=BearerGetter()))


@auth_router.post("/login", openapi_name="Log In User", openapi_tags=["Auth"])
async def login(request: Request):
    try:
        data = request.json()

        with SessionLocal() as db:
            token = handlers.authenticate_user(db, **data)

        if token is None:
            return jsonify({"error": "Invalid token"}), {}, 401

        return jsonify({"access_token": token}), {}, 200
    except Exception as e:
        return jsonify({"error": str(e)}), {}, 400


@auth_router.post(
    "/logout", openapi_name="Log Out User", openapi_tags=["Auth"], auth_required=True
)
async def logout(request: Request):
    try:
        decoded_token = request.identity.claims
        if decoded_token is None:
            raise ValueError("Not Authorized")
        with SessionLocal() as db:
            result = handlers.logout_user(db, decoded_token)
            return result
    except Exception as e:
        return jsonify({"error": str(e)}), {}, 400


@user_router.post(
    "/register",
    openapi_name="Create New  User",
    openapi_tags=["User Management"],
)
async def create_user(request: Request, body: RobynUserCreate):
    try:
        data = request.json()
        user_data = UserCreate(**data)

        with SessionLocal() as db:
            db_user = handlers.create_user(db, user_data)
            response_data = UserResponse.model_validate(db_user)
            return jsonify(response_data.model_dump()), {}, 201

    except Exception as e:
        return jsonify({"error": str(e)}), {}, 400


@user_router.get(
    "/me",
    openapi_name="Get User Information",
    openapi_tags=["User Management"],
    auth_required=True,
)
async def get_current_user(request):
    user = request.identity.claims["user"]
    return user


@user_router.get(
    "/:user_id",
    openapi_name="Get User Information By ID",
    openapi_tags=["User Management"],
)
async def get_user_id(request: Request):
    try:
        user_id = request.path_params.get("user_id")
        if user_id is None:
            return jsonify({"error": "User id is not provided"})

        with SessionLocal() as db:
            db_user = handlers.get_user(db, user_id)

            if not db_user:
                return jsonify({"error": "User not found"}), {}, 404

            response_data = UserResponse.model_validate(db_user)
            return jsonify(response_data.model_dump()), {}, 200

    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), {}, 400
    except Exception as e:
        return jsonify({"error": str(e)}), {}, 500


@user_router.put(
    "/update/:user_id",
    openapi_name="Update User Information",
    openapi_tags=["User Management"],
    auth_required=True,
)
async def update_user(request: Request, body: RobynUserUpdate):
    try:
        user_id = request.path_params.get("user_id")
        if user_id is None:
            return jsonify({"error": "User id is not provided"})
        data = request.json()
        update_data = UserUpdate(**data)

        with SessionLocal() as db:
            db_user = handlers.update_user(db, user_id, update_data)

            if not db_user:
                return jsonify({"error": "User not found"}), {}, 404

            response_data = UserResponse.model_validate(db_user)
            return jsonify(response_data.model_dump()), {}, 200

    except ValueError as e:
        return jsonify({"error": str(e)}), {}, 400
    except Exception as e:
        return jsonify({"error": str(e)}), {}, 500


@user_router.delete(
    "/delete/:user_id",
    openapi_name="Delete User",
    openapi_tags=["User Management"],
    auth_required=True,
)
async def delete_user(request: Request):
    try:
        user_id = request.path_params.get("user_id")
        if user_id is None:
            return jsonify({"error": "User id is not provided"})

        with SessionLocal() as db:
            db_user = handlers.delete_user(db, user_id)

            if not db_user:
                return jsonify({"error": "User not found"})
            return jsonify({"msg": "User deleted successfully"})
    except ValueError as e:
        return jsonify({"error": str(e)}), {}, 400
    except Exception as e:
        return jsonify({"error": str(e)}), {}, 500
