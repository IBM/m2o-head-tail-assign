from m2pCalc.data import Data

import pandas as pd
from IPython.display import display
from rdkit import Chem


class Performance:
    '''
    Class related to data performance calculation

    Methods:

        _compare(self, df_merged) -> (list): Private method. Compare SMILES strings. Returns list.
        _canonicalize(self, df_merged): Private method. Performs the canonicalization of SMILES strings. Returns Dataframe.
        validate_results(self, df1_smiles, df2_smiles): Performs the validation of the results by comparing predicted data with actual data. Returns Dataframe.
        calculate_performance_name(self): Calculates the performance of the m2p algorithm. It uses the formula data_calculated/total_data*100. Returns string.
        get_not_calculated(self): Get only the polymers which m2p could not polymerize. Returns dataframe.
        
        '''
    def __init__(self, df1, df2):
        '''Initialize the instance of a class.

        Arguments:
            df1(dataframe): Dataframe which contains m2p output.
            df2(dataframe): Dataframe which contains m2p input.
        '''
        self.df1 = df1
        self.df2 = df2

    def _compare(self, df_merged) -> (list):
        '''Private method. 
        Compare SMILES strings. Returns list.
        
        Arguments:
            df_merged(dataframe): Dataframe which contains merged data from df1 and df2.'''

        df_rows = len(df_merged)

        n = 0

        number = []
        tf = []

        while n < df_rows:
            a = set(df_merged['canonicalized_x'][n]).issubset(df_merged['canonicalized_y'][n])
            number.append(n)
            tf.append(a)

            n += 1

        df_res = pd.DataFrame({'number': number, 'boolean': tf})

        res = []
        def f(x, y):
            if y == False:
                res.append(x)

        result = [f(x, y) for x, y in zip(df_res['number'], df_res['boolean'])]
        print(f'{len(res)} results are False, those are: {res}')

        return res

    def _canonicalize(self, df_merged):
        '''Private method. 
        Performs the canonicalization of SMILES strings. Returns Dataframe.
        
        Arguments:
            df_merged(dataframe): Dataframe which contains merged data from df1 and df2.'''
        n = 0

        df_rows = len(df_merged)

        df1_can_res = []
        df2_can_res = []

        while n < df_rows:
            try:
                df1_can= [Chem.MolToSmiles(Chem.MolFromSmiles(df_merged['smiles_polymer_x'][n]),True)]
                df2_can= [Chem.MolToSmiles(Chem.MolFromSmiles(df_merged['smiles_polymer_y'][n]),True)]

                df1_can_res.append(df1_can)
                df2_can_res.append(df2_can)
            except:
                df1_can_res.append('no')
                df2_can_res.append('no')

            n += 1

        df_merged['canonicalized_x'] = df1_can_res
        df_merged['canonicalized_y'] = df2_can_res

        return

    def validate_results(self, df1_smiles, df2_smiles):
        '''Performs the validation of the results by comparing predicted data with actual data. Returns Dataframe.
        
        Arguments:
            df1_smiles(str): Name of the SMILES column of df1.
            df2_smiles(str): Name of the SMILES column of df2.'''
        
        df1 = self.df1.sort_values([df1_smiles], key=lambda x: x.str.len())
        df2 = self.df2.sort_values([df2_smiles], key=lambda x: x.str.len())

        df_merged = df2.merge(df1, on='smiles')

        self._canonicalize(df_merged)

        self._compare(df_merged)

        return

    def calculate_performance(self) -> (str):
            '''Calculates the performance of the m2p algorithm. It uses the formula data_calculated/total_data*100. Returns string.'''

            df1_rows = len(self.df1.index)
            df2_rows = len(self.df2.index)

            result = round((df1_rows / df2_rows)*100)
            print(f'Performance = {result}%')
            
            return

    def get_not_calculated(self):
        '''Get only the polymers which m2p could not polymerize. Returns dataframe.'''

        df2 = self.df2[['smiles','classes','smiles_polymer']]
        df1 = self.df1.rename(columns={'mechanism': 'classes'})
        merged = df1.merge(df2, on='smiles', indicator=True, how='outer')
        merged = merged[merged['_merge'] != 'both']

        merged_rows = len(merged)
        print(f'm2p algorithm could not calculate {merged_rows} polymers')

        return merged