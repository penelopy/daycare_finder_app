from datetime import datetime, date, time
import model
import csv

def load_centers(session): 
    # f = open('seed_data/centers.csv','rb')

    with open('seed_data/centers.csv', 'rU') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', dialect=csv.excel_tab)
        for fields in datareader:

    # lines = f.readlines()
    # for line in lines:
    #     fields = line.split(',')

            if fields[12] == "":
                fields[12] = 3
            else:
                fields[12] = int(fields[12])

            if fields[20] == "":
                fields[20] = 1

            if fields[17] == "No":
                fields[17] = False
            else:
                fields[17] = True

            if fields[16] == "No":
                fields[16] = False
            else:
                fields[16] = True

                # title = title.decode("latin-1")

            newcenter = model.Center(id = fields[0],
                            username= fields[1],
                            email = fields[2],
                            password = fields[3],
                            biz_name = fields[4].decode("latin-1"), 
                            primary_contact = fields[5], 
                            zipcode = fields[6], 
                            neighborhood = fields[7], 
                            address = fields[8], 
                            phone = fields[9], 
                            web_url = fields[10], 
                            fb_url = fields[11], 
                            yr_in_biz = fields[12], 
                            capacity = fields[13], 
                            num_staff = fields[14], 
                            license_num = fields[15], 
                            current_openings = fields[16], 
                            special_needs = fields[17], 
                            opening_time = fields[18],   
                            closing_time = fields[19],   
                            type_of_center_id = fields[20], 
                            rate = fields[21], 
                            about_us = fields[22], 
                            philosophy = fields[23], 
                            activities = fields[24], 
                            )

            session.add(newcenter)

    # f.close()


def load_parents(session):
    f = open('seed_data/parents.csv','r')
    f = f.read().split("\r")

    for line in f:
        fields = line.split(',')

        print "fields =", fields

        newparent = model.Parent(id=fields[0],
                        first_name=fields[1],
                        last_name=fields[2],
                        username=fields[3],
                        email=fields[4],
                        password=fields[5],
                        zipcode=fields[6],
                        neighborhood=fields[7],
                        )
        session.add(newparent)

    # f.close()

def load_languages(session):
    f = open('seed_data/languages.csv','r')

    lines = f.readlines()

    for line in lines:
        fields = line.split(',')

        newlanguage = model.Language(id=fields[0],
                        name=fields[1])

        session.add(newlanguage)

    f.close()


def load_schedules(session):
    f = open('seed_data/schedule.csv','r')

    lines = f.readlines()

    for line in lines:
        fields = line.split(',')

        newschedule = model.Schedule(id=fields[0],
                        name=fields[1])

        session.add(newschedule)

    f.close()

def load_types(session):
    f = open('seed_data/types.csv','r')

    lines = f.readlines()

    for line in lines:
        fields = line.split(',')

        newtype = model.Type(id=fields[0],
                        name=fields[1])

        session.add(newtype)

    f.close()

def main(session):
    load_centers(session)
    # load_parents(session)
    # load_languages(session)
    # load_schedules(session)
    # load_types(session)
    session.commit()

if __name__ == "__main__":
    # session = model.connect()
    session = model.db_session
    main(session)