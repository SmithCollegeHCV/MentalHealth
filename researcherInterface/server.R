
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
library(shiny)
library(ggplot2)
library(rpart)
library(rpart.plot)
library(readr)
library(randomForest)
library(tidyverse)
library(party)
library(plotly)
library(heatmaply)
#library(rattle)


# Data used for the Decision Tree model 

symptoms<- c("adl", "attachment", "attention","avoidance", 
             "behavior" ,"cogdev" ,"communication","concentration",
             "delusion","detachment","duration","feeling",
             "hallucination","iho" ,"impulse","motor","onset",
             "orientation","prereq","rigidity","risk","self.concept" ,
             "self.harm","sensory","sleep","sexual","somatic" ,
             "substance","thought" )

##------------------------------------------------------------- Shiny Server -----------------------------------------
  
shinyServer(function(input, output) {
  #pivot <- read_csv("~/Google Drive/2017classes/Mental health : Model and Visual/mental-health-project/Mental Health Interface/pivot.csv")

  ########### PAGE 1:  About  #######################################  

  output$chaptable = renderDataTable(dsm5)
  
  output$category = renderDataTable(catdef)
  
  ########### PAGE 2:  DSM PAGE OUTPUT #######################################  
  
  pivotMod <- select(pivot, -Code, -Symptom, -X1)
  
  observeEvent(input$columns,{
    cols <- as.numeric(input$columns)
    if(length(input$columns) == 1){
      df <- data.frame(pivot[,cols])
      names(df) <- names(pivot)[cols]
      output$mytable = renderDataTable(df)
    }else{
      output$mytable = renderDataTable(pivot[,cols])

    }
  })
 
  ########### PAGE 3:  TREE #######################################  
  
  
  
  
  
  #### Sliders
  
  symp <- select(pivot, -Chapter, -Code, -Symptom, -X1)
  output$sliders <- renderUI({
    pvars <- names(symp)
    lapply(seq(pvars), function(i) {
      sliderInput(inputId = paste0("range", pvars[i]),
                  label = pvars[i],
                  min = 0, max = 1, value = 0,step=1)
    })
  })
  
  
  
  #### TREE Plot
  
  output$Treeplot <- renderPlot({ 
    pivotMod <- select(pivot, -Code, -Symptom, -X1)
    pivotMod[sapply(pivotMod,is.integer)] <- lapply(pivotMod[sapply(pivotMod,is.integer)],as.factor)
    #pivotMod$Chapter <- as.factor(pivotMod$Chapter)
    tree2<-rpart(Chapter ~ ., data=pivotMod, method="class",control= rpart.control(minsplit = input$minsplit,  cp = input$cp, maxdepth = input$maxdepth))
    #fancyRpartPlot(tree2)
    rpart.plot(tree2, # middle graph
               extra=102,
               branch.lty=3, shadow.col="gray", nn=TRUE)
    
  })
  
  ##### Variance Explained plot
  
  output$treeVE <- renderPlot({ 
    pivotMod <- select(pivot, -Code, -Symptom, -X1)
    pivotMod[sapply(pivotMod,is.integer)] <- lapply(pivotMod[sapply(pivotMod,is.integer)],as.factor)
    #pivotMod$Chapter <- as.factor(pivotMod$Chapter)
    tree2<-rpart(Chapter ~ ., data=pivotMod, method="class",control= rpart.control(minsplit = input$minsplit,  cp = input$cp, maxdepth = input$maxdepth))
    plotcp(tree2)
    
  })
  
  #### TREE Plot
  
  output$ctrplot <- renderPlot({ 
    pivotMod <- select(pivot, -Code, -Symptom, -X1)
    pivotMod[sapply(pivotMod,is.integer)] <- lapply(pivotMod[sapply(pivotMod,is.integer)],as.factor)
    #pivotMod$Chapter <- as.factor(pivotMod$Chapter)
    cit<-ctree(Chapter ~ ., data=pivotMod, control = ctree_control(minsplit = input$minsplit, maxdepth = input$maxdepth))
    plot(cit)
    
  })
  
  ########### PAGE 3: PT 1 : Chapter similarity#######################################  
  
  output$similarity <- renderPlotly({
    chaps<- 1:19
    Chapter<- as.array(chaps)
    Frequency <- as.array(c(28,13,1,0,6,6,7,2,14,0,2,14,7,2,3,30,2,1,2))
    chapFreq<- data.frame(Chapter,Frequency)
    #chapFreq$Frequency <- as.integer(chapFreq$Frequency)
    chapFreq$Chapter <- as.factor(chapFreq$Chapter)
    chapFreq_plot <- ggplot(chapFreq, aes(x = Chapter, y = Frequency, text = paste("Chapter:", Chapter, "<br>", "Number of Non-distinguishable Diagnoses:", Frequency))) + geom_bar(stat = "identity", fill = I("skyblue")) + 
      theme_classic() + ylab("Number of Non-distinguishable Diagnoses per Chapter")
    ggplotly(chapFreq_plot, tooltip = c("text"))
    
  })
  ########### PAGE 3: PT 2 : Random Foest#######################################  
 
  #TAB 1: Varibale Importance
  
  output$varimp <- renderPlotly({ 
    
    #variable importance-mean decrease in accuracy of symptoms in random forest
    varImp_plot <- ggplot(mean_dec_acc, aes(x = reorder(Symptom, -MeanDecreaseAccuracy), y = MeanDecreaseAccuracy, text = paste("Symptom:", Symptom, "<br>", "Mean Decrease in Accuracy:", MeanDecreaseAccuracy))) + 
      geom_bar(stat = "identity",  fill = I("skyblue")) + xlab("Symptom") + 
      ylab("Mean Decrease in Accuracy") + ggtitle("Variable Importance for Random Forest") +
      theme_classic() +  coord_flip() 
    varImp_plot <- ggplotly(varImp_plot, tooltip = c("text"))
    varImp_plot
    
    
    
  })
  
  #TAB 2: Heatmap
  
  output$heatmap <- renderPlotly({ 
    
    heatmaply(varchap, k_col = 2, k_row = 3) %>% layout(margin = list(l = 130, b = 40))
    
    
    
  })
  
  # TAB 3: Chapter wise error rate bar chart
  
  output$confusionplot <- renderPlotly({ 
    
    confusion_plot <- ggplot(misclass, aes(x = misclass$Chapter, y =misclass$class.error)) + geom_bar(stat = "identity", aes(fill = Occurance)) + 
      
      ylab("Class Error") + xlab("Chapter") +theme_classic()
    
    confusion_plot <- ggplotly(confusion_plot)
    
    confusion_plot
    
  }) 
  
  
################## end of server
}) 
  
