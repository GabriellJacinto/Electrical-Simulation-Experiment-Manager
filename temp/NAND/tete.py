import pandas as pd

# Step 1: Read the text file into a list of strings
with open('nand.mt0', 'r') as file:
    lines = file.readlines()[2:]

#print(lines)
# Step 2: Process the list to remove unwanted characters or lines
lines = [line.strip() for line in lines if line.strip()]
print(lines)
# Step 3: Extract column names from the 6th line
#columns = lines[5].split()

# Step 4: Extract data starting from the 8th line
#data_lines = lines[7:]

# Step 5: Split the data lines into columns
#data = [line.split() for line in data_lines]

# Step 6: Create a pandas DataFrame
#df = pd.DataFrame(data, columns=columns)

# Display the resulting DataFrame
#print(df)
