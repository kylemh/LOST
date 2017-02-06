/* This script does some patching for things that can be inferred but were left out of
   the input dataset
*/

-- Put the vehicles at the facility they start and terminate
-- If vehicles existed in the inventories, this would be unsafe
-- If vehicles existed in more than one leg, this would be unsafe
INSERT INTO asset_at (asset_fk,facility_fk,arrive_dt) SELECT asset_fk,dst_fk,arrive_dt FROM convoys c JOIN used_by u ON c.convoy_pk=u.convoy_fk JOIN vehicles v ON u.vehicle_fk=v.vehicle_pk;
INSERT INTO asset_at (asset_fk,facility_fk,depart_dt) SELECT asset_fk,src_fk,depart_dt FROM convoys c JOIN used_by u ON c.convoy_pk=u.convoy_fk JOIN vehicles v ON u.vehicle_fk=v.vehicle_pk;

-- Inventory sheets only had assets that had already arrived, infer prior locations
-- for those that were in transit. Would fail if the inventory had historic info
INSERT INTO asset_at (asset_fk,facility_fk,depart_dt) SELECT asset_fk,src_fk,load_dt
FROM  convoys c JOIN asset_on a ON convoy_pk=a.convoy_fk;