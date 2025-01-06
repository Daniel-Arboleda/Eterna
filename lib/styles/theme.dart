// theme.dart
import 'package:flutter/material.dart';
import 'app_colors.dart';

final ThemeData appTheme = ThemeData(
  primaryColor: AppColors.primary,
  scaffoldBackgroundColor: AppColors.background,
  textTheme: const TextTheme(
    displayLarge: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.primary),
    bodyLarge: TextStyle(fontSize: 16, color: AppColors.textPrimary),
  ),
  appBarTheme: const AppBarTheme(
    backgroundColor: AppColors.primary,
    titleTextStyle: TextStyle(color: AppColors.secondary, fontSize: 20, fontWeight: FontWeight.bold),
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: AppColors.secondary, // Fondo dorado
      foregroundColor: AppColors.background, // Texto blanco
    ),
  ),
);
