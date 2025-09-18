def main():
    a = float(input("Enter the number of cars: "))
    b: float = a * 573.52
    print("The total cost will be: $","%.2f" % b,sep = '')

if __name__ == "__main__":
    main()