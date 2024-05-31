
import os
import pandas as pd
import sys


nocats =False

#datasets = ['data_x']
#datasets = ['ggh_powheg']
datasets = ['vbf_powheg']

if sys.argv[1] == 'all':
    years = ['2016preVFP','2016postVFP','2017','2018']
else:
    years = [str(sys.argv[1])]
label = sys.argv[2]
# Iterate through each CSV file
if nocats==True:
    for dataset in datasets:
        combined_data = pd.DataFrame()
        for year in years:

            data_dir = f'/depot/cms/hmm/vscheure/{label}/stage2_output/{year}/{dataset}/'
        
            # Get a list of CSV files in the directory
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            for csv_file in csv_files:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(os.path.join(data_dir, csv_file))
        
                # Remove the year from the "category" column
                df['category'] = df['category'].apply(lambda x: x.replace(str(year), '').strip())

            # Concatenate the current DataFrame with the combined_data DataFrame
            combined_data = pd.concat([combined_data, df], ignore_index=True)
            for i in range(5):
                df_test = combined_data[combined_data["category"] == f"phifixedBDT_cat{i}"]
                #print(df_test)
                #print(df_test["wgt_cumsum_normed"])

            # Save the combined data to a new CSV file
        if len(years)>1:
            #os.remove(f'/depot/cms/hmm/vscheure/{label}/stage2_output/combined/{dataset}/{dataset}.csv')
            combined_data.to_csv(f'/depot/cms/hmm/vscheure/{label}/stage2_output/combined/{dataset}/{dataset}.csv', index=False)
        if len(years)==1:
            #os.remove(f'/depot/cms/hmm/vscheure/{label}/stage2_output/{year}/{dataset}/{dataset}.csv')
            combined_data.to_csv(f'/depot/cms/hmm/vscheure/{label}/stage2_output/{year}/{dataset}/{dataset}.csv', index=False)

    print("Combined data saved to combined_data.csv")
else:
    for dataset in datasets:
        combined_data = pd.DataFrame()
        for year in years:

            data_dir = f'/depot/cms/hmm/vscheure/{label}/stage2_output/{year}/{dataset}/'
        
            # Get a list of CSV files in the directory
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            for csv_file in csv_files:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(os.path.join(data_dir, csv_file))
            
                # Remove the year from the "category" column
                df['category'] = "All"

            # Concatenate the current DataFrame with the combined_data DataFrame
            combined_data = pd.concat([combined_data, df], ignore_index=True)
            
            # Save the combined data to a new CSV file

        #os.remove(f'/depot/cms/hmm/vscheure/{label}/stage2_output/combined/{dataset}/{dataset}_nocats.csv')
        if len(years)>1:
            #os.remove(f'/depot/cms/hmm/vscheure/{label}/stage2_output/combined/{dataset}/{dataset}_nocats.csv')
            combined_data.to_csv(f'/depot/cms/hmm/vscheure/{label}/stage2_output/combined/{dataset}/{dataset}_nocats.csv', index=False)
        if len(years)==1:
            #os.remove(f'/depot/cms/hmm/vscheure/{label}/stage2_output/{year}/{dataset}/{dataset}_nocats.csv')
            combined_data.to_csv(f'/depot/cms/hmm/vscheure/{label}/stage2_output/{year}/{dataset}/{dataset}_nocats.csv', index=False)

print("Combined data saved to combined_data.csv")