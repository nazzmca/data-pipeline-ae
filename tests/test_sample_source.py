import unittest

from src.pipeline.sample_source import load_sample_dataset


class SampleSourceTests(unittest.TestCase):
    def test_load_sample_dataset_reads_control_files(self):
        dataset = load_sample_dataset()

        self.assertGreaterEqual(len(dataset), 2)

        data_files = {item["data_file"].name for item in dataset}
        self.assertIn("sample_orders.parquet", data_files)
        self.assertIn("sample_products.parquet", data_files)

        for item in dataset:
            self.assertEqual(item["record_count"], len(item["rows"]))
            self.assertTrue(item["business_date"])


if __name__ == "__main__":
    unittest.main()
