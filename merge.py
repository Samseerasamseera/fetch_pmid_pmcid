# import requests

# MAIL = 'mahammadn143@gmail.com'
# API_KEY = '41bb5a3ad524015540f7f39ebdeb24dbf209'

# class PubMedProcessor:

#     def __init__(self, molecule, user_email=MAIL, user_pmid_api_key=API_KEY):
#         self.molecule = molecule
#         self.user_email = user_email
#         self.user_pmid_api_key = user_pmid_api_key
#         self.tool_name = "Gene-ius pathways"
#         self.pmid_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#         self.idconv_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"

#         self.pmid_params = {
#             "db": "pubmed",
#             "term": self.search_query_generator(molecule),
#             "retmode": "json",
#             "retmax": 10000,
#             "tool": self.tool_name,
#             "email": user_email,
#             "api_key": self.user_pmid_api_key
#         }

#     def search_query_generator(self, molecule):
#         return f'"{molecule}" AND "pathway" AND "signaling pathway"'

#     def fetch_pmids(self):
#         response = requests.get(self.pmid_url, params=self.pmid_params)
#         if response.status_code == 200:
#             try:
#                 data = response.json()
#                 return data.get("esearchresult", {}).get("idlist", [])
#             except Exception as e:
#                 print(f"Error parsing PMIDs: {e}")
#                 return []
#         else:
#             print(f"Failed to fetch PMIDs: {response.status_code}")
#             return []
    

#     def convert_pmids_to_pmcids(self, pmids):
#         pmid_to_pmcid = {}
#         batch_size = 200
#         batches = [pmids[i:i + batch_size] for i in range(0, len(pmids), batch_size)]

#         for batch in batches:

#             print(",".join(batch))

#         for batch in batches:
#             params = {
#                 "tool": self.tool_name,
#                 "email": self.user_email,
#                 "format": "json",
#                 "ids": ",".join(batch)
#             }
#             response = requests.get(self.idconv_url, params=params)
#             if response.status_code == 200:
#                 try:
#                     data = response.json()
#                     for record in data.get("records", []):
#                         pmid = record.get("id")
#                         pmcid = record.get("pmcid")
#                         if pmid and pmcid:
#                             pmid_to_pmcid[pmid] = pmcid
#                 except Exception as e:
#                     print(f"Error parsing PMCID response: {e}")
#             else:
#                 print(f"Failed to fetch PMCIDs for batch: {response.status_code}")
        
#         return pmid_to_pmcid


# processor = PubMedProcessor("IL 24")
# pmids = processor.fetch_pmids()
# pmid_to_pmcid_map = processor.convert_pmids_to_pmcids(pmids)

# print(pmid_to_pmcid_map)
# import requests

# class PubMedProcessor:
#     def __init__(self, molecule, user_email="samshisam87@gmail.com", user_pmid_api_key="2d95e759a9ae1dd725248f9ab5bd6b3b2d09"):
#         self.molecule = molecule
#         self.user_email = user_email
#         self.user_pmid_api_key = user_pmid_api_key
#         self.tool_name = "Gene-ius pathways"
#         self.pmc_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

#         self.pmc_params = {
#             "db": "pmc",  # 🔥 Direct search in PMC
#             "term": self.search_query_generator(molecule),
#             "retmode": "json",
#             "retmax": 10000,
#             "tool": self.tool_name,
#             "email": self.user_email,
#             "api_key": self.user_pmid_api_key
#         }

#     def search_query_generator(self, molecule):
#         return f'"{molecule}" AND "pathway" AND "signaling pathway"'

#     def fetch_pmcids(self):
#         response = requests.get(self.pmc_url, params=self.pmc_params)
#         if response.status_code == 200:
#             try:
#                 data = response.json()
#                 return [f"PMC{id_}" for id_ in data.get("esearchresult", {}).get("idlist", [])]
#             except Exception as e:
#                 print(f"Error parsing PMC IDs: {e}")
#                 return []
#         else:
#             print(f"Failed to fetch PMC IDs: {response.status_code}")
#             return []


# # Example usage
# processor = PubMedProcessor("IL 24")
# pmc_ids = processor.fetch_pmcids()
# print(pmc_ids)
# import requests
import requests
import time
import pandas as pd

MAIL = 'samshisam87@gmail.com'
API_KEY = '2d95e759a9ae1dd725248f9ab5bd6b3b2d09'

class PubMedProcessor:
    def __init__(self, molecule, user_email=MAIL, user_api_key=API_KEY):
        self.molecule = molecule
        self.email = user_email
        self.key = user_api_key
        self.tool = "Gene-ius-pathways"
        self.pmid_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.idconv_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"

    def search_query_generator(self, molecule):
        return f'"{molecule}"'

    def fetch_all_pmids(self):
        all_pmids = []
        batch_size = 200
        start = 0

        while True:
            params = {
                "db": "pubmed",
                "term": self.search_query_generator(self.molecule),
                "retmode": "json",
                "retmax": batch_size,
                "retstart": start,
                "tool": self.tool,
                "email": self.email,
                "api_key": self.key
            }
            res = requests.get(self.pmid_url, params=params)
            if res.status_code != 200:
                print(f"❌ Failed to fetch batch starting at {start}")
                break
            data = res.json()
            batch_pmids = data.get("esearchresult", {}).get("idlist", [])
            if not batch_pmids:
                break
            all_pmids.extend(batch_pmids)
            start += batch_size
            time.sleep(0.4)

        return all_pmids

    def convert_pmids_to_pmcids_df(self, pmids):
	    results = []
	    batch_size = 200
	    headers = {
	        "User-Agent": f"{self.tool}/1.0 (mailto:{self.email})"
	    }
	    batches = [pmids[i:i + batch_size] for i in range(0, len(pmids), batch_size)]

	    for batch in batches:
	        params = {
	            "tool": self.tool,
	            "email": self.email,
	            "api_key": self.key,
	            "format": "json",
	            "ids": ",".join(batch)
	        }
	        response = requests.get(self.idconv_url, headers=headers, params=params)
	        if response.status_code == 200:
	            try:
	                data = response.json()
	                # Create a lookup of pmid to pmcid
	                record_map = {str(r.get("pmid")): r.get("pmcid") for r in data.get("records", [])}

	                for pmid in batch:
	                    pmcid = record_map.get(pmid)
	                    results.append({"PMID": pmid, "PMCID": pmcid})
	            except Exception as e:
	                print(f"❌ Error parsing PMCID response: {e}")
	        else:
	            print(f"❌ Failed to fetch PMCIDs for batch (status {response.status_code})")

	    return pd.DataFrame(results)


# ==== Main Run ====
if __name__ == "__main__":
    mol = "IL19"
    processor = PubMedProcessor(mol)

    pmids = processor.fetch_all_pmids()

    print(f"Searched Molecule: {mol}")
    print(f"PMIDs Fetched: {len(pmids)}\n")

    if pmids:
        df = processor.convert_pmids_to_pmcids_df(pmids)
        print("🔎 PMID → PMCID Mapping (DataFrame):\n")
        print(df)

        df.to_csv("pmid_to_pmcid.csv", index=False)
        df.to_excel("pmid_to_pmcid.xlsx", index=False)

    else:
        print("❌ No PMIDs found.")
