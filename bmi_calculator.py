def calculate_bmi(weight, height):
    """Calculate BMI (Body Mass Index)"""
    bmi = weight / (height ** 2)
    return bmi

def get_bmi_category(bmi):
    """Determine BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_weight_difference(weight, height, bmi):
    """Calculate how many kilograms the person is overweight or underweight"""
    if bmi < 18.5:
        # Calculate target weight for normal BMI (18.5)
        target_weight = 18.5 * (height ** 2)
        difference = target_weight - weight
        return difference, "underweight"
    elif bmi >= 25:
        # Calculate target weight for upper normal BMI (25)
        target_weight = 25 * (height ** 2)
        difference = weight - target_weight
        return difference, "overweight"
    else:
        return 0, "normal"

def main():
    print("=" * 50)
    print("BMI Calculator and Health Assessment")
    print("=" * 50)
    print()
    
    try:
        # Get user input
        age = float(input("Enter your age: "))
        weight = float(input("Enter your weight in kilograms (kg): "))
        height_input = input("Enter your height (e.g., 1.75 for meters or 175 for cm): ")
        
        # Convert height to meters
        height = float(height_input)
        if height > 3:  # Likely entered in cm
            height = height / 100
            print(f"Converted height: {height:.2f} meters")
        
        # Validate inputs
        if weight <= 0 or height <= 0 or age <= 0:
            print("Error: Weight, height, and age must be positive numbers!")
            return
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)
        weight_diff, status = calculate_weight_difference(weight, height, bmi)
        
        # Display results
        print()
        print("=" * 50)
        print("RESULTS")
        print("=" * 50)
        print(f"Age: {age:.0f} years")
        print(f"Weight: {weight:.2f} kg")
        print(f"Height: {height:.2f} meters")
        print(f"BMI: {bmi:.2f}")
        print(f"Condition: {category}")
        print()
        
        if status == "underweight":
            print(f"You are {weight_diff:.2f} kg underweight.")
            print("You need to gain weight to reach a healthy BMI range.")
        elif status == "overweight":
            print(f"You are {weight_diff:.2f} kg overweight.")
            print("You need to lose weight to reach a healthy BMI range.")
        else:
            print("Your weight is within the normal range. Keep maintaining it!")
        
        print()
        print("BMI Categories:")
        print("- Underweight: BMI < 18.5")
        print("- Normal weight: 18.5 ≤ BMI < 25")
        print("- Overweight: 25 ≤ BMI < 30")
        print("- Obese: BMI ≥ 30")
        
    except ValueError:
        print("Error: Please enter valid numbers!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

