"""
Calendar Converter
Converts dates between Gregorian, Hijri Lunar, and Hijri Solar calendars
"""

from datetime import datetime
try:
    from hijri_converter import convert
    HIJRI_LUNAR_AVAILABLE = True
except ImportError:
    HIJRI_LUNAR_AVAILABLE = False
    print("Warning: hijri-converter library not found. Install it with: pip install hijri-converter")

try:
    import jdatetime
    HIJRI_SOLAR_AVAILABLE = True
except ImportError:
    HIJRI_SOLAR_AVAILABLE = False
    print("Warning: jdatetime library not found. Install it with: pip install jdatetime")


def gregorian_to_hijri_lunar(year, month, day):
    """Convert Gregorian date to Hijri Lunar date"""
    if not HIJRI_LUNAR_AVAILABLE:
        return None, "Library not available"
    try:
        hijri_date = convert.Gregorian(year, month, day).to_hijri()
        return (hijri_date.year, hijri_date.month, hijri_date.day), None
    except Exception as e:
        return None, str(e)


def hijri_lunar_to_gregorian(year, month, day):
    """Convert Hijri Lunar date to Gregorian date"""
    if not HIJRI_LUNAR_AVAILABLE:
        return None, "Library not available"
    try:
        gregorian_date = convert.Hijri(year, month, day).to_gregorian()
        return (gregorian_date.year, gregorian_date.month, gregorian_date.day), None
    except Exception as e:
        return None, str(e)


def gregorian_to_hijri_solar(year, month, day):
    """Convert Gregorian date to Hijri Solar (Persian) date"""
    if not HIJRI_SOLAR_AVAILABLE:
        return None, "Library not available"
    try:
        hijri_solar = jdatetime.date.fromgregorian(year=year, month=month, day=day)
        return (hijri_solar.year, hijri_solar.month, hijri_solar.day), None
    except Exception as e:
        return None, str(e)


def hijri_solar_to_gregorian(year, month, day):
    """Convert Hijri Solar (Persian) date to Gregorian date"""
    if not HIJRI_SOLAR_AVAILABLE:
        return None, "Library not available"
    try:
        gregorian = jdatetime.date(year, month, day).togregorian()
        return (gregorian.year, gregorian.month, gregorian.day), None
    except Exception as e:
        return None, str(e)


def convert_all_calendars(input_type, year, month, day):
    """Convert a date from one calendar to the other two"""
    results = {}
    errors = {}
    
    if input_type == "gregorian":
        # Convert to Hijri Lunar
        hijri_lunar, error = gregorian_to_hijri_lunar(year, month, day)
        if error:
            errors["hijri_lunar"] = error
        else:
            results["hijri_lunar"] = hijri_lunar
        
        # Convert to Hijri Solar
        hijri_solar, error = gregorian_to_hijri_solar(year, month, day)
        if error:
            errors["hijri_solar"] = error
        else:
            results["hijri_solar"] = hijri_solar
        
        results["gregorian"] = (year, month, day)
    
    elif input_type == "hijri_lunar":
        # Convert to Gregorian first
        gregorian, error = hijri_lunar_to_gregorian(year, month, day)
        if error:
            errors["gregorian"] = error
            errors["hijri_solar"] = "Cannot convert without Gregorian date"
        else:
            results["gregorian"] = gregorian
            # Convert Gregorian to Hijri Solar
            hijri_solar, error = gregorian_to_hijri_solar(
                gregorian[0], gregorian[1], gregorian[2]
            )
            if error:
                errors["hijri_solar"] = error
            else:
                results["hijri_solar"] = hijri_solar
        
        results["hijri_lunar"] = (year, month, day)
    
    elif input_type == "hijri_solar":
        # Convert to Gregorian first
        gregorian, error = hijri_solar_to_gregorian(year, month, day)
        if error:
            errors["gregorian"] = error
            errors["hijri_lunar"] = "Cannot convert without Gregorian date"
        else:
            results["gregorian"] = gregorian
            # Convert Gregorian to Hijri Lunar
            hijri_lunar, error = gregorian_to_hijri_lunar(
                gregorian[0], gregorian[1], gregorian[2]
            )
            if error:
                errors["hijri_lunar"] = error
            else:
                results["hijri_lunar"] = hijri_lunar
        
        results["hijri_solar"] = (year, month, day)
    
    return results, errors


def validate_date(year, month, day, calendar_type):
    """Validate date based on calendar type"""
    if calendar_type == "gregorian":
        try:
            datetime(year, month, day)
            return True, None
        except ValueError as e:
            return False, str(e)
    elif calendar_type == "hijri_lunar":
        # Basic validation for Hijri Lunar
        if year < 1 or year > 1500:
            return False, "Hijri Lunar year should be between 1 and 1500"
        if month < 1 or month > 12:
            return False, "Month should be between 1 and 12"
        if day < 1 or day > 30:
            return False, "Day should be between 1 and 30"
        return True, None
    elif calendar_type == "hijri_solar":
        # Basic validation for Hijri Solar
        if year < 1 or year > 1500:
            return False, "Hijri Solar year should be between 1 and 1500"
        if month < 1 or month > 12:
            return False, "Month should be between 1 and 12"
        if day < 1 or day > 31:
            return False, "Day should be between 1 and 31"
        return True, None
    return False, "Unknown calendar type"


def get_month_name(month, calendar_type):
    """Get month name based on calendar type"""
    if calendar_type == "gregorian":
        months = ["", "January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
    elif calendar_type == "hijri_lunar":
        months = ["", "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani",
                 "Jumada al-awwal", "Jumada al-thani", "Rajab", "Sha'ban",
                 "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"]
    elif calendar_type == "hijri_solar":
        months = ["", "Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad",
                 "Shahrivar", "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"]
    else:
        return str(month)
    
    if 1 <= month <= 12:
        return months[month]
    return str(month)


def format_date(year, month, day, calendar_type):
    """Format date for display"""
    month_name = get_month_name(month, calendar_type)
    return f"{day} {month_name} {year}"


def main():
    print("=" * 70)
    print("Calendar Converter - Gregorian, Hijri Lunar, and Hijri Solar")
    print("=" * 70)
    print()
    
    # Check library availability
    if not HIJRI_LUNAR_AVAILABLE or not HIJRI_SOLAR_AVAILABLE:
        print("\n⚠️  IMPORTANT: Some required libraries are missing!")
        print("Please install them using:")
        if not HIJRI_LUNAR_AVAILABLE:
            print("  pip install hijri-converter")
        if not HIJRI_SOLAR_AVAILABLE:
            print("  pip install jdatetime")
        print()
    
    while True:
        print("\n" + "-" * 70)
        print("Select the calendar type of your input date:")
        print("1. Gregorian Calendar")
        print("2. Hijri Lunar Calendar (Islamic Calendar)")
        print("3. Hijri Solar Calendar (Persian/Iranian Calendar)")
        print("4. Exit")
        print("-" * 70)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "4":
            print("\nThank you for using Calendar Converter!")
            break
        
        calendar_types = {
            "1": "gregorian",
            "2": "hijri_lunar",
            "3": "hijri_solar"
        }
        
        if choice not in calendar_types:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")
            continue
        
        calendar_type = calendar_types[choice]
        calendar_name = {
            "gregorian": "Gregorian",
            "hijri_lunar": "Hijri Lunar",
            "hijri_solar": "Hijri Solar"
        }[calendar_type]
        
        print(f"\nEnter date in {calendar_name} Calendar:")
        print("(Format: Year Month Day, e.g., 2024 3 15)")
        
        try:
            date_input = input("Date: ").strip().split()
            if len(date_input) != 3:
                print("Error: Please enter date in format: Year Month Day")
                continue
            
            year = int(date_input[0])
            month = int(date_input[1])
            day = int(date_input[2])
            
            # Validate date
            is_valid, error_msg = validate_date(year, month, day, calendar_type)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Convert dates
            results, errors = convert_all_calendars(calendar_type, year, month, day)
            
            # Display results
            print("\n" + "=" * 70)
            print("CONVERSION RESULTS")
            print("=" * 70)
            
            # Display input date
            input_formatted = format_date(year, month, day, calendar_type)
            print(f"\n📅 Input Date ({calendar_name}): {input_formatted}")
            print(f"   ({year}/{month:02d}/{day:02d})")
            
            # Display converted dates
            print("\n📆 Converted Dates:")
            print("-" * 70)
            
            if "gregorian" in results:
                greg = results["gregorian"]
                formatted = format_date(greg[0], greg[1], greg[2], "gregorian")
                print(f"   Gregorian:     {formatted}")
                print(f"                  ({greg[0]}/{greg[1]:02d}/{greg[2]:02d})")
            elif "gregorian" in errors:
                print(f"   Gregorian:     ❌ Error: {errors['gregorian']}")
            
            if "hijri_lunar" in results:
                hijri_l = results["hijri_lunar"]
                formatted = format_date(hijri_l[0], hijri_l[1], hijri_l[2], "hijri_lunar")
                print(f"   Hijri Lunar:   {formatted}")
                print(f"                  ({hijri_l[0]}/{hijri_l[1]:02d}/{hijri_l[2]:02d})")
            elif "hijri_lunar" in errors:
                print(f"   Hijri Lunar:   ❌ Error: {errors['hijri_lunar']}")
            
            if "hijri_solar" in results:
                hijri_s = results["hijri_solar"]
                formatted = format_date(hijri_s[0], hijri_s[1], hijri_s[2], "hijri_solar")
                print(f"   Hijri Solar:   {formatted}")
                print(f"                  ({hijri_s[0]}/{hijri_s[1]:02d}/{hijri_s[2]:02d})")
            elif "hijri_solar" in errors:
                print(f"   Hijri Solar:   ❌ Error: {errors['hijri_solar']}")
            
            print("=" * 70)
            
        except ValueError:
            print("Error: Please enter valid numbers for year, month, and day!")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Ask if user wants to continue
        continue_choice = input("\nDo you want to convert another date? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\nThank you for using Calendar Converter!")
            break


if __name__ == "__main__":
    main()

