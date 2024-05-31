def replace_and_save(input_file, output_file_prefix, replacement_list, i):
    with open(input_file, 'r') as file:
        content = file.read()

    for replacement_string in replacement_list:
        modified_content = content.replace(f"ProdPDFchebyshev{i}", replacement_string)
        output_file = f"{output_file_prefix}_{replacement_string}.txt"

        with open(output_file, 'w') as file:
            file.write(modified_content)

if __name__ == "__main__":
    for N in ['2']:
        for i in ["1","2"]:
            input_file_path = f"datacard_comb_sig_cat{N}_chebyshev{i}.txt"
            output_file_prefix = f"datacard_comb_sig_cat{N}"
            replacement_strings = [f"ProdPDFfewz_chebyshev{i}", f"ProdPDFSumTwoExpPdfchebyshev{i}",f"ProdPDFbwz_reduxchebyshev{i}"] 
            #"chebyshev4","bernstein2","bernstein3"]

            replace_and_save(input_file_path, output_file_prefix, replacement_strings,i)