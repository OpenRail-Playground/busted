import 'package:flutter/material.dart';
import 'package:frontend/app_router.dart';
import 'settings/settings_controller.dart';

class MyApp extends StatelessWidget {
  const MyApp({
    super.key,
    required this.settingsController,
  });

  final SettingsController settingsController;

  @override
  Widget build(BuildContext context) {
  final appRouter = AppRouter();
    return AnimatedBuilder(
      animation: settingsController,
      builder: (BuildContext context, Widget? child) {
            return MaterialApp.router(
      routerConfig: appRouter.config(),
    );
      },
    );
  }
}
