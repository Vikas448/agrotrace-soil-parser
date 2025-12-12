#!/usr/bin/env python3
# soil_parser.py
import csv, json, os
from statistics import mean, median
INPUT_CSV = "sample_data/soil.csv"
OUTPUT_DIR = "output"
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "soil_report.json")
def parse_csv(path):
    rows=[]
    with open(path,newline='') as f:
        reader=csv.DictReader(f)
        for r in reader:
            r2={}
            for k,v in r.items():
                v=v.strip()
                try:
                    r2[k]=None if v=="" else float(v)
                except:
                    r2[k]=v
            rows.append(r2)
    return rows
def analyze(rows):
    numeric_cols=["ph","nitrogen","phosphorus","potassium"]
    stats={}
    for col in numeric_cols:
        vals=[r[col] for r in rows if isinstance(r.get(col),(int,float))]
        stats[col]=None
        if vals:
            stats[col]={"count":len(vals),"mean":round(mean(vals),3),"median":round(median(vals),3),"min":round(min(vals),3),"max":round(max(vals),3)}
    for r in rows:
        ph=r.get("ph")
        r["ph_ok"]= (isinstance(ph,(int,float)) and 6.0<=ph<=7.5)
    return {"summary":stats,"samples":rows}
def ensure_output_dir(): os.makedirs(OUTPUT_DIR,exist_ok=True)
def main():
    if not os.path.exists(INPUT_CSV):
        print(f"ERROR: input CSV not found at {INPUT_CSV}")
        return 2
    rows=parse_csv(INPUT_CSV)
    report=analyze(rows)
    ensure_output_dir()
    with open(OUTPUT_JSON,"w") as f: json.dump(report,f,indent=2)
    print(f"Wrote {OUTPUT_JSON}")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
