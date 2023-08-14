import pandas as pd
import re 

class Data:
    '''
    Class related to data manipulation

    Methods:
        clean_smiles(self, name_column, smiles_column, reaction=False): Get only product and remove atom mappings of reaction smiles. Returns a dataframe with the compound name and smiles.
        add_head_tail(self, head_pattern, tail_pattern): Remove m2p noble gases assignment from output dataset and add head and tail nomenclature. Returns a dataset.
        get_results(self): Get only results without errors. Returns a dataset.
        separate_copolymers(self, smiles_row): Separates copolymers with 2 monomers of copolymers with 3 monomers. Returns a dataset.
        clean_all_tokens(self, row_to_clean, regex_pattern): Transforms list of tuples into smiles notation. Returns a dataset.
    ''' 

    def __init__(self, data):
        '''Initialize the instance of a class.

        Arguments:
            data(dataframe): Dataframe which contains information about polymers. Can be the input or output.
        '''
        self.data = data

    def clean_smiles(self, name_column, smiles_column, reaction=False):
        '''Get only product and remove atom mappings of reaction smiles. Returns a dataframe with the compound name and smiles.
        
        Parameters:
        name_column(str): The name of the name column.
        smiles_column(str): The name of the smiles column.
        reaction(boolean): if the input is a reaction add True.'''
        compName = []
        smilesList = []

        if reaction == True:
            for index, row in self.data.iterrows():
                compName.append(index)
                reactionSmiles = row[smiles_column]

                productSmiles = re.findall('(?:.*?\>){2}(.*)', reactionSmiles)
                cleanSmiles = re.sub('\:\d{1,2}|\|.+|^\[\'| |\'\]$', '', str(productSmiles))

                smilesList.append(cleanSmiles)
        
        else:
            for index, row in self.data.iterrows():
                compName.append(index)
                reactionSmiles = row[smiles_column]

                cleanSmiles = re.sub('\:\d{1,2}|\|.+|^\[\'| |\'\]$', '', str(reactionSmiles))

                smilesList.append(cleanSmiles)

        data2 = zip(compName, smilesList)
        df = pd.DataFrame(data2, columns=[name_column, 'smiles']).set_index(name_column)

        return df

    def add_head_tail(self, head_pattern, tail_pattern):
        '''Remove m2p noble gases assignment from output dataset and add head and tail nomenclature. Returns a dataset.
        
        Parameters:
        head_pattern(str): The regex pattern of the head notation.
        tail_pattern(str): The regex pattern of the tail notation.'''
        df_headtail = self.data
        for index, row in df_headtail.iterrows():
            smilesrxn = row['smiles_polymer']

            head = re.sub(head_pattern, '[*:1]', str(smilesrxn))
            tail = re.sub(tail_pattern, '[*:2]', str(head))
            df_headtail.at[index,'smiles_polymer_head_tail'] = tail

            cols = df_headtail.columns.tolist()
            #cols = cols[:6] + cols[-1:] + cols[-2:-1]
            df_headtail = df_headtail[cols]
        
        return df_headtail

    def get_results(self):
        '''Get only results without errors. Returns a dataset.'''
        count = 0
        newData = []
        for index, row in self.data.iterrows():
            if (row['smiles_polymer'] != 'ERROR_01:NoReaction' and
                row['smiles_polymer'] != "ERROR_02:MultiplePolymerizations"):
                newData.append(row)
                count = count + 1

        result = pd.DataFrame(newData)
        
        return result
    
    def separate_copolymers(self, smiles_row):
        '''Separates copolymers with 2 monomers of copolymers with 3 monomers. Returns a dataset.'''

        homopolymer = []
        copolymer2 = []
        copolymer3 = []
        copolymer4 = []
        for index, row in self.data.iterrows():
            if bool(re.match(r"^[^.]+\.[^.]+$", str(row[smiles_row]))) == True:
                copolymer2.append(row)
            
            elif bool(re.match(r"^[^.]+\.[^.]+\.[^.]+$", str(row[smiles_row]))) == True:
                copolymer3.append(row)

            elif bool(re.match(r".*\..*\..*", str(row[smiles_row]))) == True:
                copolymer4.append(row)

            elif bool(re.match(r"^[^.]+\.[^.]+$", str(row[smiles_row]))) == False:
                homopolymer .append(row)

        result2 = pd.DataFrame(copolymer2)
        result3 = pd.DataFrame(copolymer3)
        result4 = pd.DataFrame(copolymer4)
        result1 = pd.DataFrame(homopolymer)

        return result1, result2, result3, result4

    def clean_all_tokens(self, row_to_clean, regex_pattern):
        '''Transforms list of tuples into smiles notation. Returns a dataset.
        
        Paramenters:
        row_to_clean(str): name of the row to be cleaned.
        regex_pattern(str): regex pattern to be cleaned.'''
        df = self.data
        for index, row in df.iterrows():
            monomers = row[row_to_clean]

            head = re.sub(regex_pattern, '', str(monomers))
            df.at[index,'smiles_polymer_noToken'] = head

            cols = df.columns.tolist()
            # cols = cols[:6] + cols[-1:] + cols[-2:-1]
            df = df[cols]    

        return df