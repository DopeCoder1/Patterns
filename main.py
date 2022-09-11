import json
from typing import Dict
import os.path


class General:
    def __init__(self, salary: float, mrp: float) -> None:
        self.mrp = mrp
        self.salary = salary
        self.opv = None
        self.vosms = None
        self.ipn = None
        self.zp = None
        self.co = None
        self.cn = None
        self.osms = None

    def set_config(self, opv, vosms, ipn, co, cn, osms) -> None:
        self.opv = (self.salary * opv) / 100
        self.vosms = (self.salary * vosms) / 100
        self.ipn = ((self.salary - self.opv - (14 * self.mrp) - self.vosms) * ipn) / 100
        self.zp = (self.salary - self.opv - self.ipn - self.vosms)
        self.co = ((self.salary - self.opv) * co) / 100
        self.cn = (((self.salary - self.opv - self.vosms) * cn) / 100) - self.co
        self.osms = (self.salary * osms) / 100

    def get_config_file(self, opv, vosms, ipn, co, cn, osms) -> Dict:
        return {
            "VERSION": "GENERAL",
            "SALARY_SET": self.salary,
            "MRP_SET": self.mrp,
            "OPV_SET": opv,
            "VOSMS_SET": vosms,
            "IPN_SET": ipn,
            "CO_SET": co,
            "CH_SET": cn,
            "OSMS_SET": osms
        }

    def get_config(self) -> Dict:
        return {
            "REPORT GENERAL": {
                "SALARY": self.salary,
                "MRP": self.mrp,
                "OPV": self.opv,
                "VOSMS": self.vosms,
                "IPN": self.ipn,
                "ZP": self.zp,
                "CO": self.co,
                "CH": self.cn,
                "OSMS": self.osms
            }
        }


class Gph:
    def __init__(self, salary) -> None:
        self.salary = salary
        self.ipn = None
        self.opv = None
        self.osms = None
        self.zp = None

    def set_config(self, opv, ipn, osms) -> None:
        self.opv = (self.salary * opv) / 100
        self.ipn = ((self.salary - self.opv) * ipn) / 100
        self.osms = (self.salary * osms) / 100
        self.zp = (self.salary - self.opv - self.ipn - self.osms)

    def get_config_file(self, opv, ipn, osms) -> Dict:
        return {
            "VERSION": "GPH",
            "OPV_SET": opv,
            "IPN_SET": ipn,
            "OSMS_SET": osms,
            "SALARY_SET": self.salary
        }

    def get_config(self) -> Dict:
        return {
            "REPORT GPH": {
                "SALARY": self.salary,
                "IPN": self.ipn,
                "OPV": self.opv,
                "OSMS": self.osms,
                "ZP": self.zp
            }
        }


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def read(self):
        if (os.path.isfile("config_file.json")):
            with open("config_file.json", "r") as fs:
                string = fs.read()
                data = json.loads(string)
                if data["VERSION"] == "GPH":
                    salary = data["SALARY_SET"]
                    gph = Gph(salary)
                    gph.set_config(opv=data["OPV_SET"], ipn=data["IPN_SET"], osms=data["OSMS_SET"])
                    with open("report.json", "w") as f:
                        string = json.dumps(gph.get_config())
                        f.write(string)

                        print(gph.get_config())
                elif data["VERSION"] == "GENERAL":
                    salary = data["SALARY_SET"]
                    mrp = data["MRP_SET"]
                    general = General(salary, mrp)
                    general.set_config(opv=data["OPV_SET"], vosms=data["VOSMS_SET"], ipn=data["IPN_SET"],
                                       co=data["CO_SET"], cn=data["CH_SET"], osms=data["OSMS_SET"])
                    with open("report.json", "w") as f:
                        string = json.dumps(general.get_config())
                        f.write(string)

                        print(general.get_config())
        else:
            salary = float(input("ENTER THE GENERAL SALARY: "))
            choise = int(input("CHOISE GPH[0] OR GENERAL[1] EXIT[2]: "))
            if choise == 0:
                gph = Gph(salary)
                with open("config_file.json", "w") as fs:
                    opv = float(input("ENTER THE OPV %: "))
                    ipn = float(input("ENTER THE IPN %: "))
                    osms = float(input("ENTER THE OSMS %: "))
                    data = gph.get_config_file(opv=opv, ipn=ipn, osms=osms)
                    string = json.dumps(data)
                    fs.write(string)

                    print(data)
            elif choise == 1:
                mrp = float(input("ENTER THE MRP: "))
                general = General(salary, mrp)
                with open("config_file.json", "w") as fs:
                    opv = float(input("ENTER THE OPV %: "))
                    ipn = float(input("ENTER THE IPN %: "))
                    osms = float(input("ENTER THE OSMS %: "))
                    vosms = float(input("ENTER THE VOSMS %: "))
                    co = float(input("ENTER THE CO %: "))
                    cn = float(input("ENTER THE CN %: "))
                    data = general.get_config_file(opv=opv, osms=osms, ipn=ipn, vosms=vosms, co=co, cn=cn)
                    string = json.dumps(data)
                    fs.write(string)

                    print(data)
            elif choise == 2:
                print("EXIT...")


if __name__ == "__main__":
    s1 = Singleton()
    s1.read()
