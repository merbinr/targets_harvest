from src.hackerone_helper import HackeroneHelper
from src.db_helper import DBHelper





def main():

    db_helper = DBHelper("targets.db")
    db_helper.initialize_db()

    hackerone_helper = HackeroneHelper(db_helper=db_helper)
    hackerone_programs = hackerone_helper.get_programes_list()





if __name__ == "__main__":
    main()
