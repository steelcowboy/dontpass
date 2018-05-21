from get_info import parse_pass
from print_classes import print_class

def main(html):
    full_outp = ""

    classes = parse_pass(html) 
    quarter = "F18" 

    full_outp += f"\033[31m{quarter}\033[0m\n\n"
    for cls in classes:
        full_outp += print_class(cls)

    return full_outp

if __name__ == "__main__":
    with open("pass.html", "r") as htmlfile:
        print(main(htmlfile.read()))

