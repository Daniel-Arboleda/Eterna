import 'package:flutter/material.dart';

class AuthService {
  // Simular creación de usuarios
  Future<bool> createUser(String email, String password) async {
    // Aquí conectarás con el backend o Firebase más adelante
    await Future.delayed(Duration(seconds: 1)); // Simular tiempo de respuesta
    print('Usuario creado: $email');
    return true;
  }

  // Simular inicio de sesión
  Future<bool> loginUser(String email, String password) async {
    await Future.delayed(Duration(seconds: 1)); // Simular tiempo de respuesta
    print('Usuario autenticado: $email');
    return true;
  }
}
