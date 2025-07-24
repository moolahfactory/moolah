import 'package:flutter/material.dart';
import 'dart:io';
import '../services/api_service.dart';
import '../models/user.dart';
import '../models/reward.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  User? _user;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    try {
      final data = await ApiService.getUser();
      setState(() => _user = data);
    } on SocketException {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Sin conexión a internet')));
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _logout() async {
    await ApiService.logout();
    if (!mounted) return;
    Navigator.pushNamedAndRemoveUntil(context, '/login', (r) => false);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: Text('Perfil', style: theme.textTheme.headline6)),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _user == null
              ? const Center(child: Text('Sin datos'))
              : Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Email: ${_user!.email}',
                          style: theme.textTheme.bodyText1),
                      const SizedBox(height: 8),
                      Text('Puntos: ${_user!.points}',
                          style: theme.textTheme.bodyText1),
                      const SizedBox(height: 20),
                      const Text('Recompensas obtenidas:'),
                      ..._user!.rewards.map(
                        (Reward r) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Card(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 2,
                            child: ListTile(
                              title: Text(r.level.toString(),
                                  style: theme.textTheme.bodyText1),
                              subtitle: Text(
                                'Puntos: ${r.points} - ${r.timestamp.toIso8601String().split('T').first}',
                                style: theme.textTheme.bodyText2,
                              ),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Center(
                        child: ElevatedButton(
                          onPressed: _logout,
                          child: Text('Cerrar sesión',
                              style: theme.textTheme.button),
                        ),
                      ),
                    ],
                  ),
                ),
    );
  }
}
