# fetch_exercise

The goal of this exercise was to build a program that took in dimensions (row, column), as well as 4 corners (x,y). The program would then
return the x y coordinates of which to plot each pixel. That data is then used to visualize the subseqent plot. 

The technology and libraries used in creation of this project was as follows:
* Python as the main programming language
* Pandas for data manipulation
* Plotly for visualizing the plot
* Dash to create the web interface 
* Docker to containerize my project
* Bash scripts to make building and running the project simplier

To build and run my project 
1. run "sh build.sh" - to build the docker image
2. run "sh run.sh" - to run the project in a docker container
3. You can then see the web interface at http://0.0.0.0:8050
