def input_numbers() -> object:
    # This function accepts numbers from the user and stores them in a file
    # Create a file object in write mode.
    # The as keyword is used to create an alias.
    # In the example we create an alias f
    with open("numbers.txt", "w") as f:
        # Prompt the user for a number.
        number = input("Enter any number here: ")

        # Check if the number is an integer.
        try:
            number = int(number)
        except ValueError:
            # If the number is not an integer, display an error message and prompt for input again.
            print("Invalid input. Please enter an only an integer.")
            return

        # Write the number to the file.
        f.write(str(number) + "\n")

        # Ask if the user wants to continue.
        continue_input = input("Do you want to continue? (Yes/No): ")

        # If the user inputs 'Yes', repeat steps 1 to 3.
        if continue_input == "Yes":
            input_numbers()


if __name__ == "__main__":
    input_numbers()
