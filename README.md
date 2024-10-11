# Busted

An appliction to calculate possible connection conflicts after timetable updates using GTFS data.
This PoC is using the swiss train/bus train timetable from [Opentransportdata.swiss](https://opentransportdata.swiss/de/dataset/timetable-2024-gtfs2020) and compares between two timetable releases.
If a connection was previously possible and currently isnt anymore due to schedule changes it will be reported as a conflict.

## Background

<p align="center">
  <img alt="Dreiländerhack Logo" src="img/3LH.png" width="220"/>
</p>

This project has been initiated during the [Dreiländerhack 2024](https://data.deutschebahn.com/opendata/Veranstaltungen/DreiLaenderHack-2024-12737424), a joint hackathon organised by the railway companies ÖBB, DB, and SBB.

## Install

### backend
Prerequisites for installing the backend
* python3
* pip
* sqlite3
* docker

Once the prerequisites are follow these steps
1. Go to backend code "cd backend"
2. create docker file "docker build -t busted ."
3. start docker container "docker run -d -p 5000:5000 --name busted busted"

Be aware that building the container needs ~2GB of space and starting the container can take ~30 minutes depending on the available resources. As it is parsing the complete swiss train/bus schedule for a whole year twice on startup.
If you want to exchange the data, simply overwrite the data in "resources/data".


## License

<!-- If you decide for another license, please change it here, and exchange the LICENSE file -->

The content of this repository is licensed under the [Apache 2.0 license](LICENSE).
