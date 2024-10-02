import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';

import '../main_layout.dart';
@RoutePage()
class ConflictsPage extends StatelessWidget {
  const ConflictsPage({super.key});

  @override
  Widget build(BuildContext context) {

    return const MainLayout(
      child: 
     Text("Conflicts")
    );
  }
}
