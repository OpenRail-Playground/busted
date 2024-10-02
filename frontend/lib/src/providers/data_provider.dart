import 'dart:convert';
import 'package:frontend/src/model/agency.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/services.dart' show rootBundle;
import 'package:logger/web.dart';

class DataProvider {
  final String baseUrl;

  DataProvider({required this.baseUrl});
  var logger = Logger();



  // Fetch agencies
  Future<List<Agency>> fetchAgencies() async {
    final response = await http.get(Uri.parse('$baseUrl/agencies'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load agencies');
    }
  }

  // Fetch stations
  Future<List<dynamic>> fetchStations() async {
    final response = await http.get(Uri.parse('$baseUrl/stations'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load stations');
    }
  }

  // Fetch conflicts
  Future<List<dynamic>> fetchConflicts() async {
    final response = await http.get(Uri.parse('$baseUrl/conflicts'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load conflicts');
    }
  }

  Future<List<Agency>> fetchAgenciesFromJson() async {
    try {
      final String response = await rootBundle.loadString('assets/data/agencies.json');

      List<dynamic> jsonList = json.decode(response);

      return jsonList.map((json) => Agency.fromJson(json)).toList();
    } catch (e) {
      logger.d("Error parsing JSON: $e");
      return [];
    }
  }

  //   Future<List<Station>> fetchStationsFromJson() async {
  //   try {
  //     final String response = await rootBundle.loadString('assets/data/stations.json');

  //     List<dynamic> jsonList = json.decode(response);

  //     return jsonList.map((json) => Station.fromJson(json)).toList();
  //   } catch (e) {
  //     logger.d("Error parsing JSON: $e");
  //     return [];
  //   }
  // }
}
