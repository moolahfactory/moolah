import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/whatsapp_service.dart';
import '../models/chat.dart';

class ChatListScreen extends StatefulWidget {
  const ChatListScreen({Key? key}) : super(key: key);

  @override
  State<ChatListScreen> createState() => _ChatListScreenState();
}

class _ChatListScreenState extends State<ChatListScreen> {
  List<Chat> _chats = [];
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _loadChats();
  }

  Future<void> _loadChats() async {
    setState(() => _loading = true);
    final config = await ApiService.getConfig();
    final phoneNumberId =
        config['phone_number_id'] ?? config['phoneNumberId'] as String;
    final items = await WhatsAppService.getChats(phoneNumberId);
    setState(() {
      _chats = items.map((e) => Chat.fromJson(e as Map<String, dynamic>)).toList();
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chats')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _chats.length,
              itemBuilder: (context, index) {
                final chat = _chats[index];
                return ListTile(
                  title: Text(chat.name),
                  onTap: () => Navigator.pushNamed(
                    context,
                    '/chat',
                    arguments: chat,
                  ),
                );
              },
            ),
    );
  }
}
