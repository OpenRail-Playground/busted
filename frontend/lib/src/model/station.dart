class Station {
  final String id;
  final String stationName;

  Station({
    required this.id,
    required this.stationName,
  });

  factory Station.fromJson(Map<String, dynamic> json) {
    return Station(
      id: json['id'] as String,           
      stationName: json['station_name'] as String,  
    );
  }

}
