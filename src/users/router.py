from fastapi import APIRouter, Response, Depends
from src.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dependencies import get_current_user, get_current_admin_user
from src.users.models import User
from src.users.repo import repo
from src.users.schemas import SUserRegister, SUserAuth

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
def register_user(user_data: SUserRegister) -> dict:
    user = repo.load_by_login(user_data.login)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    repo.save(User(login=user_dict['login'], password=user_dict['password']))
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/login/")
def auth_user(response: Response, user_data: SUserAuth):
    check = authenticate_user(login=user_data.login, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}


@router.post("/logout/")
def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me/")
def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.get("/all_users/")
def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return repo.load_all()
