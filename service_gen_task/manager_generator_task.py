import csv
def run(choice, runfile):
    if choice == "1":
        with open(runfile, "r", encoding="utf-8") as rnf:
            exec(rnf.read())
    elif choice == "2":
        with open(runfile, "r", encoding="utf-8") as rnf:
            exec(rnf.read())
    elif choice == "3":
        with open(runfile, "r", encoding="utf-8") as rnf:
            exec(rnf.read())
    else:
        print("Некорректный выбор. Пожалуйста, выберите 1, 2 или 3.")

if __name__ == "__main__":
    choice = input("Введите номер выбранной опции 1:одс+ , 2:ддс, 3:дм : ")
    if choice in ["1", "2", "3"]:
        run(choice, "service_gen_task/generator_tasks/service_create_tasks.py" if choice == "1" else
                  "service_gen_task/generator_tasks/service_create_tasks_dds.py" if choice == "2" else
                  "service_gen_task/generator_tasks/service_create_tasks_dm.py")
    else:
        print("Некорректный выбор. Пожалуйста, выберите 1, 2 или 3.")
 