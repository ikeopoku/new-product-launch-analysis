# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define columns to be used
employer_cols = ['company', 'industries', 'country_territory', 'employees']
company_cols = ['Company', 'Sales ($billion)', 'Profits ($billion)',
                'Assets ($billion)', 'Market Value ($billion)', 'Country']

# Load a CSV file into pandas DataFrame
employer_data = pd.read_csv(r"C:\Users\1\Documents\Dataset\forbes_best_employers_2023.csv",
                            usecols=employer_cols)
company_data = pd.read_csv(r"C:\Users\1\Documents\Dataset\Largest_Companies_In_The_World.csv",
                           usecols=company_cols, dtype={1: str, 6: str})

# Print first ten lines of the DataFrame
print(employer_data.head(5))
print(company_data.head(5))

# Get summary information about the DataFrame
print(employer_data.info())
print(company_data.info())

# Merging the two Dataframes using inner join on left 'company'and right 'Company' by validating and indicating the join
data = employer_data.merge(company_data, left_on='company', right_on='Company',
                                       how='inner', validate='one_to_many', indicator=True)

# Display all columns in the DataFrame
pd.set_option('display.max_columns', None)
	
# Get summary information about the DataFrame
print(data.info())
print(data.head(3))

# Drop 'country_territory' and "Company" columns, and inplace DataFrame
data.drop(['country_territory','Company'], axis=1, inplace=True)
print(data.head(3))

# Extract unique values from "industries" column of the DataFrame
print(data['industries'].unique())

# Replace column name with 'Travel & Leisure'
data['industries'] = data['industries'].replace('Travel & Leisure\xa0\xa0\xa0\xa0\xa0\xa0', 'Travel & Leisure')
print(data['industries'].unique())


# Check for duplicates across all columns
print(data.duplicated())

# Information about the DataFrame
print(data.info())

# Get statistical summary
print(data.describe())


# Group "industries" and count "company"
counted_data = data.groupby(data['industries']).agg({'company':'count'})

# Sort the counted_data in descending order
sorted_data = counted_data.sort_values('company', ascending=False)

# Show the result of sorted_data
print(sorted_data)



# Define plot style
sns.set_style('whitegrid')

# Define the xticks position and corresponding labels
xticks = (range(len(counted_data)))

xtick_names = ['Conglomerate', 'Information technology', 'Electrical Engineering',
               'Retail & Wholesale', 'Automotive', 'Fashion', 'Aerospace & Defense',
               'Supply Chain', 'Pharmaceutical', 'Travel & Leisure', 'Manufacturing',
               'Food, Beverages & tobacco', 'Banking & Financial','Packaging',
               'Health Services', 'Construction & Extraction', 'Insurance',
               'Telecommunications', 'Media & Advertising',
               'Utilities', 'Business Services', 'Restaurants', 'Professional Services']

# Create countplot with counted_data 
counted_plot = sns.countplot(counted_data, x=data['industries'])

# Set xstick with labels at a 90 degrees rotation
plt.xticks(ticks=xticks, labels=xtick_names, rotation=90)

# Set the title
plt.title('Industries Controlled by Dominant Companies')

# Add x and y labels
plt.xlabel("Types Of Industries")
plt.ylabel("Number Of Dominant Companies")

# Show a graph for the counted_data
plt.show()



# Filter rows where Industries is "IT, Internet, Software & Services"
IT_Industries = data[data["industries"] == "IT, Internet, Software & Services"]

# Print result
print(IT_Industries)



# Use 'seaborn-v0_8-colorblind' and create Figures and Axes with plt.subplots
plt.style.use("seaborn-v0_8-colorblind")
fig, ax = plt.subplots()

# Plot a pie chart of the IT industry Market share
wedges, texts, autotexts = ax.pie(IT_Industries["Sales ($billion)"],
                                  autopct= '%1.1f%%')

# Set legend
ax.legend(title="Companies", labels=IT_Industries["company"],
          loc="center right", bbox_to_anchor=(1, 0, 0.5, 1))

# Set pie chart title
ax.set_title("Market Share for Information Technology Industries")

# Set autopct property for pie chart
plt.setp(autotexts, size=8, weight="bold", color="w")

# Show the pie chart result
plt.show()



# Filter rows where Industry is Transportation and Logistics
Supply_chain = data[data["industries"] == "Transportation and Logistics"]

# Print result
print(Supply_chain.head(3))



# Set the theme style for a scatter plot
sns.set_theme(style="darkgrid")

# Plot the x and y axis of scatter plot
Technology = sns.scatterplot(data=IT_Industries, x="Sales ($billion)", y="Profits ($billion)",
                    style="industries", color="#1686CD", s=100, legend=False)
Supply = sns.scatterplot(data=Supply_chain, x="Sales ($billion)", y="Profits ($billion)",
                style="industries", color="#EA3699", s=100)

# Rename labels
legend_label={"IT": "Technology", "Suppliers": "Supply"}

# Add a title to legend
plt.legend(title="Industries", labels=legend_label)

# Add x and y labels
plt.xlabel("Sales ($billion)")
plt.ylabel("Profits ($billion)")

# Set the title
plt.title("Relationship Between IT And Its Suppliers")

# Show scatter plot
plt.show()



# Replace -5.5 with 5.5 under "Profits ($billion)" 
data['Profits ($billion)'] = data['Profits ($billion)'].replace(-5.5, 5.5)

# Filter rows where the Industry is "Conglomerate"
Conglomerate = data[data["industries"] == "Conglomerate"]



# Use plt.subplots to create figure and axes object
fig, ax = plt.subplots()

# Create stacked bar with labels and colors for bar 1 and bar 2
bar1 = ax.bar(Conglomerate['company'], Conglomerate['Sales ($billion)'],
              label='Sales ($billion)', color='#24b1d1')
bar2 = ax.bar(Conglomerate['company'], Conglomerate['Assets ($billion)'],
              bottom=Conglomerate['Sales ($billion)'], label='Assets ($billion)',
             color='#ae24d1')

# Create, color, and calculate the bottom for bar 3
bottom3 = Conglomerate['Sales ($billion)'] + Conglomerate['Assets ($billion)']
bar3 = ax.bar(Conglomerate['company'], Conglomerate['Profits ($billion)'],
              bottom=bottom3, label='Profits ($billion)', color='deeppink')

# Add, center  and color labels for bar 1, bar 2, and bar 3
ax.bar_label(bar1, label_type='center', color='white')
ax.bar_label(bar2, label_type='center', color='white')
ax.bar_label(bar3, label_type='center')

# X Position, Set xticklabels position and fix warming
xstick_pos = list(range(len(Conglomerate['company'])))
ax.set_xticks(xstick_pos)
ax.set_xticklabels(labels=Conglomerate['company'], rotation=45)

# Add xlabel, ylabel, title, and legend
ax.set_xlabel('Conglomerate Industry')
ax.set_ylabel('Financial Metrics in Billions ($)')
ax.set_title('Performance of Company Substitute Products Across Various Financial Metrics')
ax.legend()

# Call the function
plt.show()


