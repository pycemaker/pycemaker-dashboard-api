from flask_restful import Api

from .controllers.authentication import SignUpApi, LoginApi
from .controllers.user import UsersApi, UserApi
from .controllers.meal import MealsApi, MealApi
from .controllers.cpu import CpuAnalytics, CpuAnalytics_2
from .controllers.report import Report


def create_routes(api: Api):
    api.add_resource(SignUpApi, '/authentication/signup')
    api.add_resource(LoginApi, '/authentication/login')

    api.add_resource(UsersApi, '/user')
    api.add_resource(UserApi, '/user/<user_id>')

    api.add_resource(MealsApi, '/meal')
    api.add_resource(MealApi, '/meal/<meal_id>')

    api.add_resource(CpuAnalytics, '/cpu/<date_now>/<time_range>')
    api.add_resource(CpuAnalytics_2, '/cpus/<date_now>/<time_range>')

    api.add_resource(Report, '/report/<date_now>/<time_range>/<email_to>')
