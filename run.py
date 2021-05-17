from wsgiref.simple_server import make_server

from boxwood_framework.main import Framework, FakeApplication, DebugApplication
from urls import fronts
from views import routes

# application = Framework(routes, fronts)

# application = FakeApplication(routes, fronts)

application = DebugApplication(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
