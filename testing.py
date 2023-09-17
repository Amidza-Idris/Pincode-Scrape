import requests
import json
import pandas as pd

# Load list of pins
df = pd.read_csv('Pin.csv', encoding='latin1', index_col=False)
df = df.drop_duplicates(subset=['Pincode'])
pin_codes = df['Pincode'] # Add more pin codes as needed

api_url = "https://www.utimf.com/service/get-advisor-data/"

# Empty list to store dictionaries data
all_data = []

def scrape(pin):
    params = {"pincode": pin}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        print(response.text, "\n")  #check 1 (this can be deleted for optimization)
        advisor_data = json.loads(response.text)

        if not advisor_data:  # Check if advisor_data is empty
            return 0

        main_dict = {}

        for elem_dict in advisor_data:
            for key, value in elem_dict.items():
                if key not in main_dict:
                    main_dict[key] = []
                main_dict[key].append(value)

        # Convert lists to strings
        for key, value in main_dict.items():
            if key != 'pincode':
                main_dict[key] = ', '.join(value)

        # Create a new key at the beginning for 'pincode'
        main_dict = {'pincode': int(pin), **main_dict}
        main_dict['pincode'] = int(pin)

        return main_dict
    else:
        print("API request for pin code {pin} failed with status code:", response.status_code)
        return (1)
ijk = 0
for pinc in pin_codes:
    print(pinc, "\n")
    
    ijk = ijk + 1
    if ijk == 100:
        break
    to_process = scrape(pinc)

    if to_process == 0:
        continue
    elif to_process == 1:
        continue
    else:
        all_data.append(to_process)

# Create a Pandas DataFrame from the dictionary
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
output_filename = "advisor_data.xlsx"
df.to_excel(output_filename, index=False)

print(f"Data saved to {output_filename}")
