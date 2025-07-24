import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/home_screen.dart';
import 'screens/transactions_screen.dart';
import 'screens/goals_screen.dart';
import 'screens/categories_screen.dart';
import 'screens/budgets_screen.dart';
import 'screens/rewards_screen.dart';
import 'screens/analytics_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/chat_list_screen.dart';
import 'screens/chat_screen.dart';
import 'models/chat.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WhatsApp Client',
      theme: ThemeData(
        useMaterial3: false,
        colorSchemeSeed: Colors.green,
      ),
      initialRoute: '/login',
      onGenerateRoute: (settings) {
        if (settings.name == '/chat') {
          final chat = settings.arguments as Chat;
          return MaterialPageRoute(builder: (_) => ChatScreen(chat: chat));
        }
        return null;
      },
      routes: {
        '/login': (_) => const LoginScreen(),
        '/register': (_) => const RegisterScreen(),
        '/home': (_) => const HomeScreen(),
        '/transactions': (_) => const TransactionsScreen(),
        '/goals': (_) => const GoalsScreen(),
        '/categories': (_) => const CategoriesScreen(),
        '/budgets': (_) => const BudgetsScreen(),
        '/rewards': (_) => const RewardsScreen(),
        '/analytics': (_) => const AnalyticsScreen(),
        '/profile': (_) => const ProfileScreen(),
        '/chats': (_) => const ChatListScreen(),
      },
    );
  }
}
