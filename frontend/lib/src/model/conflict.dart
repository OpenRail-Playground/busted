class Conflict {
  final String id;
  final String trainName;
  final DateTime fromDate;
  final DateTime toDate;

  Conflict({
    required this.id,
    required this.trainName,
    DateTime? oldDate, 
    DateTime? newDate,
  })  : fromDate = oldDate ?? DateTime(2024, 8, 8), 
        toDate = newDate ?? DateTime.now(); 

  factory Conflict.fromJson(Map<String, dynamic> json) {
    return Conflict(
      id: json['id'] as String,           
      trainName: json['train_name'] as String,
      oldDate: DateTime(2024, 8, 8),
      newDate: DateTime.now(), 
    );
  }
}
