import 'package:flutter/material.dart';
import '../models/chat.dart';
import '../models/message.dart';
import '../services/api_service.dart';
import '../services/whatsapp_service.dart';

class ChatScreen extends StatefulWidget {
  final Chat chat;
  const ChatScreen({Key? key, required this.chat}) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  List<Message> _messages = [];
  String? _phoneNumberId;

  @override
  void initState() {
    super.initState();
    _loadConfig();
  }

  Future<void> _loadConfig() async {
    final config = await ApiService.getConfig();
    setState(() {
      _phoneNumberId =
          config['phone_number_id'] ?? config['phoneNumberId'] as String;
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _send() async {
    if (_controller.text.isEmpty) return;
    if (_phoneNumberId == null) {
      await _loadConfig();
      if (_phoneNumberId == null) return;
    }
    await WhatsAppService.sendMessage(_phoneNumberId!, {
      'messaging_product': 'whatsapp',
      'to': widget.chat.id,
      'type': 'text',
      'text': {'body': _controller.text},
    });
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.chat.name)),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return ListTile(
                  title: Text(msg.body),
                  subtitle: Text(msg.from),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Escribe un mensaje',
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _send,
                ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
