# EMI-CDAT: Ethiopian Meteorological Institute Climate Data Analysis Tool  🌦️🌍🚀

EMI-CDAT is designed to streamline the data workflow within the Meteorological Data and Climatology Directorate of the Ethiopian Meteorological Institute. Its primary purpose is to facilitate the production of climate bulletins, including monthly, seasonal, and annual reports. Here are the key features of EMI-CDAT:

1. **Automated Data Processing**:
   - EMI-CDAT automates the generation of charts, graphs, maps, and tabular outputs required for climate bulletins.
   - It handles data preprocessing, analysis, and visualization seamlessly.

2. **Built with Streamlit**:
   - The application is constructed and deployed using the Streamlit application development framework.
   - Streamlit provides an intuitive interface for creating interactive web apps with Python.

3. **Integration of Data Libraries**:
   - EMI-CDAT leverages various data analysis and visualization libraries, including:
     - Plotly: For interactive charts and graphs
     - SciPy: For scientific computing and statistical analysis
     - Cartopy: For geospatial data visualization
     - Geopandas: For handling geospatial data
     - Xarray: For working with labeled multi-dimensional arrays
     - Verde: For gridding and interpolation
     - Scikit-learn (Sklearn): For machine learning tasks
     - Shapely: For geometric operations
     - Regionmask: For region-based masking
     - Pykrige: For kriging interpolation
     - Seaborn: For statistical data visualization

4. **Modularized System**:
   - EMI-CDAT follows a modularized approach, promoting code reusability and maintainability.
   - Well-defined modules enable independent development and testing.
   - This structure leads to faster development cycles and robust applications.

By combining these features, EMI-CDAT provides an efficient and well-structured tool for climate data analysis and reporting.

---

EMI-CDAT offers a suite of six user-friendly modules to streamline climate data analysis. Each module tackles a specific task, making data analysis efficient and informative.

**Key functionalities:**

* **Data Importing** (**Interactive and user-friendly**): Configure input settings, upload data (CSV or Excel format), and display loaded data for further analysis.
* **Missing Data Review** (**Exploring data patterns**): Identify and visualize missing data patterns in climate datasets (Rainfall, Maximum and Minimum Temperature) through tabular reports and graphical visualizations.
* **Data Conversion** (**Seamless conversion**): Convert data between different time scales (Daily to Monthly, Monthly to Seasonal, Monthly to Annual, Seasonal to Annual).
* **Summary and Indices Calculator** (**Informative summaries and essential indices**): Generate summaries and calculate climate indices relevant to climate bulletins (Rainfall Threshold, Number of Rainy Days, Maximum Temperature and Minimum Temperature Thresholds).
* **Interpolation** (**Variety of techniques**): Transform irregularly spaced station data into regularly spaced fields using various spatial interpolation techniques (10) including Nearest Neighbor, Inverse Distance Weighting, Radial basis, Simple Kriging, Ordinary Kriging, Universal Kriging, Splines, and Gaussian Process Regressor.
* **Mapping Module** (**Seamless map generation**): Generate essential maps for climate bulletins (monthly (6), seasonal (6), or annual (6)).

**Highlights:**

* **User-friendly interface** for all modules.
* **Interactive exploration** of missing data patterns.
* **Seamless data conversion** between various time scales.
* **Essential climate indices** calculation for climate bulletins.
* **Variety of spatial interpolation techniques** for data transformation.
* **Efficient map generation** for climate analysis visualization.

---


