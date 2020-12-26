import pandas as pd
from app import app, db
from app.models import Listing


raw_data = pd.read_csv('77005data.csv') 

for i, row in raw_data.iterrows():
    print(i)
    listing = Listing(address=row['address'], price=row['price'] ,description=row['description'], zipcode=row['zipcode'], year=row['yearbuilt'], building_sqft=row['buildingsqft'])
    db.session.add(listing)
    try:
        db.session.commit()
    except:
        db.session.rollback()



