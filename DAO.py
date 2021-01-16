import DTO


class _DAO:
    def __init__(self, conn):
        self._conn = conn
        self.cursor = conn.cursor()
        self.total_inventory = 0
        self.total_demand = 0
        self.total_received = 0
        self.total_sent = 0

    def insert_vaccine(self, vaccine):
        self._conn.execute("INSERT INTO Vaccines(id, date, supplier, quantity) VALUES(?, ?, ?, ?)",
                           vaccine.getmembers())
        self.total_inventory += vaccine.quantity

    def find_vaccine(self):
        c = self.cursor
        c.execute("SELECT * FROM Vaccines ORDER BY date")
        return DTO.Vaccine(*c.fetchone())

    def update_vaccine(self, vaccine_id, amount):
        self._conn.execute("UPDATE Vaccines SET quantity = quantity - ? WHERE id = ?",
                           [amount, vaccine_id])
        self.total_inventory -= amount

    def delete_vaccine(self, vaccine_id, amount):
        self._conn.execute("DELETE FROM Vaccines WHERE id = ?",
                           [vaccine_id])
        self.total_inventory -= amount

    def insert_supplier(self, supplier):
        self._conn.execute("INSERT INTO Suppliers(id, name, logistic) VALUES(?, ?, ?)",
                           supplier.getmembers())

    def find_supplier(self, info, with_what):
        c = self.cursor
        c.execute("SELECT * FROM Suppliers WHERE " + with_what + " = ?", [info])
        return DTO.Supplier(*c.fetchone())

    def insert_clinic(self, clinic):
        self._conn.execute("INSERT INTO Clinics(id, location, demand, logistic) VALUES(?, ?, ?, ?)",
                           clinic.getmembers())
        self.total_demand += clinic.demand

    def find_clinic(self, info, with_what):
        c = self.cursor
        c.execute("SELECT * FROM Clinics WHERE " + with_what + " = ?", [info])
        return DTO.Clinic(*c.fetchone())

    def insert_logistic(self, logistic):
        self._conn.execute("INSERT INTO Logistics(id, name, count_sent, count_received) VALUES(?, ?, ?, ?)",
                           logistic.getmembers())
        self.total_sent += logistic.count_sent
        self.total_received += logistic.count_received

    def update_clinic_demand(self, clinic_id, amount):
        self._conn.execute("UPDATE Clinics SET demand = demand - ? WHERE id = ?",
                           [amount, clinic_id])
        self.total_demand -= amount

    def find_logistic(self, logistic_id):
        c = self.cursor
        c.execute("SELECT * FROM Logistics WHERE id = ?", [logistic_id])
        return DTO.Logistic(*c.fetchone())

    def update_logistic_received(self, logistic_id, amount):
        self._conn.execute("UPDATE Logistics SET count_received = count_received + ? WHERE id = ?",
                           [amount, logistic_id])
        self.total_received += amount

    def update_logistic_sent(self, logistic_id, amount):
        self._conn.execute("UPDATE Logistics SET count_sent = count_sent + ? WHERE id = ?",
                           [amount, logistic_id])
        self.total_sent += amount
