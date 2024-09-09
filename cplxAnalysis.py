#First LOC and static analysis'''
import requests
import subprocess

#from pinecone import Pinecone, ServerlessSpec
h = open("config.txt")
username = h.readline().strip()
data_dir = h.readline().strip()
h.close()


def download_code_from_url(url):
    """
    Download code from a given raw GitHub URL.
    """
    response = requests.get(url)
    if response.status_code == 200:
        print(1)
        return response.text
    else:
        print(f"Error: Unable to download file from {url}")
        return None

def download_code_from_txt(file_path):
    """
    Read a text file containing GitHub URLs and download the corresponding code.
    """
    code_files = {}
    with open(file_path, 'r') as file:
        for url in file.readlines():
            url = url.strip()
            code_content = download_code_from_url(url)
            if code_content:
                # Save the content keyed by the URL
                code_files[url] = code_content
    return code_files

def calculate_loc(code_content):
    """
    Calculate the Lines of Code (LOC) from the given code content.
    Excludes blank lines and comments.
    """
    loc = 0
    for line in code_content.splitlines():
        # Exclude empty lines and comment lines
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('//') and not line.startswith('"""'):
            loc += 1
    return loc

#will finish pylint analysis later
def run_pylint_on_code(code_content, file_path):
    """
    Run PyLint on the given code content.
    """
    with open(file_path, 'w') as temp_file:
        temp_file.write(code_content)
    
    result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
    return result.stdout

code_files = download_code_from_txt(f'{data_dir}/{username}_fileUrls.txt')


# Calculate LOC for each file
#loc_report = {}
#for url, code in code_files.items():
    #loc_report[url] = calculate_loc(code)


with open(f"{data_dir}/{username}_locReport.txt" , "a") as g:
    for url, code in code_files.items():
        g.write(url+"  "+str(calculate_loc(code))+"\n")


''' Print LOC for each file
for url, loc in loc_report.items():
    print(f"{url} - LOC: {loc}")
'''
#Linter analysis
# Example for Python
'''
linter_report = {}
for url, code in code_files.items():
    if url.endswith('.py'):
        pylint_report = run_pylint_on_code(code, 'temp_file.py')
        #print(f"{url} - PyLint Report:\n{pylint_report}")
        linter_report[url] = pylint_report
'''
'''
f=open("secrets.txt","r")
secrets = [r.strip() for r in f.readlines()]
# Initialize Pinecone with your API key and environment
pcone = Pinecone(
    api_key=secrets[0].split("=")[1]
)
f.close()
# Check for existing indexes (optional)
print(pcone.list_indexes())

pcone.create_index(f"{username}-code-cplxity", dimension=1536, metric="cosine")
'''