import 'package:flutter/material.dart';

class IndexScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2, // Dos pestañas: Login y Crear Usuario
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Eterna'),
          backgroundColor: const Color(0xFF021229),
          bottom: const TabBar(
            indicatorColor: Color(0xFFC19A6B),
            labelColor: Color(0xFFC19A6B),
            unselectedLabelColor: Colors.white,
            tabs: [
              Tab(text: 'Iniciar Sesión'),
              Tab(text: 'Crear Usuario'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            LoginForm(), // Componente del formulario de inicio de sesión
            RegisterForm(), // Componente del formulario de registro
          ],
        ),
      ),
    );
  }
}

class LoginForm extends StatelessWidget {
  const LoginForm({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text(
            'Bienvenido de nuevo',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Color(0xFF021229),
            ),
          ),
          const SizedBox(height: 20),
          TextField(
            decoration: const InputDecoration(
              labelText: 'Correo Electrónico',
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.emailAddress, // Permite entrada de email
          ),
          const SizedBox(height: 20),
          TextField(
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Contraseña',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFC19A6B), // Botón dorado
            ),
            onPressed: () {
              // Lógica para iniciar sesión
            },
            child: const Text('Iniciar Sesión'),
          ),
        ],
      ),
    );
  }
}

class RegisterForm extends StatelessWidget {
  const RegisterForm({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text(
            'Crea una cuenta',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Color(0xFF021229),
            ),
          ),
          const SizedBox(height: 20),
          TextField(
            decoration: const InputDecoration(
              labelText: 'Nombre de Usuario',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 20),
          TextField(
            decoration: const InputDecoration(
              labelText: 'Correo Electrónico',
              border: OutlineInputBorder(),
            ),
            keyboardType: TextInputType.emailAddress, // Permite entrada de email
          ),
          const SizedBox(height: 20),
          TextField(
            obscureText: true,
            decoration: const InputDecoration(
              labelText: 'Contraseña',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFC19A6B), // Botón dorado
            ),
            onPressed: () {
              // Lógica para crear usuario
            },
            child: const Text('Crear Cuenta'),
          ),
        ],
      ),
    );
  }
}
