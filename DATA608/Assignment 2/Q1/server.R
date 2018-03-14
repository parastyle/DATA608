#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(googleVis)
data = read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv')
data = data[c('ICD.Chapter',
              'State',
              'Year',
              'Crude.Rate')]
data = subset(data, Year == 2010)
# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  updatedData = reactive({
    codData = subset(data,ICD.Chapter == input$CoD)
    codData = codData[order(-codData$Crude.Rate),]
    return(codData)
  })

  
  
  output$gGraph = renderGvis({gvisBarChart(updatedData(),
                                           xvar="State", 
                                           yvar=c("Crude.Rate"),
                                           options=list(width="100%", 
                                                        height="1000",
                                                        chartArea="{top:'9'}",
                                                        colors="['#3ad87d']",
                                                        vAxis="{textStyle: {fontSize: '9'}}",
                                                        axes="{x: {label: 'Rate (Crude)'}}"))})
  
})