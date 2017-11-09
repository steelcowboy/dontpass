import settings

from get_info import get_info 

def main():
    classes = get_info(settings.classes)

    for cls in classes:
        print("\33[31m{}\33[0m".format(cls["title"]))
        for section in cls["sections"]:
            print(section)
        print()

if __name__ == "__main__":
    main()

