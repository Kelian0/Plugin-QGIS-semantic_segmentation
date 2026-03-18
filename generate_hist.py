import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import rasterio


def create_histogram(raster_path, clr_path):
        color_dict = {}
        with open(clr_path, 'r') as f:
            for line in f:
                clean_line = line.strip()
                if clean_line == "":
                    continue
                    
                parts = clean_line.split()
                if len(parts) >= 5:
                    val = int(parts[0])
                    r = int(parts[1]) / 255.0
                    g = int(parts[2]) / 255.0
                    b = int(parts[3]) / 255.0
                    
                    if len(parts) >= 6:
                        label = " ".join(parts[5:])
                    if len(parts) == 5:
                        label = parts[4]
                        
                    color_dict[val] = {'color': (r, g, b), 'label': label}

        with rasterio.open(raster_path) as src:
            data = src.read(1)


        valid_data = data[data != 255]
        if len(valid_data) == 0:
            return None

        classes, counts = np.unique(valid_data, return_counts=True)
        total_pixels = len(valid_data)
        
        percentages = []
        labels = []
        colors = []
        
        for i in range(len(classes)):
            c = classes[i]
            pct = (counts[i] / total_pixels) * 100
            percentages.append(pct)
            
            if c in color_dict:
                labels.append(color_dict[c]['label'])
                colors.append(color_dict[c]['color'])
            if c not in color_dict:
                labels.append(str(c))
                colors.append((0.5, 0.5, 0.5))

        plt.figure(figsize=(10, 6))
        plt.bar(labels, percentages, color=colors)
        plt.xlabel("Classes")
        plt.ylabel("Percentage (%)")
        plt.title("Class Distribution")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        hist_path = os.path.join(os.path.dirname(raster_path), "histogram.png")
        plt.savefig(hist_path)
        plt.close()

        csv_path = os.path.join(os.path.dirname(raster_path), "histogram_data.csv")
        
        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Class", "Percentage"])
            
            for i in range(len(labels)):
                writer.writerow([labels[i], round(percentages[i], 2)])
        
        return None

if __name__ == "__main__":
    if len(sys.argv) == 4:
        raster_file = sys.argv[1]
        color_file = sys.argv[2]
        
        create_histogram(raster_file, color_file)