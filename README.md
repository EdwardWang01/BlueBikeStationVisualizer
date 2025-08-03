# BlueBikeStationVisualizer
Visualizes real-time Bluebike station activity in Boston using GBFS data from the Bluebike API in a timelapse animation

Code comes packaged in two python scripts in the bluebike_data folder. Run all code from that folder as it will be used as the main directory to access the newly generated JSON and CSV files. 

The first script "bluebike_requests" pulls JSON files from the Bluebike API. This includes station information (ID, longitude, latitude, name, max capacity, etc..) and more importantly, starts the collection of live Bluebike dock data (as .JSON) at regular 5 minute intervals. 

The second script "process_snapshots" takes all the collected blubike dock data and synthesizes it into a time-series with the number of bluebikes parked at each dock across every dock in 5-minute snapshots. It then takes this time-series and plots each bluebike dock onto a map of the Boston Area using the lat/lon data from the pulled station_information. The map is animated such that every second shows an updated 5-minute snapshot where each dock is represented as a dot with color indicating fullness:

🔴 Red: empty
🟡 Yellow: ~half full
🟢 Green: full
