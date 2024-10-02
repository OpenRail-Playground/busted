class Agency {
  final String id;
  final String agencyName;

  Agency({
    required this.id,
    required this.agencyName,
  });

  factory Agency.fromJson(Map<String, dynamic> json) {
    return Agency(
      id: json['id'] as String,
      agencyName: json['agency_name'] as String,
    );
  }
}
