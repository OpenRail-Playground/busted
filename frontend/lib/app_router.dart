import 'package:auto_route/auto_route.dart';

import 'app_router.gr.dart';

@AutoRouterConfig(replaceInRouteName: 'Page,Route')
class AppRouter extends RootStackRouter {
  @override
  RouteType get defaultRouteType => const RouteType.material(); 

  @override
  List<AutoRoute> get routes => [
        RedirectRoute(path: '/', redirectTo: '/agencies'),
        AutoRoute(path: '/agencies', page: AgenciesRoute.page),
        AutoRoute(path: '/stations', page: StationsRoute.page),
        AutoRoute(path: '/conflicts', page: ConflictsRoute.page),
      ];
}
