import 'dart:convert';
import 'package:http/http.dart' as http;

class UserSession {
  final String id;
  final String name;
  final String email;
  final String role;

  UserSession({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
  });

  factory UserSession.fromJson(Map<String, dynamic> json) {
    return UserSession(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      role: json['role'] ?? 'student',
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'email': email,
    'role': role,
  };
}

class AuthService {
  static UserSession? _currentSession;

  static UserSession? get currentSession => _currentSession;
  static bool get isAuthenticated => _currentSession != null;

  static Future<bool> login(String email, String password, String role) async {
    final cleanEmail = email.trim().toLowerCase();
    final cleanPassword = password.trim();
    final cleanRole = role.trim().toLowerCase();

    try {
      final response = await http.post(
        Uri.parse('http://10.0.2.2:8000/api/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': cleanEmail,
          'password': cleanPassword,
          'role': cleanRole,
        }),
      ).timeout(const Duration(seconds: 3));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['authenticated'] == true && data['user'] != null) {
          _currentSession = UserSession.fromJson(data['user']);
          return true;
        }
      }
    } catch (_) {
      // Offline fallback
    }

    // Demo credentials fallback
    if (cleanEmail == 'student@learnsync.ai' && cleanPassword == 'student123' && cleanRole == 'student') {
      _currentSession = UserSession(id: 'std_001', name: 'Santhosh', email: cleanEmail, role: 'student');
      return true;
    }

    if (cleanEmail == 'faculty@learnsync.ai' && cleanPassword == 'faculty123' && cleanRole == 'faculty') {
      _currentSession = UserSession(id: 'fac_001', name: 'Prof. R. Sharma', email: cleanEmail, role: 'faculty');
      return true;
    }

    return false;
  }

  static void logout() {
    _currentSession = null;
  }
}
