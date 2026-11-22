import secrets ,string ,datetime
def generate_password(length):
    if length < 4:
        return None
    alphabet = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*()"
    )

    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()")
    ]

    remaining_length = length - 4

    for _ in range(remaining_length):
        password.append(secrets.choice(alphabet))

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def check_password_strength(password):
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in "!@#$%^&*()" for c in password):
        score += 1

    if score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        "length": len(password),
        "strength": strength,
        "score": f"{score}/6",
        "password": password
    }


def save_reminder(account, period_months):
    today = datetime.date.today()
    due_date = today + datetime.timedelta(
        days=period_months * 30
    )

    try:
        with open("reminders.txt", "a", encoding="utf-8") as file:
            file.write(f"Account: {account}\n")
            file.write(f"Start Date: {today.strftime('%Y-%m-%d')}\n")
            file.write(f"Reminder Period (months): {period_months}\n")
            file.write(f"Due Date: {due_date.strftime('%Y-%m-%d')}\n")
            file.write("\n")

        print("Reminder saved successfully.")

    except OSError as error:
        print(f"Error saving reminder: {error}")


def load_reminders():
    reminders = []

    try:
        with open("reminders.txt", "r", encoding="utf-8") as file:
            content = file.read()

        records = content.strip().split("\n\n")

        for record in records:
            if not record.strip():
                continue

            reminder = {}

            for line in record.splitlines():
                if ": " in line:
                    key, value = line.split(": ", 1)
                    reminder[key] = value

            if (
                "Account" in reminder
                and "Start Date" in reminder
                and "Due Date" in reminder
            ):
                reminders.append(reminder)

    except FileNotFoundError:
        return []

    except OSError as error:
        print(f"Error reading reminders: {error}")
        return []

    return reminders


def main():
    print("=" * 40)
    print("       PASSWORD SECURITY TOOL")
    print("=" * 40)

    while True:
        try:
            length = int(input("[1] Enter password length: "))

            if length < 4:
                print("Password length must be at least 4.")
                continue

            break

        except ValueError:
            print("Please enter a valid integer.")

    generated_password = generate_password(length)

    if generated_password is None:
        print("Error generating password.")
    else:
        print(f"[2] Generated Password: {generated_password}")

    check_input = input(
        "[3] Enter a password to check "
        "(or press Enter for generated): "
    )

    if not check_input.strip():
        password_to_check = generated_password
    else:
        password_to_check = check_input

    strength_result = check_password_strength(password_to_check)

    print("\nPassword Analysis")
    print("-" * 30)
    print(f"Password length: {strength_result['length']}")
    print(f"Strength: {strength_result['strength']}")
    print(f"Score: {strength_result['score']}")

    account_name = input(
        "\n[4] Enter account name for reminder: "
    ).strip()

    while not account_name:
        print("Account name cannot be empty.")
        account_name = input("Enter account name: ").strip()

    while True:
        try:
            period_months = int(
                input("Enter reminder period (3, 6, 9, or 12 months): ")
            )

            if period_months not in [3, 6, 9, 12]:
                print("Invalid period. Choose 3, 6, 9, or 12.")
                continue

            break

        except ValueError:
            print("Please enter a valid integer.")

    save_reminder(account_name, period_months)

    print("\n[5] Password Reminders")
    print("=" * 40)

    reminders = load_reminders()

    if not reminders:
        print("No reminders found.")
    else:
        today = datetime.date.today()

        for reminder in reminders:
            try:
                due_date = datetime.datetime.strptime(
                    reminder["Due Date"],
                    "%Y-%m-%d"
                ).date()

                days_remaining = (due_date - today).days

                if days_remaining < 0:
                    status = f"OVERDUE by {abs(days_remaining)} days"
                elif days_remaining == 0:
                    status = "DUE TODAY"
                else:
                    status = f"{days_remaining} days remaining"

                print(f"\nAccount: {reminder['Account']}")
                print(f"Start Date: {reminder['Start Date']}")
                print(f"Due Date: {reminder['Due Date']}")
                print(f"Status: {status}")

            except (KeyError, ValueError):
                print("Invalid reminder record.")

    print("\n" + "=" * 40)
    print("       PROGRAM COMPLETED")
    print("=" * 40)


if __name__ == "__main__":
    main()
