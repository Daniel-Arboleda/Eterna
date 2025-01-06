import 'package:flutter/material.dart';
import 'styles/theme.dart';
import 'screens/index.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Eterna',
      theme: appTheme, // Aplicar el tema global
      home: IndexScreen(),
    );
  }
}
