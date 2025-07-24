import 'package:flutter/material.dart';
import 'transactions_screen.dart';
import 'goals_screen.dart';
import 'categories_screen.dart';
import 'budgets_screen.dart';
import 'rewards_screen.dart';
import 'analytics_screen.dart';
import 'profile_screen.dart';
import 'chat_list_screen.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

Widget _buildOption(BuildContext context, String title, VoidCallback onTap) {
  return Padding(
    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    child: GestureDetector(
      onTap: onTap,
      child: Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        elevation: 0,
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(fontWeight: FontWeight.w500)),
              const Icon(Icons.arrow_forward_ios, size: 16),
            ],
          ),
        ),
      ),
    ),
  );
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  static const _introKey = 'intro_shown';
  final _storage = const FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    _showIntroIfNeeded();
  }

  Future<void> _showIntroIfNeeded() async {
    final shown = await _storage.read(key: _introKey);
    if (shown != 'true') {
      await Future.delayed(Duration.zero);
      if (!mounted) return;
      await showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Bienvenido a Moolah'),
          content: const Text(
            'Usa el menú principal para gestionar tus pagos, metas y recompensas.',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Entendido'),
            ),
          ],
        ),
      );
      await _storage.write(key: _introKey, value: 'true');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Moolah')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildOption(
              context,
              'Controlar mis pagos',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const TransactionsScreen()),
              ),
            ),
            _buildOption(
              context,
              'Mis metas de ahorro',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const GoalsScreen()),
              ),
            ),
            _buildOption(
              context,
              'Administrar categorías',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const CategoriesScreen()),
              ),
            ),
            _buildOption(
              context,
              'Configurar presupuestos',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const BudgetsScreen()),
              ),
            ),
            _buildOption(
              context,
              'Programa de recompensas',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const RewardsScreen()),
              ),
            ),
            _buildOption(
              context,
              'Aprender y mejorar mis finanzas',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const AnalyticsScreen()),
              ),
            ),
            _buildOption(
              context,
              'Mi perfil',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ProfileScreen()),
              ),
            ),
            _buildOption(
              context,
              'Mis chats de WhatsApp',
              () => Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ChatListScreen()),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
