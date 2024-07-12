import os
import sys
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

class Visualizations:
    def __init__(self, data):
        self.df = data.copy()
        self.district_to_region = {
            "aalst": "Flanders", "antwerp": "Flanders", "arlon": "Wallonie", "ath": "Wallonie", 
            "bastogne": "Wallonie", "brugge": "Flanders", "brussels": "Brussels", "charleroi": "Wallonie", 
            "dendermonde": "Flanders", "diksmuide": "Flanders", "dinant": "Wallonie", "eeklo": "Flanders", 
            "ghent": "Flanders", "halle-vilvoorde": "Flanders", "hasselt": "Flanders", "houtain-le-val": "Wallonie", 
            "kortrijk": "Flanders", "leuven": "Flanders", "liège": "Wallonie", "maaseik": "Flanders", 
            "mechelen": "Flanders", "mons": "Wallonie", "naxhelet": "Wallonie", "ninove": "Flanders", 
            "nivelles": "Wallonie", "ostend": "Flanders", "oudenaarde": "Flanders", "pepinster": "Wallonie", 
            "rachecourt": "Wallonie", "roeselare": "Flanders", "seraing": "Wallonie", "soignies": "Wallonie", 
            "stavelot": "Wallonie", "termonde": "Flanders", "tielt": "Flanders", "tienen": "Flanders", 
            "tongeren": "Flanders", "turnhout": "Flanders", "veurne": "Flanders", "vielsalm": "Wallonie", 
            "vilvoorde": "Flanders", "waregem": "Flanders", "ypres": "Flanders"
        }
        # Combine subtypes into 'House' and 'Flat'
        self.df['CombinedType'] = self.df['SubtypeOfProperty'].apply(self.combine_subtypes)
        # Filter out 'Other'
        self.df = self.df[self.df['CombinedType'] != 'Other']
        # Map districts to regions
        self.df['Region'] = self.df['District'].map(self.district_to_region)
        # Ensure Region is correctly mapped
        self.df = self.df.dropna(subset=['Region'])

    def combine_subtypes(self, subtype):
        house_types = ['bungalow', 'chalet', 'country_cottage', 'farmhouse', 'house', 'kot', 'manor_house', 'mansion', 'mixed_use_building', 'pavilion', 'town_house', 'villa']
        flat_types = ['apartment', 'apartment_block', 'duplex', 'exceptional_property', 'flat_studio', 'ground_floor', 'loft', 'penthouse', 'service_flat', 'triplex']

        if subtype in house_types:
            return 'House'
        elif subtype in flat_types:
            return 'Flat'
        else:
            return 'Other'
        
    def heat_map(self):
        # Transform all categorical values to numerical values using LabelEncoder
        df = self.df.copy()
        label_encoders = {}
        for column in df.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column].astype(str))
            label_encoders[column] = le

        # Create a heatmap
        plt.figure(figsize=(20, 15))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')

        # Save the heatmap as a file
        plt.savefig('data/visualization/correlation_heatmap.png', bbox_inches='tight')
        plt.show()

    def plot_totalarea_to_price(self):
        # Ensure 'TotalLivingArea' and 'Price' columns exist
        if 'TotalLivingArea' not in self.df.columns or 'Price' not in self.df.columns:
            raise ValueError("DataFrame must contain 'TotalLivingArea' and 'Price' columns")

        # Create a bar chart
        plt.figure(figsize=(15, 10))
        sns.barplot(x='TotalLivingArea', y='Price', data=self.df)
        plt.title('Total Living Area vs Price')
        plt.xlabel('Total Living Area')
        plt.ylabel('Price')

        # Save the bar chart as a file
        plt.savefig('totalarea_to_price.png', bbox_inches='tight')
        plt.show()

    def plot_average_sale_price(self):
        # Map districts to regions
        self.df['Region'] = self.df['District'].map(self.district_to_region)

        # Filter data for sale
        sale_data = self.df[self.df['TypeOfSale'] == 'residential_sale']

        # Group by 'Region', 'CombinedType' to calculate the average price
        average_price_region_property = sale_data.groupby(['Region', 'CombinedType'])['Price'].mean().reset_index()

        # Set the style of the visualization
        sns.set_theme(style="whitegrid")

        # Create a figure and axis for sale prices
        plt.figure(figsize=(16, 10))
        sale_barplot = sns.barplot(x='Region', y='Price', hue='CombinedType', data=average_price_region_property, palette="flare", order=['Flanders', 'Wallonie', 'Brussels'])

        # Customize the plot for sale prices
        plt.title('Average Sale Price by Region and Property Type', fontsize=20)
        plt.ylabel('Average Price', fontsize=15)
        plt.xlabel('Region', fontsize=15)
        plt.yticks(fontsize=12)
        plt.xticks(fontsize=12, rotation=45, ha='right')  # Rotate x-axis labels for better readability
        handles, labels = sale_barplot.get_legend_handles_labels()
        plt.legend(handles=handles, labels=labels, title='Property Type', fontsize=12)

        # Add labels on the bars for sale prices
        for p in sale_barplot.patches:
            sale_barplot.annotate(format(p.get_height(), '.2f'),
                                  (p.get_x() + p.get_width() / 2., p.get_height()),
                                  ha='center', va='center',
                                  xytext=(0, 9),
                                  textcoords='offset points',
                                  fontsize=12,
                                  color='black')

        # Save the sale price bar chart as an image file
        plt.savefig('data/visualization/average_sale_price_by_region_and_combined_type.png', bbox_inches='tight')
        plt.show()


    def plot_average_rent_price(self):
        # Map districts to regions
        self.df['Region'] = self.df['District'].map(self.district_to_region)

        # Filter data for rent
        rent_data = self.df[self.df['TypeOfSale'] == 'residential_monthly_rent']

        # Group by 'Region', 'CombinedType' to calculate the average price
        average_price_region_property = rent_data.groupby(['Region', 'CombinedType'])['Price'].mean().reset_index()

        # Set the style of the visualization
        sns.set_theme(style="whitegrid")

        # Create a figure and axis for rent prices
        plt.figure(figsize=(16, 10))
        rent_barplot = sns.barplot(x='Region', y='Price', hue='CombinedType', data=average_price_region_property, palette="flare", order=['Flanders', 'Wallonie', 'Brussels'])

        # Customize the plot for rent prices
        plt.title('Average Rent Price by Region and Property Type', fontsize=20)
        plt.ylabel('Average Price', fontsize=15)
        plt.xlabel('Region', fontsize=15)
        plt.yticks(fontsize=12)
        plt.xticks(fontsize=12, rotation=45, ha='right')  # Rotate x-axis labels for better readability
        handles, labels = rent_barplot.get_legend_handles_labels()
        plt.legend(handles=handles, labels=labels, title='Property Type', fontsize=12)

        # Add labels on the bars for rent prices
        for p in rent_barplot.patches:
            rent_barplot.annotate(format(p.get_height(), '.2f'),
                                  (p.get_x() + p.get_width() / 2., p.get_height()),
                                  ha='center', va='center',
                                  xytext=(0, 9),
                                  textcoords='offset points',
                                  fontsize=12,
                                  color='black')

        # Save the rent price bar chart as an image file
        plt.savefig('data/visualization/average_rent_price_by_region_and_combined_type.png', bbox_inches='tight')
        plt.show()


    def plot_average_sale_price_region(self):
        # Filter data for sale
        sale_data = self.df[self.df['TypeOfSale'] == 'residential_sale']

        # Group by 'Region' to calculate the average price
        average_price_region = sale_data.groupby(['Region'])['Price'].mean().reset_index()

        # Set the style of the visualization
        sns.set_theme(style="whitegrid")

        # Create a figure and axis for sale prices
        plt.figure(figsize=(16, 10))
        sale_barplot = sns.barplot(x='Region', y='Price', data=average_price_region, palette="flare", order=['Flanders', 'Wallonie', 'Brussels'])

        # Customize the plot for sale prices
        plt.title('Average Sale Price by Region', fontsize=20)
        plt.ylabel('Average Price', fontsize=15)
        plt.xlabel('Region', fontsize=15)
        plt.yticks(fontsize=12)
        plt.xticks(fontsize=12, rotation=45, ha='right')  # Rotate x-axis labels for better readability

        # Add labels on the bars for sale prices
        for p in sale_barplot.patches:
            sale_barplot.annotate(format(p.get_height(), '.2f'),
                                  (p.get_x() + p.get_width() / 2., p.get_height()),
                                  ha='center', va='center',
                                  xytext=(0, 9),
                                  textcoords='offset points',
                                  fontsize=12,
                                  color='black')

        # Save the sale price bar chart as an image file
        plt.savefig('data/visualization/average_sale_price_by_region.png', bbox_inches='tight')
        plt.show()


    def plot_average_rent_price_region(self):
        # Filter data for rent
        rent_data = self.df[self.df['TypeOfSale'] == 'residential_monthly_rent']

        # Group by 'Region' to calculate the average price
        average_price_region = rent_data.groupby(['Region'])['Price'].mean().reset_index()

        # Set the style of the visualization
        sns.set_theme(style="whitegrid")

        # Create a figure and axis for rent prices
        plt.figure(figsize=(16, 10))
        rent_barplot = sns.barplot(x='Region', y='Price', data=average_price_region, palette="flare", order=['Flanders', 'Wallonie', 'Brussels'])

        # Customize the plot for rent prices
        plt.title('Average Rent Price by Region', fontsize=20)
        plt.ylabel('Average Price', fontsize=15)
        plt.xlabel('Region', fontsize=15)
        plt.yticks(fontsize=12)
        plt.xticks(fontsize=12, rotation=45, ha='right')  # Rotate x-axis labels for better readability

        # Add labels on the bars for rent prices
        for p in rent_barplot.patches:
            rent_barplot.annotate(format(p.get_height(), '.2f'),
                                  (p.get_x() + p.get_width() / 2., p.get_height()),
                                  ha='center', va='center',
                                  xytext=(0, 9),
                                  textcoords='offset points',
                                  fontsize=12,
                                  color='black')

        # Save the rent price bar chart as an image file
        plt.savefig('data/visualization/average_rent_price_by_region.png', bbox_inches='tight')
        plt.show()