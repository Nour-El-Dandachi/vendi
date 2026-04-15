import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    const primary = Color(0xFFA25557);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        foregroundColor: primary,
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: const Center(
        child: Text('Profile Screen'),
      ),
    );
  }
}