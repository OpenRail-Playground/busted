import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app_router.gr.dart';

import '../main_layout.dart';
import '../model/agency.dart';
import '../providers/data_provider.dart';

@RoutePage()
class AgenciesPage extends StatelessWidget {
  const AgenciesPage({super.key});

  @override
  Widget build(BuildContext context) {
    final dataProvider = DataProvider(baseUrl: 'https://example.com/api');

    final Map<String, ValueNotifier<bool>> checkboxStates = {};

    final ValueNotifier<List<Agency>> selectedAgencies = ValueNotifier<List<Agency>>([]);

    final ValueNotifier<String> searchQuery = ValueNotifier<String>('');

    return MainLayout(
      child: Center(
        child: Container(
          width: 480,
          height: 650,
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
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 16.0, horizontal: 16.0),
              color: Colors.white,
              child: FutureBuilder<List<Agency>>(
                future: dataProvider.fetchAgenciesFromJson(), 
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  } else if (snapshot.hasError) {
                    return Center(child: Text('Error: ${snapshot.error}'));
                  } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return const Center(child: Text('No agencies found'));
                  } else {
                    final agencies = snapshot.data!;

                    for (var agency in agencies) {
                      checkboxStates[agency.id] ??= ValueNotifier(false);
                    }

                    return Column(
                      children: [
                        // Selected Agencies
                        // ValueListenableBuilder<List<Agency>>(
                        //   valueListenable: selectedAgencies,
                        //   builder: (context, selected, _) {
                        //     return selected.isEmpty
                        //         ? const SizedBox.shrink()
                        //         : Column(
                        //             children: [
                        //               const Text(
                        //                 'Selected Agencies:',
                        //                 style: TextStyle(fontWeight: FontWeight.bold),
                        //               ),
                        //               Wrap(
                        //                 children: selected
                        //                     .map(
                        //                       (agency) => Chip(
                        //                         label: Text(agency.agencyName),
                        //                         onDeleted: () {
                        //                           checkboxStates[agency.id]!.value = false;
                        //                           selectedAgencies.value =
                        //                               List.from(selectedAgencies.value)
                        //                                 ..remove(agency);
                        //                         },
                        //                       ),
                        //                     )
                        //                     .toList(),
                        //               ),
                        //             ],
                        //           );
                        //   },
                        // ),

                        // Search bar
                        Padding(
                          padding: const EdgeInsets.only(bottom: 16.0),
                          child: TextField(
                            decoration: InputDecoration(
                              hintText: 'Search agencies...',
                              prefixIcon: const Icon(Icons.search),
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(20),
                              ),
                            ),
                            onChanged: (query) {
                              searchQuery.value = query;
                            },
                          ),
                        ),

                        Expanded(
                          child: ValueListenableBuilder<String>(
                            valueListenable: searchQuery,
                            builder: (context, query, child) {
                              final filteredAgencies = agencies.where((agency) {
                                return agency.agencyName
                                    .toLowerCase()
                                    .contains(query.toLowerCase());
                              }).toList();

                              final sortedAgencies = [
                                ...filteredAgencies.where((agency) =>
                                    checkboxStates[agency.id]?.value ?? false),
                                ...filteredAgencies.where((agency) =>
                                    !(checkboxStates[agency.id]?.value ?? false)), 
                              ];

                              if (sortedAgencies.isEmpty) {
                                return const Center(child: Text('No agencies found'));
                              }

                              return ListView.builder(
                                itemCount: sortedAgencies.length,
                                itemBuilder: (context, index) {
                                  final agency = sortedAgencies[index];

                                  return ListTile(
                                    title: Text(agency.agencyName),
                                    trailing: ValueListenableBuilder<bool>(
                                      valueListenable: checkboxStates[agency.id]!,
                                      builder: (context, isChecked, _) {
                                        return Checkbox(
                                          value: isChecked,
                                          onChanged: (bool? value) {
                                            checkboxStates[agency.id]!.value = value ?? false;

                                            if (value == true) {
                                              selectedAgencies.value = [
                                                ...selectedAgencies.value,
                                                agency
                                              ];
                                            } else {
                                              selectedAgencies.value = List.from(
                                                  selectedAgencies.value)
                                                ..remove(agency);
                                            }
                                          },
                                        );
                                      },
                                    ),
                                    onTap: () {
                                      final isSelected =
                                          checkboxStates[agency.id]!.value;
                                      checkboxStates[agency.id]!.value = !isSelected;

                                      if (!isSelected) {
                                        selectedAgencies.value = [
                                          ...selectedAgencies.value,
                                          agency
                                        ];
                                      } else {
                                        selectedAgencies.value = List.from(
                                            selectedAgencies.value)
                                          ..remove(agency);
                                      }
                                    },
                                  );
                                },
                              );
                            },
                          ),
                        ),

                        // Next button
                        Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: SizedBox(
                            height: 38.0,
                            width: double.infinity,
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                  foregroundColor: Colors.white,
                                  backgroundColor: const Color(0xFFEB0000),
                                  padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 20),
                                  textStyle: const TextStyle(fontWeight: FontWeight.bold)),
                              onPressed: () {
                                final selected = selectedAgencies.value;

                                if (selected.isNotEmpty) {
                                  context.router.push(
                                    StationsRoute(selectedAgencies: selected),
                                  );
                                } else {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text('Please select at least one agency'),
                                    ),
                                  );
                                }
                              },
                              child: const Text(
                                'Weiter',
                                style: TextStyle(color: Colors.white),
                              ),
                            ),
                          ),
                        ),
                      ],
                    );
                  }
                },
              ),
            ),
          ),
        ),
      ),
    );
  }
}
