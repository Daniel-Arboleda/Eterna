import 'package:flutter/material.dart';

class AppDecorations {
  static final BoxDecoration card = BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(10),
    boxShadow: [
      BoxShadow(
        color: Colors.grey.withOpacity(0.5),
        blurRadius: 5,
        offset: Offset(0, 2),
      ),
    ],
  );
}
