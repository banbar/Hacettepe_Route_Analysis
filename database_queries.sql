-- Spotting the notable routes (Figures 3 & 4): 

--Routes of point A: d_osrm ~3058, d_legacy~433 (pedestrian)
select id, start_building_id, end_building_id, dist_legacy, dist_osrm
from route_comparisons
where travel_mode = 'yaya' and dist_osrm > 3000 and dist_osrm < 3100
                               and dist_legacy > 410 and dist_legacy < 450
--Route ID: 4183
-- Start_Building_ID: 1705
-- End_building_ID: 1128

-- Obtaining the geometries in the legacy database and OSRM
select geom_legacy, geom_osrm
from route_comparisons
where id =4183


--Routes of point B: d_osrm ~67, d_legacy~304 (Bicycle)
select id, start_building_id, end_building_id, dist_legacy, dist_osrm
from route_comparisons
where travel_mode = 'bisiklet' and dist_osrm > 55 and dist_osrm < 75
                               and dist_legacy > 290 and dist_legacy < 320
--Route ID: 10787
-- Start_Building_ID: 1405
-- End_building_ID: 1391

-- Obtaining the geometries in the legacy database and OSRM
select geom_legacy, geom_osrm
from route_comparisons
where id =10787