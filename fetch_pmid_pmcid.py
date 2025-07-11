import requests
import time
import pandas as pd

MAIL = ''
API_KEY = ''

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
                print(f" Failed to fetch batch starting at {start}")
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
	                print(f" Error parsing PMCID response: {e}")
	        else:
	            print(f" Failed to fetch PMCIDs for batch (status {response.status_code})")

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
        df.to_csv("pmid_to_pmcid.csv", index=False)
    else:
        print("No PMIDs found.")
