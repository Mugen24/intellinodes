-- Image should probably be stored on disc instead as a Blob
-- Example location might be /template/rgb_image_id

-- date: YYYY-MM-DDThh:mmZ
create table user (
    id integer primary key autoincrement
    temperature real
    fever_probability real 
    rgb_image_id integer autoincrement
    thermal_image_id integer autoincrement
    date_created date
)
