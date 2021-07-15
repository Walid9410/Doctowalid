
import json 

Utilisateur=str('walid2')
mdp = str('friha')
mail = str('mail')
tel= '113'
    
data = { 
            	"ressourceType":"patient",
            "Username": Utilisateur,
            "password":mdp,
            "mail":mail,
            "phone":tel,
	"organization": "/fhir/Organization?_id=1"
            
            }
with open (Utilisateur+".json","w") as f_write:
    
    json.dump(data,f_write,indent=1)

