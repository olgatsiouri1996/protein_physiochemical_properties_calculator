# python3
import argparse
import itertools
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd
# imput parameters
ap = argparse.ArgumentParser(description="outputs the id, pI, charge and molecular weight of each protein")
ap.add_argument("-in", "--input_file", required=True, help="input fasta file")
ap.add_argument("-pH", "--pH", required=True,help=" 1-column txt file with pH values 1 for each protein, to calculate the protein charge")
ap.add_argument("-out", "--output_file", required=True, help="output txt file")
args = vars(ap.parse_args())
# main
headers = []
seqs = []
pI = [] 
charge = []
mw = [] # setup empty lists
for record in SeqIO.parse(args['input_file'], "fasta"):
	headers.append(record.id)
	seqs.append(record.seq)
# import txt file with pH values
with open(args['pH'], 'r') as f:
	ph_values = f.readlines()
ph_values = [x.strip() for x in ph_values] 
# calculate the properties using a pair of the above 2 lists
for (a, b) in itertools.zip_longest(seqs, ph_values):
	prot = ProteinAnalysis(str(a))
	pI.append('%0.2f' % prot.isoelectric_point())
	mw.append('%0.2f' % prot.molecular_weight())
	charge.append('%0.2f' % prot.charge_at_pH(float(b)))
# create data frame
df = pd.DataFrame()
df['id'] = headers
df['pI'] = pI
df['charge'] = charge
df['mw'] = mw
df['pH'] = ph_values
# export
with open(args['output_file'], 'a') as f:
    f.write(
        df.to_csv(header = True, index = False, sep = '\t', doublequote= False, line_terminator= '\n')
    )




