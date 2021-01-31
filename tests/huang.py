import pandas as pd
import os
import sys
import inspect
import unittest
from glob import glob

currentdir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.data_mani.utils import merge_market_and_gtrends  # noqa
from src.feature_selection.huang import run_huang_methods  # noqa

full_words = ['BUY AND HOLD',
              'DOW JONES',
              'act',
              'arts',
              'bank',
              'banking',
              'blacklist',
              'bonds',
              'bubble',
              'business',
              'buy',
              'cancer',
              'car',
              'carolina',
              'case',
              'cash',
              'ceo',
              'chance',
              'college',
              'color',
              'committee',
              'community',
              'companies',
              'conflict',
              'consume',
              'consumption',
              'corporation',
              'council',
              'county',
              'court',
              'crash',
              'credit',
              'crisis',
              'culture',
              'debt',
              'default',
              'democratic',
              'derivatives',
              'development',
              'district',
              'dividend',
              'dow jones',
              'earnings',
              'economic',
              'economics',
              'economy',
              'elected',
              'election',
              'elections',
              'energy',
              'environment',
              'fed',
              'federal',
              'finance',
              'financial',
              'financial markets',
              'fine',
              'firm',
              'fond',
              'food',
              'forex',
              'founded',
              'freedom',
              'fun',
              'gain',
              'gains',
              'garden',
              'georgia',
              'global',
              'gold',
              'government',
              'governor',
              'greed',
              'growth',
              'happy',
              'headlines',
              'health',
              'hedge',
              'holiday',
              'home',
              'house',
              'housing',
              'illinois',
              'inc',
              'industry',
              'inflation',
              'invest',
              'investment',
              'judge',
              'justice',
              'kentucky',
              'kitchen',
              'labor',
              'law',
              'legal',
              'leverage',
              'lifestyle',
              'loss',
              'ltd',
              'management',
              'market',
              'marketing',
              'markets',
              'marriage',
              'massachusetts',
              'media',
              'members',
              'metals',
              'million',
              'minister',
              'ministry',
              'missouri',
              'money',
              'movement',
              'movie',
              'nasdaq',
              'nyse',
              'office',
              'ohio',
              'oil',
              'opportunity',
              'ore',
              'party',
              'pennsylvania',
              'police',
              'political',
              'politics',
              'portfolio',
              'present',
              'president',
              'products',
              'profit',
              'project',
              'rare earths',
              'religion',
              'representatives',
              'republican',
              'restaurant',
              'return',
              'returns',
              'revenue',
              'rich',
              'rights',
              'ring',
              'risk',
              'seats',
              'secretary',
              'security',
              'sell',
              'senate',
              'served',
              'service',
              'services',
              'short sell',
              'short selling',
              'social',
              'society',
              'stats',
              'stock market',
              'stocks',
              'success',
              'technology',
              'tennessee',
              'texas',
              'tourism',
              'trader',
              'train',
              'transaction',
              'travel',
              'unemployment',
              'union',
              'vermont',
              'virginia',
              'voters',
              'votes',
              'war',
              'washington',
              'water',
              'william',
              'wisconsin',
              'world',
              'york']

words = ['BUY AND HOLD',
         'DOW JONES',
         'act',
         'arts',
         'bank',
         'banking',
         'blacklist',
         'bonds',
         'bubble',
         'business']


class Test_huang(unittest.TestCase):
    def test_huang_basic1(self):
        path_m = os.path.join(parentdir,
                              "src", "data",
                              "toy", "ticker7.csv")
        merged, _ = merge_market_and_gtrends(path_m,
                                             test_size=0.5,
                                             path_gt_list=[parentdir,
                                                           "src",
                                                           "data",
                                                           "gtrends.csv"])
        result = run_huang_methods(merged_df=merged, target_name="target_return",
                                   words=words, max_lag=20, verbose=False,
                                   sig_level=0.05, correl_threshold=0.5, constant_threshold=0.9)
        result = list(result[~result.feature_score.isna()].feature)

        self.assertTrue('banking_1' in result)
        self.assertTrue('bonds_1' in result)
        self.assertTrue(len(result) == 2)

    def test_huang_reproducibility(self):
        path_m = os.path.join(parentdir,
                              "src", "data",
                              "toy", "ticker8.csv")
        merged, _ = merge_market_and_gtrends(path_m,
                                             test_size=0.5,
                                             path_gt_list=[parentdir,
                                                           "src",
                                                           "data",
                                                           "gtrends.csv"])
        result = run_huang_methods(merged_df=merged, target_name="target_return",
                                   words=["DOW JONES", "act", "arts", "bank", "business"], max_lag=20, verbose=False,
                                   sig_level=0.05, correl_threshold=0.5, constant_threshold=0.9)

        self.assertAlmostEqual(result.loc[result['feature'] == 'DOW_JONES_11']['feature_score'].iloc[0],
                               0.004244, places=3)
        self.assertAlmostEqual(result.loc[result['feature'] == 'act_3']['feature_score'].iloc[0],
                               0.004747, places=3)
        self.assertAlmostEqual(result.loc[result['feature'] == 'business_5']['feature_score'].iloc[0],
                               0.041698, places=3)
        self.assertAlmostEqual(result.loc[result['feature'] == 'business_7']['feature_score'].iloc[0],
                               0.010985, places=3)

    def test_huang_singular_matrix(self):
        path_m = os.path.join(parentdir,
                              "src", "data",
                              "toy", "ticker8.csv")
        merged, _ = merge_market_and_gtrends(path_m,
                                             test_size=0.5,
                                             path_gt_list=[parentdir,
                                                           "src",
                                                           "data",
                                                           "gtrends.csv"])
        result = run_huang_methods(merged_df=merged, target_name="target_return",
                                   words=full_words, max_lag=20, verbose=False,
                                   sig_level=0.05, correl_threshold=0.5, constant_threshold=0.9)
        result = list(result[~result.feature_score.isna()].feature)

        list_to_check = ['act_3', 'bonds_17', 'business_8', 'business_15', 'consume_1', 'debt_13',
                         'firm_16', 'gain_6', 'greed_4', 'members_15', 'movement_1', 'nyse_3', 'nyse_5',
                         'nyse_6', 'police_19', 'returns_4', 'success_5', 'world_9']
        for w in list_to_check:
            self.assertTrue(w in result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
