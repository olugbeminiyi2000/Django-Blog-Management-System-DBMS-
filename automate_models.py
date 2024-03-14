if __name__ == "__main__":
    import sys
    from qwik_aids.models import Country, Language

    # create country
    country = Country(country_name=sys.argv[1], continent=sys.argv[2])
    country.save()

    # use a for loop to check the number of languages and language_code
    length = len(sys.argv[1:])
    curr_pos = 3
    while curr_pos < length:
        language = Language(langauge=sys.argv[curr_pos], language_code=sys.argv[curr_pos + 1], country=country)
        language.save()
        curr_pos += 2
    # Corrected variable name
    country1 = Country.objects.filter(country_name=sys.argv[1]).first()

    # Accessing languages for the corrected country variable
    languages = country1.languages.all()
    print(languages)
