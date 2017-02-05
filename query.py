"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

#Returns a base query object at a specified memory address
#<flask_sqlalchemy.BaseQuery at 0x7f6c6222f410>
#If we added .all() we would recieve a list of meaningful results.
#[<Brand id=for name=Ford founded=1903 headquarters=Dearborn, MI discontinued=None>]
#If we added .one(), we would know for certain that only one entry in the
#table matched that result, if there were 0 or 2 matching results,
#we would recieve an error.

# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

#An association table is a one to many table that has no meaningful fields.
#It is used to link tables together to avoid a many to many relationship.
#Many to many relationships are a lie, association tables are the "hidden" linkers
#in a many to many relationship.
# -------------------------------------------------------------------
print "=" * 100
print "=" * 100
print "Part 3: SQLAlchemy Queries"

print "\nQuestion 1" + "-" * 100
# Get the brand with the ``id`` of "ram."
q1 = db.session.query(Brand.name).filter_by(brand_id='ram').one()
print q1


print "\nQuestion 2" + "-" * 100
# Get all models with the name "Corvette" and the brand_id "che."
q2 = db.session.query(Model).filter_by(brand_id='che', name='Corvette').all()
print q2


print "\nQuestion 3" + "-" * 100
# Get all models that are older than 1960.
q3 = db.session.query(Model.name).filter(Model.year < 1960).all()
print q3
print "-" * 75

print "\nQuestion 4" + "-" * 100
# Get all brands that were founded after 1920.
q4 = db.session.query(Brand.name).filter(Brand.founded > 1920).all()
print q4

print "\nQuestion 5" + "-" * 100
# Get all models with names that begin with "Cor."
q5 = db.session.query(Model.name).join(Brand).filter(Model.name.like('%Cor%')).all()
print q5

print "\nQuestion 6" + "-" * 100
# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = db.session.query(Brand.name).filter_by(founded=1903, discontinued=None).all()
print q6

print "\nQuestion 7" + "-" * 100
# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
#q7 = Brand.query.filter(db.or_(Brand.discontinued = None, Brand.founded < 1950)).all()
q7 = db.session.query(Brand).filter(db.or_(Brand.discontinued == None, Brand.founded < 1950)).all()
print q7

print "\nQuestion 8" + "-" * 100
# Get any model whose brand_id is not "for."
q8 = db.session.query(Model.name).filter(db.not_(Model.brand_id == 'for')).all()
print q8
# -------------------------------------------------------------------
print "=" * 100
print "=" * 100
print "Part 4: Write Functions\n"


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query.

    >>> get_model_info(1960)
    [(u'Corvette', u'Chevrolet', u'Detroit, Michigan'), (u'Corvair', u'Chevrolet', u'Detroit, Michigan'), (u'Rockette', u'Fairthorpe', u'Chalfont St Peter, Buckinghamshire')]

    >>> get_model_info(1909)
    [(u'Model T', u'Ford', u'Dearborn, MI')]
    """

    year_info = db.session.query(Model.name, Brand.name, Brand.headquarters).join(Brand).filter(Model.year == year).all()
    print year_info


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query.

    >>> get_brands_summary()
    [(u'Austin', u'Mini', 1959), (u'Austin', u'Mini Cooper', 1961), (u'Austin', u'Mini', 1963), (u'Austin', u'Mini Cooper S', 1963), (u'Austin', u'Mini Cooper', 1964), (u'BMW', u'600', 1957), (u'BMW', u'600', 1958), (u'BMW', u'600', 1959), (u'Buick', u'Special', 1962), (u'Cadillac', u'Fleetwood', 1954), (u'Chevrolet', u'Corvette', 1953), (u'Chevrolet', u'Corvette', 1954), (u'Chevrolet', u'Corvette', 1955), (u'Chevrolet', u'Corvette', 1956), (u'Chevrolet', u'Corvette', 1957), (u'Chevrolet', u'Corvette', 1958), (u'Chevrolet', u'Corvette', 1959), (u'Chevrolet', u'Corvair', 1960), (u'Chevrolet', u'Corvette', 1960), (u'Chevrolet', u'Corvette', 1961), (u'Chevrolet', u'Corvette', 1962), (u'Chevrolet', u'Corvair 500', 1963), (u'Chevrolet', u'Corvette', 1963), (u'Chevrolet', u'Corvette', 1964), (u'Chrysler', u'Imperial', 1926), (u'Citroen', u'2CV', 1948), (u'Fairthorpe', u'Rockette', 1960), (u'Ford', u'Model T', 1909), (u'Ford', u'Thunderbird', 1955), (u'Ford', u'Thunderbird', 1958), (u'Ford', u'E-Series', 1963), (u'Ford', u'Galaxie', 1964), (u'Ford', u'Mustang', 1964), (u'Hillman', u'Minx Magnificent', 1950), (u'Plymouth', u'Fury', 1964), (u'Pontiac', u'Tempest', 1961), (u'Pontiac', u'Grand Prix', 1962), (u'Pontiac', u'Grand Prix', 1963), (u'Pontiac', u'Bonneville', 1964), (u'Pontiac', u'Grand Prix', 1964), (u'Pontiac', u'LeMans', 1964), (u'Rambler', u'Classic', 1963), (u'Studebaker', u'Avanti', 1961), (u'Studebaker', u'Avanti', 1962), (u'Studebaker', u'Avanti', 1963), (u'Studebaker', u'Avanti', 1964)]

    """

    ordered_brands = db.session.query(Brand.name, Model.name, Model.year).join(Model).group_by(Brand.name, Model.name, Model.year).order_by(Brand.name, Model.year).all()

    print ordered_brands


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string.

    >>> search_brands_by_name("Ford")
    [<Brand id=for name=Ford founded=1903 headquarters=Dearborn, MI discontinued=None>]

    >>> search_brands_by_name("Te")
    [<Brand id=tes name=Tesla founded=2003 headquarters=Palo Alto, CA discontinued=None>]

    >>> search_brands_by_name("x")
    []
    """

    search = db.session.query(Brand).filter(Brand.name.contains(mystr)).all()

    return search


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive).

    >>> get_models_between(1960, 1962)
    [<Model id=19 year=1960 brand id=che name=Corvair>, <Model id=20 year=1960 brand id=che name=Corvette>, <Model id=21 year=1960 brand id=fai name=Rockette>, <Model id=22 year=1961 brand id=aus name=Mini Cooper>, <Model id=23 year=1961 brand id=stu name=Avanti>, <Model id=24 year=1961 brand id=pon name=Tempest>, <Model id=25 year=1961 brand id=che name=Corvette>]
    """

    start_year = start_year - 1
    between = db.session.query(Model).filter(Model.year > start_year, Model.year < end_year).all()

    return between

##############################################################################
if __name__ == "__main__":
    import doctest

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED. GOOD WORK!"
    print
