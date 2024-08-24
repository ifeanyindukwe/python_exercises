import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class RainfallPlots:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.start_date_october = pd.Timestamp('2023-10-01')
        self.filtered_data_since_october = self.data[self.data['Date'] >= self.start_date_october]
        self.last_7_days_data = self.data.tail(7)

    def cumulative_rainfall_plot(self):
        self.filtered_data_since_october['Cumulative_Rainfall'] = self.filtered_data_since_october['Value'].cumsum()

        cumulative_rainfall_plot = go.Figure()
        cumulative_rainfall_plot.add_trace(go.Scatter(
            x=self.filtered_data_since_october['Date'],
            y=self.filtered_data_since_october['Cumulative_Rainfall'],
            mode='lines+markers',
            name='Cumulative Rainfall'
        ))

        cumulative_rainfall_plot.update_layout(
            title='Cumulative Rainfall at Uruti at Kaka Rd since 1 October 2023',
            xaxis_title='Date',
            yaxis_title='Cumulative Rainfall (mm)',
            xaxis=dict(tickangle=-45)
        )

        cumulative_rainfall_plot.show()

    def rainfall_bar_plot_since_october(self):
        bar_plot_october = px.bar(
            self.filtered_data_since_october,
            x='Date',
            y='Value',
            title='Daily Rainfall at Uruti at Kaka Rd since 1 October 2023',
            labels={'Value': 'Rainfall (mm)', 'Date': 'Date'}
        )
        bar_plot_october.update_layout(xaxis_title="Date", yaxis_title="Rainfall (mm)", xaxis_tickangle=-45)
        bar_plot_october.show()

    def rainfall_bar_plot_last_7_days(self):
        bar_plot_last_7_days = px.bar(
            self.last_7_days_data,
            x='Date',
            y='Value',
            title='Daily Rainfall at Uruti at Kaka Rd for the Last 7 Days',
            labels={'Value': 'Rainfall (mm)', 'Date': 'Date'}
        )
        bar_plot_last_7_days.update_layout(xaxis_title="Date", yaxis_title="Rainfall (mm)", xaxis_tickangle=-45)
        bar_plot_last_7_days.show()


if __name__ == "__main__":
    file_path = 'data/Uruti_at_Kaka_Rd_Rainfall.csv'
    rainfall_plots = RainfallPlots(file_path)
    rainfall_plots.cumulative_rainfall_plot()
    rainfall_plots.rainfall_bar_plot_since_october()
    rainfall_plots.rainfall_bar_plot_last_7_days()
