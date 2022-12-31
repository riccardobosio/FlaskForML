## HOW TO MANAGE THE DB


### TO CREATE IT

First define the FLASK_APP variable:
```console
export FLASK_APP=your_path_to_app
```

Then use flask shell:
```console
flask shell
```

From the just opened shell run:
```console
db.create_all()
```

### TO POPULATE IT MANUALLY

Always from flask shell, first create a new object, for example:
```console
user_1 = User(email='riccardobosio18@gmail.com', password='password')
```

Then add it among the changes:
```console
db.session.add(user_1)
```

Finally, commit the changes (you can add multiple changes before committing):
```console
db.session.commit()
```

You will see the new record only after committing.

### TO DELETE EVERYTHING

From flask shell run:
```console
db.drop_all()
```