# D3_Visualization

Summary: Zillow's Home Value Prediction competition is a two-round competition in which the first round of the competition aims at predicting the Zestimate's residual error. Here, I created an effective visualization on the number (and the magnitude, and distribution) of outliers for the ZillowPrize dataset (see https://github.com/hadi-ramezani/ZillowPrize for more details) using d3.js. The main finding here is that the number of outliers (abs(logerror) > 0.5) are much smaller at the end of the year (during the months 10, 11, and 12). 

Design: 
 
* I decided to use a scatter plot to show the outliers because of the following reasons:
	1) The main goal here is to show the number of outliers not their exact location although some information on the distribution of the outliers is inherently included in the visualization.
	2) A line chart would also convey the main message here but it would lack many other information that a scatter plot would include.
	3) I was not able to find an appropriate map for my regions of interest, i.e. three California counties. 

* I decided to encode the magnitude of the logerror using the size of the circles (the bigger the logerror the bigger are the circles).

* I decided to make the layout of the plot somewhat unconventional (the height is larger that the width). I intentionally changed the shape of the plot to resemble the shape of the California state on the map.

* A legend that shows the sign of the values was not included, because it would distract the reader from the main message of the visualization. Note that the sign of the logerror is just a side information here but quite valuable.

* I decided to show the id_parcel, coordinates, and logerror upon mouse-over event. Other information can also be included here but it's beyond the scope of this project.

** Changes after receiving feedback: 
- The size of the circles were rescaled so that the data close to the boundary (logerror ~0.5) would have a finite size.
- Initially the sign of the logerror was only obtainable using mouse-over events. I encoded this information by using two different colors for the circles (blue: positive/overestimation, red: negative/underestimation)
- The animation initially stopped at month 12 after looping over all months. The reader could not see all the data at once after the author-driven section. An "All Data" button was added to visualize all data.
- The color of the buttons were changed to green.  
- The title updates correctly when all data are shown.
- I added a stacked bar chart to show the trend in the number of outliers and the ratio of the number of underestimated and overestimated outliers.


Feedback: 
1) Color circles based on the sign of the logerror.
2) Add a button that shows all data at once.
3) Update the title when showing all the data.
4) Use a different color for the buttons (green instead of orange for example).
5) Make the circles a bit bigger. Data with logerror values close to the cutoff are almost invisible. 
6) Draw the data on an actual map (this is explained in the design section)
7) Show other information upon mouse-over (out of the scope for this project but will consider later)
8) Add a stacked bar chart or a line chart to show how the number of outliers change each months.

Resources: w3schools and stackoverflow websites, d3.js documentation, and these examples: http://bl.ocks.org/weiglemc/6185069 and http://www.adeveloperdiary.com/d3-js/create-stacked-bar-chart-using-d3-js/



