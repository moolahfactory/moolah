class Chat {
  final String id;
  final String name;

  Chat({required this.id, required this.name});

  factory Chat.fromJson(Map<String, dynamic> json) {
    return Chat(
      id: json['id'] as String,
      name: json['name'] as String? ?? json['id'] as String,
    );
  }
}
