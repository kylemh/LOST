import csv
import sys
import psycopg2


# Connect()
if len(sys.argv) > 2:
    DB_NAME = sys.argv[1]
    DIR = sys.argv[2]
    if DIR != '' and DIR[-1] != '/':
        DIR += '/'
else:
    DB_NAME = 'lost'
    DIR = 'data/'
CONN = psycopg2.connect(dbname=DB_NAME, host='localhost', port=5432)
CUR = CONN.cursor()


def main():
    # Convert users, facilities, assets, and transfers tables to CSV files
    import_users()
    import_facilities()
    import_assets()
    import_transfers()

    # Close Postgres Database
    CUR.close()
    CONN.close()

    print('\nFinished database import!\n')
    return


def import_users():
    file = DIR + 'users.csv'
    users_insert = ("INSERT INTO users (role_fk, username, password, active) "
                    "VALUES (%s, %s, %s, %s);")

    with open(file) as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for record in rows:
            # Easy conversion of role name to role_fk
            if record['role'] == 'Logistics Officer':
                record['role'] = 2
            elif record['role'] == 'Facilities Officer':
                record['role'] = 3
            else:
                record['role'] = 1

            CUR.execute(
                users_insert, [
                    record['role'],
                    record['username'],
                    record['password'],
                    record['active']
                ]
            )
            CONN.commit()
    print('Users have been imported!')
    return


def import_facilities():
    file = DIR + 'facilities.csv'
    facilities_insert = "INSERT INTO facilities (fcode, common_name, location) VALUES (%s, %s, %s);"

    with open(file) as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for record in rows:
            CUR.execute(
                facilities_insert, [
                    record['fcode'],
                    record['common_name'],
                    record['location']
                ]
            )
            CONN.commit()
    print('Facilities have been imported!')
    return


def import_assets():
    file = DIR + 'assets.csv'
    assets_insert = "INSERT INTO assets (asset_tag, description, disposed) VALUES (%s, %s, %s);"

    asset_at_insert = ("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt, depart_dt) "
                       "VALUES (%s, %s, %s, %s);")

    with open(file) as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        for record in rows:
            if record['disposed'] == 'NULL':
                asset_disposed_bool = 'FALSE'
                record['disposed'] = None
            elif record['disposed'] == '':
                asset_disposed_bool = 'FALSE'
                record['disposed'] = None
            else:
                asset_disposed_bool = 'TRUE'

            CUR.execute(
                assets_insert, [
                    record['asset_tag'],
                    record['description'],
                    asset_disposed_bool
                ]
            )
            CONN.commit()

            CUR.execute("SELECT asset_pk FROM assets WHERE asset_tag = %s;",
                        [record['asset_tag']])
            asset_pk = CUR.fetchone()
            CONN.commit()

            CUR.execute("SELECT facility_pk FROM facilities WHERE fcode = %s;",
                        [record['facility']])
            facility_pk = CUR.fetchone()
            CONN.commit()

            CUR.execute(
                asset_at_insert, [
                    asset_pk,
                    facility_pk,
                    record['acquired'],
                    record['disposed']
                ]
            )
            CONN.commit()
    print('Assets and asset_at tables have been populated!')
    return


def import_transfers():
    file = DIR + 'transfers.csv'

    transfer_reqs_insert = ("INSERT INTO requests ("
                                "asset_fk, "
                                "user_fk, "
                                "src_fk, "
                                "dest_fk, "
                                "request_dt, "
                                "approve_dt, "
                                "approved, "
                                "approving_user_fk, "
                                "completed) "
                            "VALUES ("
                                "(SELECT asset_pk FROM assets WHERE asset_tag = %s LIMIT 1), "
                                "(SELECT user_pk FROM users WHERE username = %s), "
                                "(SELECT facility_pk FROM facilities WHERE fcode = %s), "
                                "(SELECT facility_pk FROM facilities WHERE fcode = %s), "
                                "%s, "
                                "%s, "
                                "%s, "
                                "(SELECT user_pk FROM users WHERE username = %s), "
                                "%s)")

    in_transit_insert = ("INSERT INTO in_transit (request_fk, load_dt, unload_dt) "
                         "VALUES (%s, %s, %s);")

    with open(file) as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",", quotechar="'")
        if __name__ == '__main__':
            for record in rows:
                print('\nCURRENT RECORD:', record)
                # Insert into requests table...
                if record['approve_dt'] == '':
                    approved = 'FALSE'
                else:
                    approved = 'TRUE'

                unload_dt = record['unload_dt']
                if unload_dt == '' or unload_dt == 'NULL' or unload_dt is None:
                    completed = 'FALSE'
                else:
                    completed = 'TRUE'

                CUR.execute(
                    transfer_reqs_insert, (
                        record['asset_tag'],
                        record['request_by'],
                        record['source'],
                        record['destination'],
                        record['request_dt'],
                        record['approve_dt'],
                        approved,
                        record['approve_by'],
                        completed
                    )
                )
                CONN.commit()

                # Insert into in_transit table...
                CUR.execute("SELECT request_pk FROM requests;")
                request_fk = CUR.fetchall()[-1][0]
                CONN.commit()

                load_dt = record['load_dt']
                if load_dt == '':
                    load_dt = None
                    unload_dt = None  # LOGIC: If no load time, then no unload time!
                else:
                    if unload_dt == '':
                        unload_dt = None

                print('\nHere\'s the in_transit entry:', request_fk, load_dt, unload_dt, '\n')

                CUR.execute(
                    in_transit_insert, [
                        request_fk,
                        load_dt,
                        unload_dt
                    ]
                )
                CONN.commit()
    print('Requests and in_transit tables have been populated!')
    return


if __name__ == '__main__':
    main()
