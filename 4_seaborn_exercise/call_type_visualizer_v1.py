import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class CallTypeVisualizer:
    def __init__(self, file_path):
        """
        Initialize the class with the path to the CSV file.
        
        :param file_path: The path to the CSV file containing the dataset.
        """
        self.file_path = file_path
        self.df = None
        self.call_type_counts = None

    def load_data(self):
        """Load the dataset from the CSV file."""
        self.df = pd.read_csv(self.file_path)

    def count_call_types(self):
        """Count the occurrences of each call type."""
        if self.df is not None:
            self.call_type_counts = self.df['Call Type'].value_counts()
        else:
            raise ValueError("DataFrame is empty. Please load the data first.")

    def plot_call_type_distribution(self):
        """Create and display a bar graph for the number of occurrences of each call type."""
        if self.call_type_counts is not None:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=self.call_type_counts.index, y=self.call_type_counts.values)
            plt.title('Number of Occurrences for Each Call Type')
            plt.xlabel('Call Type')
            plt.ylabel('Number of Occurrences')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        else:
            raise ValueError("Call type counts are empty. Please count the call types first.")

    def visualize(self):
        """Complete process: load data, count call types, and plot the distribution."""
        self.load_data()
        self.count_call_types()
        self.plot_call_type_distribution()

if __name__ == "__main__":
    file_path = r'data\why_did_this_take_so_long.csv'
    visualizer = CallTypeVisualizer(file_path)
    visualizer.visualize()
