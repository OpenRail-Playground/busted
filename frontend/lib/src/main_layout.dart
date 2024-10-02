import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

class MainLayout extends StatelessWidget {
  final Widget child;

  const MainLayout({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        centerTitle: true,
        actions: [
          Image.asset(
            'assets/images/db.png',
            height: 30,
          ),
          const SizedBox(width: 10),
          SvgPicture.asset(
            'assets/images/obb.svg',
            height: 25,
          ),
          const SizedBox(width: 10),
          SvgPicture.asset(
            'assets/images/sncf.svg',
            height: 25,
          ),
          const SizedBox(width: 10),
          SvgPicture.asset(
            'assets/images/sbb.svg',
            height: 25,
          ),
          const SizedBox(width: 10),
          SvgPicture.asset(
            'assets/images/bls.svg',
            height: 25,
          ),
          const SizedBox(width: 30),
        ],
      ),
      body: Stack(
        children: [
          Column(
            children: [
              Expanded(
                flex: 4,
                child: Container(
                  color: const Color(0xFFEB0000),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      SizedBox(
                        height: 80,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: SvgPicture.asset(
                                "assets/images/busted_logo_white.svg",
                                width: 50,
                                height: 50,
                              ),
                            ),
                            const Text(
                              "BUS'TED!",
                              textAlign: TextAlign.start,
                              style: TextStyle(
                                fontFamily: "Calanda",
                                fontSize: 35.0,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            )
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: 6,
                child: Container(
                  color: Colors.white,
                ),
              ),
            ],
          ),
          child,
          const Align(alignment: Alignment.bottomCenter, child: Text("© Dreiländerhack 2024 BUSTERS. All rights reserved"))
        ],
      ), 
    );
  }
}
