import 'dart:convert';
import 'dart:io';
import 'package:flutter/services.dart' show rootBundle;

/// Provides configuration values for the app.
class Config {
  static String? _apiBaseUrl;
  static String? _backendBaseUrl;
  static String? _phoneNumberId;

  /// Returns the base URL for the WhatsApp API.
  static Future<String> get apiBaseUrl async {
    if (_apiBaseUrl != null) return _apiBaseUrl!;
    final env = Platform.environment['API_BASE_URL'];
    if (env != null && env.isNotEmpty) {
      _apiBaseUrl = env;
      return _apiBaseUrl!;
    }
    try {
      final jsonString = await rootBundle.loadString('assets/config.json');
      final data = jsonDecode(jsonString) as Map<String, dynamic>;
      final url = data['apiBaseUrl'];
      if (url is String && url.isNotEmpty) {
        _apiBaseUrl = url;
        return _apiBaseUrl!;
      }
    } catch (_) {}
    _apiBaseUrl = 'https://graph.facebook.com/v18.0';
    return _apiBaseUrl!;
  }

  /// Base URL for the backend server.
  static Future<String> get backendBaseUrl async {
    if (_backendBaseUrl != null) return _backendBaseUrl!;
    final env = Platform.environment['BACKEND_BASE_URL'];
    if (env != null && env.isNotEmpty) {
      _backendBaseUrl = env;
      return _backendBaseUrl!;
    }
    try {
      final jsonString = await rootBundle.loadString('assets/config.json');
      final data = jsonDecode(jsonString) as Map<String, dynamic>;
      final url = data['backendBaseUrl'];
      if (url is String && url.isNotEmpty) {
        _backendBaseUrl = url;
        return _backendBaseUrl!;
      }
    } catch (_) {}
    _backendBaseUrl = 'http://localhost:8000';
    return _backendBaseUrl!;
  }

  /// WhatsApp business phone number ID.
  static Future<String> get phoneNumberId async {
    if (_phoneNumberId != null) return _phoneNumberId!;
    final env = Platform.environment['PHONE_NUMBER_ID'];
    if (env != null && env.isNotEmpty) {
      _phoneNumberId = env;
      return _phoneNumberId!;
    }
    try {
      final jsonString = await rootBundle.loadString('assets/config.json');
      final data = jsonDecode(jsonString) as Map<String, dynamic>;
      final id = data['phoneNumberId'];
      if (id is String && id.isNotEmpty) {
        _phoneNumberId = id;
        return _phoneNumberId!;
      }
    } catch (_) {}
    _phoneNumberId = '';
    return _phoneNumberId!;
  }
}
