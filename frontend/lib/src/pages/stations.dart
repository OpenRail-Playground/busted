import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:frontend/src/main_layout.dart';
import '../model/agency.dart';
import '../model/conflict.dart';

@RoutePage()
class StationsPage extends StatefulWidget {
  final List<Agency> selectedAgencies;

  final List<String> stationNames = ['Münsingen', 'Thun', 'Spiez', 'Interlaken', 'Brig'];

  StationsPage({required this.selectedAgencies, super.key});

  @override
  _StationsPageState createState() => _StationsPageState();
}

class _StationsPageState extends State<StationsPage> {
  String? selectedTrain;
  String? selectedTrainId; 
  List<Conflict> newlyScheduledTrains = [];
  List<String>? affectedBuses;

  void _getNewlyScheduledTrains(String stationName) {
    setState(() {
      selectedTrain = stationName;
      selectedTrainId = null; 
      affectedBuses = null;
      newlyScheduledTrains = [
        Conflict(
          id: '987',
          trainName: 'IC 61',
          oldDate: DateTime(2024, 8, 15, 22, 36), // Old time
          newDate: DateTime(2024, 8, 15, 22, 37), // New time
        ),
        Conflict(
          id: '989',
          trainName: 'IC 61',
          oldDate: DateTime(2024, 8, 15, 23, 37),
          newDate: DateTime(2024, 8, 15, 23, 39),
        ),
        Conflict(
          id: '371',
          trainName: 'ICE',
          oldDate: DateTime(2024, 9, 15, 19, 33),
          newDate: DateTime(2024, 9, 15, 20, 03),
        ),
        Conflict(
          id: '956',
          trainName: 'IC 61',
          oldDate: DateTime(2024, 10, 2, 5, 18),
          newDate: DateTime(2024, 10, 2, 5, 9),
        ),
      ];
    });
  }

  void _onTrainSelected(String trainId) {
    setState(() {
      selectedTrainId = trainId; // Set the selected train ID
      affectedBuses = List.generate(
        3,
        (index) => "Bus $index",
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return MainLayout(
      child: Center(
        child: Column(
          children: [
            const SizedBox(height: 80),
            RequestBox(
              selectedAgencies: widget.selectedAgencies,
              stationNames: widget.stationNames,
              onStationSelected: _getNewlyScheduledTrains,
            ),
            const SizedBox(height: 25),
            if (selectedTrain != null)
              ResultBox(
                newlyScheduledTrains: newlyScheduledTrains,
                affectedBuses: affectedBuses == null ? [] : affectedBuses!,
                selectedTrainId: selectedTrainId, 
                onTrainSelected: _onTrainSelected,
              ),
          ],
        ),
      ),
    );
  }
}

class NewlyScheduledTrainListBox extends StatelessWidget {
  final List<Conflict> newlyScheduledTrains;
  final String? selectedTrainId;
  final Function(String) onTrainSelected;

  const NewlyScheduledTrainListBox({
    super.key,
    required this.newlyScheduledTrains,
    required this.selectedTrainId,
    required this.onTrainSelected,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 500,
      child: newlyScheduledTrains.isNotEmpty
          ? ListView.builder(
              itemCount: newlyScheduledTrains.length,
              itemBuilder: (context, index) {
                final train = newlyScheduledTrains[index];
                final isSelected = train.id == selectedTrainId;

                return GestureDetector(
                  onTap: () => onTrainSelected(train.id),
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 16.0),
                    margin: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: isSelected ? Colors.red : Colors.transparent,
                        width: 2.0,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.1),
                          blurRadius: 5,
                          spreadRadius: 1,
                          offset: const Offset(0, 3),
                        ),
                      ],
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            // Train Number in red
                            Text(
                              train.id, // Replace with train.id if train.id is the number
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Colors.red,
                              ),
                            ),
                            const SizedBox(width: 8),
                            // Train Icon
                            const Icon(
                              Icons.train,
                              size: 24,
                              color: Colors.black,
                            ),
                            const SizedBox(width: 8),
                            // Train Type (IC 61)
                            Container(
                              padding: const EdgeInsets.symmetric(vertical: 4.0, horizontal: 8.0),
                              decoration: BoxDecoration(
                                color: Colors.red,
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                train.trainName,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Old Time (Alt)
                            Row(
                              children: [
                                const Text(
                                  'Alt: ',
                                  style: TextStyle(
                                    fontSize: 14,
                                    color: Colors.black54,
                                  ),
                                ),
                                Text(
                                  '10:09', // Replace with actual old time
                                  style: const TextStyle(
                                    fontSize: 14,
                                    color: Colors.black,
                                  ),
                                ),
                              ],
                            ),
                            // New Time (Neu)
                            Row(
                              children: [
                                const Text(
                                  'Neu: ',
                                  style: TextStyle(
                                    fontSize: 14,
                                    color: Colors.red,
                                    
                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                Text(
                                  '10:11', // Replace with actual new time
                                  style: const TextStyle(
                                    fontSize: 14,
                                    color: Colors.red,
                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                );
              },
            )
          : const Center(
              child: Text('No newly scheduled trains available'),
            ),
    );
  }
}

class AffectedBusListBox extends StatelessWidget {
  final List<String> affectedBuses;

  const AffectedBusListBox({super.key, required this.affectedBuses});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            spreadRadius: 4,
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      height: 500,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Top part with journey information
          Container(
            margin: const EdgeInsets.only(bottom: 16.0),
            padding: const EdgeInsets.all(8.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  spreadRadius: 3,
                  blurRadius: 5,
                  offset: const Offset(0, 3),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Journey Route and Date
                const Text(
                  'Basel SBB → Brig',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 8),
                // Time Range
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      '07:56',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(
                      width: 10,
                    ),
                    const Icon(
                      Icons.circle, // Represent the dot
                      size: 10, // Adjust size to make it small like a dot
                      color: Colors.black,
                    ),
                    Expanded(
                      child: Divider(
                        color: Colors.black,
                        thickness: 1.5,
                      ),
                    ),
                    const Icon(
                      Icons.circle, // Represent the dot
                      size: 10, // Adjust size to make it small like a dot
                      color: Colors.black,
                    ),
                    SizedBox(
                      width: 10,
                    ),
                    const Text(
                      '10:11',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFEB0000)),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Rest of the bus list
          Expanded(
            child: ListView.builder(
              itemCount: affectedBuses.length,
              itemBuilder: (context, index) {
                return Container(
                  padding: const EdgeInsets.symmetric(vertical: 10.0),
                  margin: const EdgeInsets.only(bottom: 10.0),
                  decoration: BoxDecoration(
                    border: Border(
                      bottom: BorderSide(color: Colors.grey.withOpacity(0.3)),
                    ),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          // Bus Name
                          Text(
                            affectedBuses[index], // Bus ID like 'STI', 'PAG'
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              color: Colors.black,
                            ),
                          ),
                          const SizedBox(width: 10),
                          const Icon(Icons.directions_bus, size: 24), // Bus icon
                        ],
                      ),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          // Departure Time
                          Row(
                            children: [
                              const Text(
                                "Abfahrtszeit: ",
                                style: TextStyle(fontSize: 14, color: Colors.black54),
                              ),
                              Text(
                                "10:07", // Example departure time
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 14,
                                  color: Color(0xFFEB80000),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 5),
                          Row(
                            children: [
                              // Platform and Train Number
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: const [
                                      Text("Kante: ", style: TextStyle(color: Colors.black54)),
                                      Text("D", style: TextStyle(fontWeight: FontWeight.bold)),
                                    ],
                                  ),
                                  Row(
                                    children: const [
                                      Text("Nr.: ", style: TextStyle(color: Colors.black54)),
                                      Text("1357", style: TextStyle(fontWeight: FontWeight.bold)),
                                    ],
                                  ),
                                ],
                              ),
                              const SizedBox(width: 20),
                              // Walking Icon and Time
                              Row(
                                children: const [
                                  Icon(Icons.directions_walk, size: 20),
                                  SizedBox(width: 5),
                                  Text("4'", style: TextStyle(fontSize: 16, color: Colors.black)),
                                ],
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class ResultBox extends StatelessWidget {
  final List<Conflict> newlyScheduledTrains;
  final List<String> affectedBuses;
  final String? selectedTrainId; // To highlight the selected train
  final Function(String) onTrainSelected;

  const ResultBox({
    super.key,
    required this.newlyScheduledTrains,
    required this.affectedBuses,
    required this.selectedTrainId, // Pass the selectedTrainId to highlight the selected train
    required this.onTrainSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 860,
      child: Row(
        children: [
          Expanded(
            flex: 1,
            child: NewlyScheduledTrainListBox(
              newlyScheduledTrains: newlyScheduledTrains,
              selectedTrainId: selectedTrainId, // Pass the selectedTrainId
              onTrainSelected: onTrainSelected,
            ),
          ),
          if (affectedBuses.isNotEmpty)
            Expanded(
              flex: 1,
              child: AffectedBusListBox(affectedBuses: affectedBuses),
            ),
        ],
      ),
    );
  }
}

class RequestBox extends StatelessWidget {
  final List<Agency> selectedAgencies;
  final List<String> stationNames;
  final Function(String) onStationSelected;

  const RequestBox({
    super.key,
    required this.selectedAgencies,
    required this.stationNames,
    required this.onStationSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 860,
      height: 250,
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            spreadRadius: 4,
            blurRadius: 10,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(20),
        child: Column(
          children: [
            SizedBox(
              height: 60, // Set a fixed height
              child: Container(
                padding: EdgeInsets.only(top: 20, left: 20),
                decoration: BoxDecoration(
                  color: Colors.white, // White background for the list container
                ),
                child: ListView.builder(
                  scrollDirection: Axis.horizontal, // Horizontal scroll
                  itemCount: selectedAgencies.length,
                  itemBuilder: (context, index) {
                    final agency = selectedAgencies[index];
                    return Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8.0), // Add horizontal padding between items
                      child: Container(
                        width: 150, // Set a fixed width for each item
                        padding: EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.teal, // Background color for each item
                          borderRadius: BorderRadius.circular(10), // Rounded corners for each item
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.1),
                              blurRadius: 4,
                              offset: Offset(0, 2),
                            ),
                          ],
                        ),
                        child: Center(
                          child: Text(
                            agency.agencyName,
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                            textAlign: TextAlign.center,
                            overflow: TextOverflow.ellipsis, // Handle overflowed text
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),
            DateRangePickerExample(),
            Container(
              height: 40,
              margin: const EdgeInsets.only(top: 20, bottom: 20, left: 20),
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: stationNames.length,
                itemBuilder: (context, index) {
                  final stationName = stationNames[index];
                  return GestureDetector(
                    onTap: () => onStationSelected(stationName),
                    child: Container(
                      width: 150,
                      height: 30,
                      margin: const EdgeInsets.symmetric(horizontal: 8),
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        color: const Color(0xFFEB0000),
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.2),
                            blurRadius: 4,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: Text(
                        stationName,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        textAlign: TextAlign.center,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class DateRangePickerExample extends StatefulWidget {
  @override
  _DateRangePickerExampleState createState() => _DateRangePickerExampleState();
}

class _DateRangePickerExampleState extends State<DateRangePickerExample> {
  DateTime? _startDate;
  DateTime? _endDate;

  // Function to format date as dd.MM.yyyy
  String _formatDate(DateTime date) {
    String day = date.day.toString().padLeft(2, '0');
    String month = date.month.toString().padLeft(2, '0');
    String year = date.year.toString();
    return "$day.$month.$year";
  }

  Future<void> _selectDateRange(BuildContext context) async {
    final DateTimeRange? picked = await showDateRangePicker(
        context: context,
        firstDate: DateTime(2024, 10, 1), // Start of October 2024
        lastDate: DateTime(2024, 10, 31), // End of October 2024
        builder: (context, child) {
          return Column(
            children: [
              Container(
                constraints: BoxConstraints(maxWidth: 400.0, maxHeight: 500.0),
                child: child,
              )
            ],
          );
        });

    if (picked != null) {
      setState(() {
        _startDate = picked.start;
        _endDate = picked.end;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Bauzeitraum:',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          ),
          Container(
            padding: EdgeInsets.all(8.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 5,
                  spreadRadius: 1,
                  offset: const Offset(0, 3),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.start,
              children: <Widget>[
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Icon(Icons.calendar_today),
                    SizedBox(width: 10),
                    GestureDetector(
                      onTap: () => _selectDateRange(context),
                      child: Text(
                        _startDate == null ? '${_formatDate(DateTime.now())}' : '${_formatDate(_startDate!)}',
                        style: TextStyle(
                          fontSize: 16,
                        ),
                      ),
                    ),
                    SizedBox(width: 10),
                    GestureDetector(
                      onTap: () => _selectDateRange(context),
                      child: Text(
                        _endDate == null ? '- ${_formatDate(DateTime.now())}' : '- ${_formatDate(_endDate!)}',
                        style: TextStyle(
                          fontSize: 16,
                        ),
                      ),
                    ),
                  ],
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
