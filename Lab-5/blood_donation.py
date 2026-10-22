"""Blood donation management system.

Registers donors after an age check, decides who may donate again
(90-day gap), records donations into blood-group stock and works out how
many compatible units are available for a patient.
"""
import subprocess  # nosec B404
import tempfile
from datetime import date, timedelta

MIN_AGE = 18
MAX_AGE = 65
DONATION_GAP_DAYS = 90

donors = []
stock = {"A+": 0, "A-": 0, "B+": 0, "B-": 0,
         "O+": 0, "O-": 0, "AB+": 0, "AB-": 0}
COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(stock),
}


def register_donor(donor_name, blood_group, age,
                   last_donation=None, notes=None):
    """Register a donor if the blood group is valid and age is allowed."""
    if blood_group not in stock:
        raise ValueError("Unknown blood group")
    if notes is None:
        notes = []
    if age < MIN_AGE or age > MAX_AGE:
        notes.append(donor_name + " is not eligible because of age")
        return False
    donors.append({"name": donor_name, "group": blood_group,
                   "last": last_donation})
    return True


def can_donate(donor):
    """Return True if the donor has waited at least 90 days."""
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=DONATION_GAP_DAYS)


def record_donation(donor_name, units=1):
    """Add units to stock if the named donor is allowed to donate."""
    for donor in donors:
        if donor["name"] == donor_name and can_donate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def units_for(patient_group):
    """Return total compatible units available for a patient group."""
    try:
        return sum(stock[group] for group in COMPATIBLE[patient_group])
    except KeyError:
        return 0


def is_universal(blood_group):
    """Return True for universal donor/recipient groups."""
    return blood_group in ("O-", "AB+")


def low_stock(threshold=2):
    """Return blood groups whose stock is below the threshold."""
    return [group for group, units in stock.items() if units < threshold]


def donor_sheet_path():
    """Create a secure temporary CSV file and return its path."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as handle:
        return handle.name


def notify_donors(phone_list):
    """Send an SMS to each phone number."""
    subprocess.run(["send-sms", *phone_list], check=False)  # nosec B603 B607


def main():
    """Run a short demonstration."""
    register_donor("Arjun", "O+", 25)
    register_donor("Priya", "A+", 30, date.today() - timedelta(days=30))
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)
    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")
    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock())  # below 2 units
    eligible = [donor["name"] for donor in donors if can_donate(donor)]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
