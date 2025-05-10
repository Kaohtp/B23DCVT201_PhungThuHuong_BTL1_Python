#Vẽ biểu đồ histogram cho từng chỉ số (toàn giải và từng đội), lưu vào thư mục histograms/.
import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class StatHistogramPlotter:
    def __init__(self, csv_path, output_dir, stats, team_col='Team', teams_per_img=20):
        self.df = pd.read_csv(csv_path, encoding='utf-8')
        self.output_dir = output_dir
        self.stats = stats
        self.team_col = team_col
        self.teams_per_img = teams_per_img
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def _safe_filename(self, s):
        return ''.join(c if c.isalnum() else '_' for c in s)[:80]

    def _sturges_bins(self, data):
        n = len(data)
        if n < 2:
            return 1
        return int(np.ceil(np.log2(n) + 1))

    def plot_overall(self, stat):
        if stat not in self.df.columns:
            return
        data = pd.to_numeric(self.df[stat], errors='coerce').dropna()
        if data.empty:
            return
        bins = self._sturges_bins(data)
        plt.figure(figsize=(8, 5))
        plt.hist(data, bins=bins, color='steelblue', edgecolor='black')
        plt.title(f'Overall: {stat}')
        plt.xlabel(stat)
        plt.ylabel('Frequency')
        plt.tight_layout()
        fname = f"all_{self._safe_filename(stat)}.png"
        plt.savefig(os.path.join(self.output_dir, fname))
        plt.close()

    def plot_by_team(self, stat):
        if stat not in self.df.columns or self.team_col not in self.df.columns:
            return
        teams = sorted(self.df[self.team_col].dropna().unique())
        for i in range(0, len(teams), self.teams_per_img):
            group = teams[i:i+self.teams_per_img]
            nrows = math.ceil(len(group) / 5)
            fig, axes = plt.subplots(nrows, min(5, len(group)), figsize=(16, 3.5*nrows))
            axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]
            for j, team in enumerate(group):
                ax = axes[j]
                team_data = pd.to_numeric(self.df[self.df[self.team_col] == team][stat], errors='coerce').dropna()
                if not team_data.empty:
                    bins = self._sturges_bins(team_data)
                    ax.hist(team_data, bins=bins, color='orange', edgecolor='black')
                    ax.set_title(team, fontsize=9)
                    ax.set_xlabel('')
                    ax.set_ylabel('')
                else:
                    ax.set_visible(False)
            for k in range(len(group), len(axes)):
                axes[k].set_visible(False)
            plt.suptitle(f'{stat} by Team (Group {i//self.teams_per_img+1})', fontsize=14)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            fname = f"teams_{self._safe_filename(stat)}_g{i//self.teams_per_img+1}.png"
            plt.savefig(os.path.join(self.output_dir, fname))
            plt.close()

if __name__ == '__main__':
    stats = [
        'Performance: goals',
        'Performance: assists',
        'Standard: shoots on target percentage (SoT%)',
        'Blocks: Int',
        'Performance: Recov',
        'Challenges: Att'
    ]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = "Report/OUTPUT_BAI2/stat_histograms"
    csv_file = "Report/OUTPUT_BAI1/results.csv"
    plotter = StatHistogramPlotter(csv_file, out_dir, stats)
    for stat in stats:
        plotter.plot_overall(stat)
        plotter.plot_by_team(stat)