from lunchbot.geocoding import geocode, is_within_km
import time


def main():
    fi = geocode("Fakulta Informatiky, Botanická, Brno")
    time.sleep(1.5)
    hrncir = geocode("Hrncirska, Brno")
    time.sleep(1.5)
    hlavak = geocode("Hlavni nadrazi, Brno")

    print(f'Hrncirska {is_within_km(1.0, fi[0], fi[1], hrncir[0], hrncir[1])}')
    print(f'Hlavak {is_within_km(1.0, fi[0], fi[1], hlavak[0], hlavak[1])}')


if __name__ == "__main__":
    main()
