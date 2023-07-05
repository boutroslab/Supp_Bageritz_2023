# This script needs to be run from a directory that contains the metadata_file,
# the cell_barcode_directory and the bam_files_directory.
# It needs python3 and the packages pandas and pysam to be installed.
# In order to run it please type: python3 extract_cb_and_subsample.py
# It first extracts the cell_barcodes in the cell barcode list from the bam files,
# then subsample them to the value listed in the metadata_file and then further
# subsamples it to 75%, 50% and 25% of that value.
# If you have any question please contact Erica Valentini e.valentini@dkfz.de
import glob
import os
import pandas as pd
import pysam
import subprocess

metadata_file = "metadata.tsv"
cell_barcodes_directory =  "cell_barcode_list/"
bam_files_directory = "bam_files/"
extra_subsample_percentages = ['75', '50', '25']

create df from meta file
meta = pd.read_csv(filepath_or_buffer=metadata_file, delimiter="\t")
meta = meta[['BAM file name', 'Percentage of reads to keep']]
meta.columns = ['bam_file', 'percentage_of_reads']
print(meta)
meta['BAM_FILE_RENAMED'] = meta.bam_file.str.replace("[", "")
meta['BAM_FILE_RENAMED'] = meta.BAM_FILE_RENAMED.str.replace("]", "")
print(meta)


for file in os.listdir(cell_barcodes_directory):
    if file[-4:] == ".txt":
        file_name = file[:-4]
        bc_list = []
        print(file_name)
        with open(cell_barcodes_directory + file, "r") as bc:
            for row in bc:
                bc_list.append(row.strip())
        print(bc_list)
        for index, row in meta.iterrows():
            if file_name in row['BAM_FILE_RENAMED']:
                print(file_name, row['BAM_FILE_RENAMED'])
                bam_file = bam_files_directory + row['BAM_FILE_RENAMED']
                print(bam_file)
                filter_bam = bam_files_directory + "filter_bam/" + row['BAM_FILE_RENAMED'] + ".filter.bam"
                if not os.path.exists(filter_bam):
                    # Filter bam files according to the cell barcode
                    print("creating filtered bam file: " + filter_bam)
                    bamfile = pysam.AlignmentFile(bam_file, "rb")
                    bamfile_filter = pysam.AlignmentFile(filter_bam, "wb", template=bamfile)
                    for read in bamfile.fetch(until_eof=True):
                        if read.get_tag("XC:Z:") in bc_list:
                            bamfile_filter.write(read)
                    bamfile_filter.close()
                    bamfile.close()
                # Downsample (normalize) filtered bam files
                percentage = row['percentage_of_reads']
                print(percentage)
                output_file = bam_files_directory + "downsampled/" + row['BAM_FILE_RENAMED'] + ".filtered." + str(percentage) + ".bam.100.bam"
                print("creating normalized bam file: " + output_file)
                if percentage != 100:
                    rows_ds = pysam.view('-s', '0.'+str(percentage), '-b', filter_bam)
                else:
                    rows_ds = pysam.view('-b', filter_bam)
                with open(output_file, "wb") as f:
                    f.write(rows_ds)
                i = 1
                # Downsample (normalize) filtered bam files to different percentages
                for value in extra_subsample_percentages:
                    output_file_extra = bam_files_directory + "downsampled/" + row['BAM_FILE_RENAMED'] + ".filtered." + str(percentage) + ".bam." + value + ".bam"
                    print("creating subsampled bam file: " + output_file_extra)
                    rows_ds_per = pysam.view('-s', str(i)+"."+value, '-b', output_file)
                    with open(output_file_extra, "wb") as fper:
                        fper.write(rows_ds_per)
                    i += 1
