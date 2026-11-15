import json,zipfile,glob
f="/home/ubuntu/t062/build-manifest.json"; d=json.load(open(f))
for r in d:
    s=r["service"]; p="infrastructure" if s in ("discovery-server","api-gateway") else "services"
    j=glob.glob(f"/opt/flash-ticket-build/t062-ac33155/{p}/{s}/target/{s}-*.jar")[0]
    r["rca_faults_classes_in_jar"]=sum("RcaFaults" in n for n in zipfile.ZipFile(j).namelist())
json.dump(d,open(f,"w"),indent=2)
print([(r["service"],r["rca_faults_classes_in_jar"]) for r in d])
