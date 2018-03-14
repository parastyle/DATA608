#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

data = read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')
data = data[c('ICD.Chapter',
              'State',
              'Year',
              'Crude.Rate',
              'Deaths',
              'Population')]
data = subset(data, Year == 2010)
cause = unique(data$ICD.Chapter)
states = unique(data$State)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Mortality rates by State"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      selectInput("CoD",
                  "Cause of Death",
                  choices = cause),
      selectInput("states",
                  "State",
                  choices = states)
    ),
    
    
    # Show a plot of the generated distribution
    mainPanel(
      htmlOutput("gGraph")
    )
  )
))
