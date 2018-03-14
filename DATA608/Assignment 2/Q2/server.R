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
              'Crude.Rate',
              'Deaths',
              'Population')]
clNames = c('ICD.Chapter','Year','nDeaths','nPopulation')
nationalStats = aggregate(cbind(Deaths,Population)~ICD.Chapter + Year, data, FUN = sum)
colnames(nationalStats) = clNames
nationalStats$nRate = (nationalStats$nDeaths/nationalStats$nPopulation)*100000

shinyServer(function(input, output) {
  
  plotIt = reactive({
    theState = input$states
    theCause = input$CoD
    theData = subset(data,State==theState & ICD.Chapter==theCause)
    theData = merge(theData,nationalStats,by=c('ICD.Chapter','Year'))
    return(data.frame(theData[c('Year','Crude.Rate','nRate')]))
  })
  
  output$gGraph = renderGvis(gvisLineChart(plotIt(),options=list(
    title="National  vs. State \n Mortality rates",
    titleTextStyle="{color:'red', 
    fontName:'Courier', 
    fontSize:16}",                         
    vAxis="{gridlines:{color:'red', count:3}}",
    legend="bottom",
    width=500,
    height=400,
    gvis.editor='Edit me'
  )))
  
})

