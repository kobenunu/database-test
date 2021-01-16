from Repository import repo
import DTO
import datetime
import sys

locations = []
suppliers = []


def main():
    repo.create_tables()
    create_database()
    f = open(sys.argv[2], "r")
    f2 = open(sys.argv[3], "w")
    for line in f:
        line = line.rstrip()
        lst = line[0:].split(',')
        if lst[0] in locations:
            send_shipment(lst)
        else:
            receive_shipment(lst)
        write(f2)


def write(f):
    c = ','
    insert = str(repo.DAO.total_inventory) + c + str(repo.DAO.total_demand) + c + str(repo.DAO.total_received) + c + str(repo.DAO.total_sent)
    f.write(insert + '\n')


def send_shipment(lst):
    location = lst[0]
    amount = int(lst[1])
    clinic = repo.DAO.find_clinic(location, "location")
    repo.DAO.update_clinic_demand(clinic.id, amount)
    while amount > 0:
        vaccine = get_earliest_vaccine()
        quantity = vaccine.quantity
        difference = quantity - amount
        if difference > 0:
            deliver_vaccines(vaccine.id, amount, clinic.logistic)
        else:
            delete_vaccine(vaccine.id, quantity, clinic.logistic)
        amount = amount - quantity


def receive_shipment(lst):
    supplier = get_supplier(lst[0], "name")
    supplier_id = supplier.id
    amount = int(lst[1])
    c = lst[2][4]
    date = datetime.datetime.strptime(lst[2], "%Y" + c + "%m" + c + "%d")
    vaccine_id = DTO.Vaccine.counter + 1
    add_vaccine(DTO.Vaccine(vaccine_id, date, supplier_id, amount))
    logistic_id = supplier.logistic
    update_logistic(logistic_id, amount)


def get_supplier(supplier_id, s):
    return repo.DAO.find_supplier(supplier_id, s)


def update_logistic(logistic_id, amount):
    repo.DAO.update_logistic_received(logistic_id, amount)


def get_earliest_vaccine():
    return repo.DAO.find_vaccine()


def deliver_vaccines(vaccine_id, amount, logistic_id):
    repo.DAO.update_vaccine(vaccine_id, amount)
    repo.DAO.update_logistic_sent(logistic_id, amount)


def delete_vaccine(vaccine_id, amount, logistic_id):
    repo.DAO.delete_vaccine(vaccine_id, amount)
    repo.DAO.update_logistic_sent(logistic_id, amount)


def create_database():
    f = open(sys.argv[1], "r")
    s = f.readline()
    lst = s[0:-1].split(',')
    read_vaccines(int(lst[0]), f)
    read_suppliers(int(lst[1]), f)
    read_clinics(int(lst[2]), f)
    read_logistics(int(lst[3]), f)


def read_logistics(x, f):
    for i in range(x):
        s = f.readline()
        parser = s[0:-1].split(',')
        if i == x - 1:
            parser = s.split(',')
        logistic_id = int(parser[0])
        name = parser[1]
        count_sent = int(parser[2])
        count_received = int(parser[3])
        add_logistic(DTO.Logistic(logistic_id, name, count_sent, count_received))


def read_clinics(x, f):
    for i in range(x):
        s = f.readline()
        parser = s[0:-1].split(',')
        clinic_id = int(parser[0])
        location = parser[1]
        locations.append(location)
        demand = int(parser[2])
        logistic = int(parser[3])
        add_clinic(DTO.Clinic(clinic_id, location, demand, logistic))


def read_suppliers(x, f):
    for i in range(x):
        s = f.readline()
        parser = s[0:-1].split(',')
        supplier_id = int(parser[0])
        name = parser[1]
        suppliers.append(name)
        logistic = int(parser[2])
        add_supplier(DTO.Supplier(supplier_id, name, logistic))


def read_vaccines(x, f):
    for i in range(x):
        s = f.readline()
        parser = s[0:-1].split(',')
        vaccine_id = int(parser[0])
        c = parser[1][4]
        date = datetime.datetime.strptime(parser[1], "%Y" + c + "%m" + c + "%d")
        supplier = int(parser[2])
        quantity = int(parser[3])
        add_vaccine(DTO.Vaccine(vaccine_id, date, supplier, quantity))


def add_clinic(clinic):
    repo.DAO.insert_clinic(clinic)


def add_vaccine(vaccine):
    repo.DAO.insert_vaccine(vaccine)


def add_logistic(logistic):
    repo.DAO.insert_logistic(logistic)


def add_supplier(supplier):
    repo.DAO.insert_supplier(supplier)


if __name__ == '__main__':
    main()
