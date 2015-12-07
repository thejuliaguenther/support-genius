from faker import Factory
fake = Factory.create()

submits = []
resolves = []
first_touches = []

for i in range(300):
    submit = fake.date_time_this_month(before_now=True, after_now=False)
    submits.append(submit)
    
    resolved = fake.date_time_between_dates(datetime_start= submit, datetime_end=None)
    resolves.append(resolved)
    
    first_touch = fake.date_time_between_dates(datetime_start=submit, datetime_end=resolved)
    first_touches.append(first_touch)


for j in range(len(submits)):
    print submits[j]

print "##############"

for x in range(len(resolves)):
    print resolves[x]

print "##############"

for y in range(len(first_touches)):
    print first_touches[y]
