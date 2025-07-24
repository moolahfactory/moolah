import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config.dart';

/// Simple service to interact with WhatsApp Business API.
class WhatsAppService {
  static const _storage = FlutterSecureStorage();
  static String? _baseUrl;

  static Future<String> _getBaseUrl() async {
    _baseUrl ??= await Config.apiBaseUrl;
    return _baseUrl!;
  }

  static Future<String?> _getToken() => _storage.read(key: 'token');
  static Future<void> _setToken(String token) => _storage.write(key: 'token', value: token);

  static String _parseError(http.Response response) {
    try {
      final data = jsonDecode(response.body);
      if (data is Map<String, dynamic> && data['error'] != null) {
        return data['error'].toString();
      }
    } catch (_) {}
    return 'Error ${response.statusCode}';
  }

  static Future<http.Response> _safeRequest(Future<http.Response> future) async {
    try {
      final response = await future;
      if (response.statusCode >= 200 && response.statusCode < 300) {
        return response;
      }
      throw Exception(_parseError(response));
    } on SocketException {
      throw Exception('No se pudo conectar al servidor');
    }
  }

  /// Stores a token to authenticate requests.
  static Future<void> login(String token) async {
    await _setToken(token);
  }

  /// Fetches chats for the business phone number.
  static Future<List<dynamic>> getChats(String phoneNumberId) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/$phoneNumberId/messages'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return data['messages'] as List<dynamic>? ?? [];
  }

  /// Sends a text message using the API.
  static Future<void> sendMessage(
    String phoneNumberId,
    Map<String, dynamic> payload,
  ) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    await _safeRequest(http.post(
      Uri.parse('$baseUrl/$phoneNumberId/messages'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(payload),
    ));
  }
}
