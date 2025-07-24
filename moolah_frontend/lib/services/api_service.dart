import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config.dart';
import '../models/transaction.dart';
import '../models/goal.dart';
import '../models/budget.dart';
import '../models/category.dart';
import '../models/reward.dart';
import '../models/user.dart';
import '../models/rewards_data.dart';

/// Service for interacting with the backend API.
class ApiService {
  static String? _baseUrl;
  static const _storage = FlutterSecureStorage();

  static Future<String> _getBaseUrl() async {
    _baseUrl ??= await Config.backendBaseUrl;
    return _baseUrl!;
  }

  static Future<String?> _getToken() => _storage.read(key: 'token');
  static Future<void> _setToken(String token) => _storage.write(key: 'token', value: token);

  static String _parseError(http.Response response) {
    try {
      final data = jsonDecode(response.body);
      if (data is Map<String, dynamic> && data['detail'] != null) {
        return data['detail'].toString();
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

  /// Authenticate a user against the backend and store the access token.
  static Future<void> login(String email, String password) async {
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.post(
      Uri.parse('$baseUrl/token'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {'username': email, 'password': password},
    ));
    final data = jsonDecode(response.body);
    await _setToken(data['access_token']);
  }

  /// Returns configuration values provided by the backend.
  static Future<Map<String, dynamic>> getConfig() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/config'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  /// Registers a new user account.
  static Future<void> register(String email, String password) async {
    final baseUrl = await _getBaseUrl();
    await _safeRequest(http.post(
      Uri.parse('$baseUrl/users/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    ));
  }

  /// Returns a list of transactions for the authenticated user.
  static Future<List<Transaction>> getTransactions({
    DateTime? startDate,
    DateTime? endDate,
    int? categoryId,
  }) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();

    final params = <String, String>{};
    if (startDate != null) {
      params['start_date'] = startDate.toIso8601String();
    }
    if (endDate != null) {
      params['end_date'] = endDate.toIso8601String();
    }
    if (categoryId != null) {
      params['category_id'] = categoryId.toString();
    }

    final uri =
        Uri.parse('$baseUrl/transactions/').replace(queryParameters: params);
    final response = await _safeRequest(http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    ));
    final items = jsonDecode(response.body) as List<dynamic>;
    return items.map((e) => Transaction.fromJson(e)).toList();
  }

  /// Retrieves the user's saving goals.
  static Future<List<Goal>> getGoals() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/goals/'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    final items = jsonDecode(response.body) as List<dynamic>;
    return items.map((e) => Goal.fromJson(e)).toList();
  }

  /// Retrieves the list of available categories.
  static Future<List<Category>> getCategories() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/categories/'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    final items = jsonDecode(response.body) as List<dynamic>;
    return items.map((e) => Category.fromJson(e)).toList();
  }

  /// Retrieves budgets defined by the user.
  static Future<List<Budget>> getBudgets() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/budgets/'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    final items = jsonDecode(response.body) as List<dynamic>;
    return items.map((e) => Budget.fromJson(e)).toList();
  }

  /// Returns reward information for the user.
  static Future<RewardsData> getRewards() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/rewards/'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return RewardsData.fromJson(data);
  }

  /// Monthly spending summary for the user.
  static Future<List<dynamic>> getMonthlySummary() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/summary/monthly'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    return jsonDecode(response.body) as List<dynamic>;
  }

  /// Spending summary grouped by category.
  static Future<List<dynamic>> getCategorySummary() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/summary/category'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    return jsonDecode(response.body) as List<dynamic>;
  }

  /// Information for the authenticated user including points and rewards.
  static Future<User> getUser() async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.get(
      Uri.parse('$baseUrl/users/me/'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    return User.fromJson(data);
  }

  /// Removes the stored authentication token.
  static Future<void> logout() => _storage.delete(key: 'token');

  // -------------------- Transactions --------------------

  static Future<Transaction> createTransaction(Transaction data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.post(
      Uri.parse('$baseUrl/transactions/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Transaction.fromJson(json);
  }

  static Future<Transaction> updateTransaction(
      int id, Transaction data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.put(
      Uri.parse('$baseUrl/transactions/$id'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Transaction.fromJson(json);
  }

  static Future<void> deleteTransaction(int id) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    await _safeRequest(http.delete(
      Uri.parse('$baseUrl/transactions/$id'),
      headers: {'Authorization': 'Bearer $token'},
    ));
  }

  // -------------------- Goals --------------------

  static Future<Goal> createGoal(Goal data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.post(
      Uri.parse('$baseUrl/goals/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Goal.fromJson(json);
  }

  static Future<Goal> updateGoal(int id, Goal data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.put(
      Uri.parse('$baseUrl/goals/$id'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Goal.fromJson(json);
  }

  static Future<Map<String, dynamic>> completeGoal(int id) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.patch(
      Uri.parse('$baseUrl/goals/$id/complete'),
      headers: {'Authorization': 'Bearer $token'},
    ));
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  static Future<void> deleteGoal(int id) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    await _safeRequest(http.delete(
      Uri.parse('$baseUrl/goals/$id'),
      headers: {'Authorization': 'Bearer $token'},
    ));
  }

  // -------------------- Categories --------------------

  static Future<Category> createCategory(Category data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.post(
      Uri.parse('$baseUrl/categories/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Category.fromJson(json);
  }

  static Future<Category> updateCategory(int id, Category data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.put(
      Uri.parse('$baseUrl/categories/$id'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Category.fromJson(json);
  }

  static Future<void> deleteCategory(int id) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    await _safeRequest(http.delete(
      Uri.parse('$baseUrl/categories/$id'),
      headers: {'Authorization': 'Bearer $token'},
    ));
  }

  // -------------------- Budgets --------------------

  static Future<Budget> createBudget(Budget data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.post(
      Uri.parse('$baseUrl/budgets/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Budget.fromJson(json);
  }

  static Future<Budget> updateBudget(int id, Budget data) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    final response = await _safeRequest(http.put(
      Uri.parse('$baseUrl/budgets/$id'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: jsonEncode(data.toJson()),
    ));
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return Budget.fromJson(json);
  }

  static Future<void> deleteBudget(int id) async {
    final token = await _getToken();
    final baseUrl = await _getBaseUrl();
    await _safeRequest(http.delete(
      Uri.parse('$baseUrl/budgets/$id'),
      headers: {'Authorization': 'Bearer $token'},
    ));
  }
}
