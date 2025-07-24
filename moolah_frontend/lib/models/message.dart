class Message {
  final String id;
  final String from;
  final String body;
  final DateTime timestamp;

  Message({required this.id, required this.from, required this.body, required this.timestamp});

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'] as String,
      from: json['from'] as String,
      body: json['text']?['body'] as String? ?? '',
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }
}
