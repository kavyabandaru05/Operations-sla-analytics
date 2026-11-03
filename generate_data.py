import random, csv
from datetime import datetime, timedelta
random.seed(7)

teams = {"Billing":0.22,"Technical Support":0.38,"Account Access":0.2,"Logistics":0.12,"General Enquiry":0.08}
# team -> root causes (weighted)
causes = {
 "Billing":["Incorrect invoice","Payment failure","Refund delay","Duplicate charge"],
 "Technical Support":["Software bug","Integration error","Performance issue","Configuration issue","Outage"],
 "Account Access":["Password reset","Locked account","MFA issue","Permissions error"],
 "Logistics":["Delivery delay","Damaged item","Wrong item","Tracking error"],
 "General Enquiry":["Product question","Policy question","Feedback"]}
priorities = {"Critical":(0.06,4),"High":(0.20,8),"Medium":(0.46,24),"Low":(0.28,72)}  # weight, SLA hours
channels = ["Email","Phone","Chat","Web Form"]
tiers = ["Standard","Premium","Enterprise"]
agents = {t:[f"{t[:3].upper()}-A{i:02d}" for i in range(1,7)] for t in teams}
# base resolution multipliers relative to SLA target (median ratio); creates real patterns
team_factor = {"Billing":1.15,"Technical Support":1.0,"Account Access":0.55,"Logistics":1.25,"General Enquiry":0.5}
snapshot = datetime(2025,12,31,23,59)
start = datetime(2025,7,1)
rows=[]; n=0
day=start
while day <= datetime(2025,12,31):
    base = 38
    if day.weekday()==0: base*=1.35
    if day.weekday()>=5: base*=0.45
    if day.month==10 and 14<=day.day<=20: base*=1.8   # outage spike week
    if day.month==12: base*=1.2                        # holiday peak
    for _ in range(max(0,int(random.gauss(base,6)))):
        n+=1
        team = random.choices(list(teams), weights=list(teams.values()))[0]
        pr = random.choices(list(priorities), weights=[v[0] for v in priorities.values()])[0]
        sla = priorities[pr][1]
        cause = random.choice(causes[team])
        if cause=="Outage": pr = random.choice(["Critical","High"]); sla=priorities[pr][1]
        created = day + timedelta(minutes=random.randint(0,1439))
        first_resp = created + timedelta(minutes=int(random.expovariate(1/ (sla*60*0.12))) + 3)
        ratio = random.lognormvariate(0, 0.55) * team_factor[team] * 0.85
        if day.month==10 and 14<=day.day<=20 and team=="Technical Support": ratio*=1.8
        if day.month==12: ratio*=1.15
        res_hours = sla*ratio
        resolved = created + timedelta(hours=res_hours)
        status = "Closed" if random.random()<0.6 else "Resolved"
        if resolved > snapshot or random.random()<0.015:
            status = random.choice(["Open","In Progress"]); resolved=None
        reopened = 1 if (resolved and random.random()<0.06) else 0
        csat = None
        if resolved and random.random()<0.55:
            csat = max(1,min(5, round(random.gauss(4.2 - 0.9*(ratio>1) - 0.6*reopened, 0.9))))
        rows.append([f"TKT{100000+n}", created.strftime("%Y-%m-%d %H:%M"), first_resp.strftime("%Y-%m-%d %H:%M"),
                     resolved.strftime("%Y-%m-%d %H:%M") if resolved else "", team, random.choice(agents[team]),
                     pr, sla, cause, random.choice(channels), random.choices(tiers,weights=[70,22,8])[0],
                     status, reopened, csat if csat else ""])
    day += timedelta(days=1)

# deliberate data-quality issues (all documented in the validation log)
rows.append(rows[25][:])                                   # exact duplicate
rows[60][3] = "2025-01-01 00:00"                           # resolved before created
rows[90][6] = ""                                           # missing priority
rows[140][6] = rows[140][6].lower() + " "                # casing/whitespace
rows[180][4] = ""                                          # missing team
rows[220][3] = ""; rows[220][11] = "Closed"                # closed but no resolved date
rows[260][13] = 9                                          # CSAT out of 1-5 range
rows[300][3] = (datetime.strptime(rows[300][1],"%Y-%m-%d %H:%M")+timedelta(hours=6000)).strftime("%Y-%m-%d %H:%M")  # extreme outlier
rows[340][2] = "2025-01-01 00:00"                          # first response before created

hdr=["ticket_id","created_at","first_response_at","resolved_at","team","agent_id","priority","sla_target_hours",
     "root_cause","channel","customer_tier","status","reopened","csat_score"]
with open("data/tickets_raw.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(hdr); w.writerows(rows)
print(len(rows),"rows")
