# Router api endpoint

from robyn import jsonify, Request, SubRouter
from schemas import UserCreate, UserResponse, UserUpdate
import handlers
from db import SessionLocal

user_router = SubRouter(__file__, prefix="/user")


@user_router.post("/register")
async def create_book(request: Request):
    try:
        data = request.json()
        user_data = UserCreate(**data)

        with SessionLocal() as db:
            db_user = handlers.create_user(db, user_data)
            response_data = UserResponse.model_validate(db_user)
            return jsonify(response_data.model_dump()), {}, 201

    except Exception as e:
        return jsonify({"error": str(e)}), {}, 400


@user_router.get("/:user_id")
async def get_user_id(request: Request):
    try:
        user_id = request.path_params.get("user_id")

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


@user_router.put("/:user_id")
async def update_user(request: Request):
    try:
        user_id = request.path_params.get("user_id")
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


@user_router.delete("/:user_id")
async def delete_user(request: Request):
    try:
        user_id = request.path_params.get("user_id")

        with SessionLocal() as db:
            db_user = handlers.delete_user(db, user_id)

            if not db_user:
                return jsonify({"error": "User not found"})
            return jsonify({"msg": "User deleted successfully"})
    except ValueError as e:
        return jsonify({"error": str(e)}), {}, 400
    except Exception as e:
        return jsonify({"error": str(e)}), {}, 500
