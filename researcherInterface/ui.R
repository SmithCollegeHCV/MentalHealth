
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(shinydashboard)
library(shinyBS)

body <- tabItems(
  tabItem("About",
          tabBox(width = 20,
                 tabPanel(title = 'About this Interface',
                          hr(),
                          titlePanel("What is the DSM"),
                          #h4('What is the DSM'),
                          br(),
                          h5(des1),
                          hr(),
                          titlePanel("Mental Health Interface"),
                          #h4("Mental Health Interface"),
                          br(),
                          h5(des2),
                          hr(),
                          #h4(des3),
                          titlePanel("How this Interface Works"),
                          #h4('How this Interface Works'),
                          br(),
                          h5(des4),
                          fluidRow(
                            box(
                              title = "A Data Filter tool", width = 4, background = "light-blue",
                              des5
                            ),
                            box(
                              title = "Interactive Decision Tree",width = 4, background = "light-blue",
                              des6
                            ),
                            box(
                              title = "Symptom & Chapter Similarity",width = 4, background = "light-blue",
                              des7
                            )
                          )
  
                          #fluidRow( infoBox("A Data Filter tool", des5, icon = icon("thumbs-up", lib = "glyphicon"))),
                          #fluidRow(infoBox("Interactive Decision Tree", des6, icon = icon("thumbs-up", lib = "glyphicon"))),
                          #fluidRow(infoBox("Symptom & Chapter Similarity", des7, icon = icon("thumbs-up", lib = "glyphicon")))
                          
                          
                 ),
                 tabPanel(title = 'Chapters of the DSM',
                          h4('DSM Chapters'),
                          br(),
                          dataTableOutput('chaptable')
                          
                ),
                tabPanel(title = 'Symptom Categories',
                         h4('Categories classified by Symptoms'),
                         br(),
                         dataTableOutput('category')
                         
                )
          )
  ),
          
          
  tabItem("dsmdata",
             box(width = 4,title = 'Select Features',solidHeader = T,status = 'primary',
             checkboxGroupInput("columns",label = h4("Pick the columns"),choices=vchoices,inline = T),
              submitButton("Update Symptom Selection")
                 ),
         
          mainPanel(
            tabsetPanel(
              tabPanel("Data", h3(textOutput("caption")), br(), dataTableOutput('mytable'))
            )
          )
          
  ),
  tabItem("model",

            box(width = 4,title = 'Parameter Controls',solidHeader = T,status = 'primary',collapsible = T,
                # CP Slider
                sliderInput("cp", "Adjust CP", 
                            min=0, max=0.2, value=0.01, step=0.05),
                sliderInput("minsplit", "Select Min Split", 
                            min=10, max=50, value=20, step=10),
                sliderInput("maxdepth", "Select Max Depth", 
                            min=2, max=8, value=5, step=1),
              
                #uiOutput("sliders"),
                submitButton("Update Selection"),
                hr()
                
                
            ),
          
          tabBox(width = 20,
                 tabPanel(title = 'Rpart Decision Tree',
                          h4( 'Recursive Partitioning Tree'),
                          plotOutput('Treeplot')

                 ),
                 tabPanel(title = ' RPart Model',
                          h4('Variance Explained in Tree'),
                          plotOutput('treeVE')
                 ),
                 tabPanel(title = 'CTree Decision Tree',
                          h4('Unbaised Recursive Partitioning Tree'),
                          plotOutput('ctrplot')
                 )
          )
          
  ),

  tabItem("ch",title = 'Similar Diagnosis',
          box(width = 30, title = "Chapters similar to each other in the Dataset" ,
              helpText('Diagnoses that have very similar symptom occurances are almost non distinguishable to the computer. These occurances are grouped by chapter and plotted below'),
              plotlyOutput('similarity')
          )
          
  ),
  

  tabItem("rf",title = 'Feature Importance',
          
          tabBox(width = 20,
                 tabPanel(title = "Variable Importance" ,
                          helpText('How Important were the Symptom categories in Classifiying chapters'),
                          plotlyOutput('varimp')
                 ),
                 tabPanel(title = "Symptoms Importance by Chapter " ,
                          helpText('Heat map to show the  matrix of importance of symptoms for each Chapter'),
                          helpText('Hover to see exact Symptom, Chapter and Importance'),
                          plotlyOutput('heatmap')
                 ),
          
                 tabPanel(title = "Error Rate by Chapter" ,
                          helpText('500 trees were made and at each split 5 variables were tried'),
                          helpText('Total Error rate of the model is 35.27% and the error rate by chapter is shown below'),
                          plotlyOutput('confusionplot')
                 )
          
          )
 )
)
#infoBox("Decisio byn Tree", "10% Accuracy", icon = icon("thumbs-up", lib = "glyphicon")),
# Dynamic infoBoxes
#infoBox("Random Forest", "70% Accuracy", icon = icon("thumbs-up", lib = "glyphicon"),color = "purple")




#------------------------------------------ ACTUAL UI -------------------------------------------------------#
dashboardPage(skin = 'black',
  dashboardHeader(title = HTML(paste(icon('cubes'),'DSM Interface'))
  ),
  dashboardSidebar(
    sidebarMenu(
      # Setting id makes input$tabs give the tabName of currently-selected tab
      id = "tabs",
      menuItem("About", tabName = "About", icon = icon("cog"),selected=T),
      menuItem("DSM-5",tabName = "dsmdata", icon = icon("book")),
      menuItem("Interactive Decision Tree",tabName = "model", icon = icon("sitemap")),
      menuItem("Feature Exploration", icon = icon("bar-chart"),
               menuSubItem("Non Distinguishable Diagnosis",tabName = "ch"),
               menuSubItem("RandomForest Results",tabName = "rf")
               ),
      br(),
      hr()
      #h6("Press for Chapter and Symptom Category"),
      #actionButton("symptoms", label = "Symptom Key",
                   #style='padding:4px; font-size:80%'),
      
      #actionButton("chapters", label = "Chapter Key",
                   #style='padding:4px; font-size:80%'),
      #width = 4
      
      #bsButton("symptoms", label = "Symptom Key", block = F),
      #bsButton("chapter", label = "Chapter Key", block = F)
      
    )),
  dashboardBody( 
     body
    )
)

